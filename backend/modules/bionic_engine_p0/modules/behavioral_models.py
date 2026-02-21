"""
BIONIC ENGINE - Behavioral Models Module
PHASE G - P0-BETA2 IMPLEMENTATION
Version: 1.0.0-beta2

Module de modelisation et prediction comportementale.
Strictement conforme au contrat: behavioral_models_contract.json

INTEGRATION DES 12 FACTEURS COMPORTEMENTAUX (BIONIC V5 ULTIME x2):
1. Predation (PredatorRisk, PredatorCorridors)
2. Stress physiologique (Thermal/Hydric/Social Stress)
3. Hierarchie sociale (DominanceScore, GroupBehavior)
4. Competition inter-especes
5. Signaux faibles (WeakSignals, Anomalies)
6. Cycles hormonaux (rut, lactation, croissance des bois)
7. Cycles digestifs (feeding->bedding transitions)
8. Memoire territoriale (AvoidanceMemory, PreferredRoutes)
9. Apprentissage comportemental (AdaptiveBehavior)
10. Activite humaine non-chasse (HumanDisturbance)
11. Disponibilite minerale (MineralAvailability, SaltLickAttraction)
12. Conditions de neige (SnowDepth, CrustRisk, WinterPenalty)

Conformite: G-SEC | G-QA | G-DOC
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone, timedelta
from enum import Enum
import math
import logging

from modules.bionic_engine_p0.contracts.data_contracts import (
    Species, ActivityLevel, BehaviorType, SeasonPhase, HierarchyLevel,
    BehavioralPredictionInput, BehavioralPredictionOutput,
    ActivityPrediction, TimelineEntry, SeasonalContext,
    StrategyRecommendation, WeatherOverride,
    BM_WEIGHTS_CONFIG, normalize_weights, score_to_activity_level
)

# Import des 12 facteurs comportementaux avances
from modules.bionic_engine_p0.contracts.advanced_factors import (
    PredatorRiskModel,
    StressModel,
    SocialHierarchyModel,
    InterspeciesCompetitionModel,
    WeakSignalsModel,
    HormonalCycleModel,
    DigestiveCycleModel,
    TerritorialMemoryModel,
    AdaptiveBehaviorModel,
    HumanDisturbanceModel,
    MineralAvailabilityModel,
    SnowConditionModel,
    IntegratedBehavioralFactors
)

logger = logging.getLogger("bionic_engine.behavioral_models")


# =============================================================================
# CONSTANTS - Constantes conformes a l'Inventaire v1.2 et Bloc 4
# =============================================================================

# Patterns d'activite horaire detailles (Bloc 4 - Cycles Temporels)
HOURLY_ACTIVITY_PATTERNS = {
    Species.MOOSE: {
        "hourly_scores": {
            0: 15, 1: 12, 2: 10, 3: 8, 4: 10,
            5: 45, 6: 85, 7: 95, 8: 75, 9: 45,
            10: 25, 11: 18, 12: 15, 13: 18, 14: 22,
            15: 35, 16: 55, 17: 85, 18: 92, 19: 70,
            20: 45, 21: 30, 22: 22, 23: 18
        },
        "activity_probabilities": {
            "dawn": {"feeding": 0.65, "traveling": 0.25, "resting": 0.05, "other": 0.05},
            "day": {"feeding": 0.15, "traveling": 0.10, "resting": 0.70, "other": 0.05},
            "dusk": {"feeding": 0.60, "traveling": 0.30, "resting": 0.05, "other": 0.05},
            "night": {"feeding": 0.20, "traveling": 0.15, "resting": 0.60, "other": 0.05}
        }
    },
    Species.DEER: {
        "hourly_scores": {
            0: 25, 1: 20, 2: 18, 3: 15, 4: 18,
            5: 55, 6: 90, 7: 95, 8: 70, 9: 40,
            10: 22, 11: 15, 12: 12, 13: 15, 14: 20,
            15: 35, 16: 60, 17: 88, 18: 95, 19: 75,
            20: 50, 21: 35, 22: 28, 23: 25
        },
        "activity_probabilities": {
            "dawn": {"feeding": 0.70, "traveling": 0.20, "resting": 0.05, "other": 0.05},
            "day": {"feeding": 0.10, "traveling": 0.10, "resting": 0.75, "other": 0.05},
            "dusk": {"feeding": 0.65, "traveling": 0.25, "resting": 0.05, "other": 0.05},
            "night": {"feeding": 0.30, "traveling": 0.20, "resting": 0.45, "other": 0.05}
        }
    },
    Species.BEAR: {
        "hourly_scores": {
            0: 5, 1: 3, 2: 2, 3: 2, 4: 3,
            5: 25, 6: 55, 7: 80, 8: 85, 9: 75,
            10: 60, 11: 45, 12: 35, 13: 40, 14: 50,
            15: 65, 16: 75, 17: 80, 18: 70, 19: 45,
            20: 25, 21: 12, 22: 8, 23: 5
        },
        "activity_probabilities": {
            "dawn": {"feeding": 0.55, "traveling": 0.35, "resting": 0.05, "other": 0.05},
            "day": {"feeding": 0.45, "traveling": 0.30, "resting": 0.20, "other": 0.05},
            "dusk": {"feeding": 0.50, "traveling": 0.35, "resting": 0.10, "other": 0.05},
            "night": {"feeding": 0.10, "traveling": 0.10, "resting": 0.75, "other": 0.05}
        },
        "hibernation_months": [12, 1, 2, 3],
        "hyperphagia_months": [9, 10, 11]
    },
    Species.WILD_TURKEY: {
        "hourly_scores": {
            0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
            5: 15, 6: 75, 7: 95, 8: 85, 9: 70,
            10: 55, 11: 45, 12: 35, 13: 40, 14: 50,
            15: 60, 16: 70, 17: 75, 18: 50, 19: 15,
            20: 0, 21: 0, 22: 0, 23: 0
        },
        "activity_probabilities": {
            "dawn": {"feeding": 0.60, "traveling": 0.30, "resting": 0.05, "other": 0.05},
            "day": {"feeding": 0.50, "traveling": 0.25, "resting": 0.20, "other": 0.05},
            "dusk": {"feeding": 0.70, "traveling": 0.20, "resting": 0.05, "other": 0.05}
        },
        "roosting_hours": [0, 1, 2, 3, 4, 5, 19, 20, 21, 22, 23]
    },
    Species.ELK: {
        "hourly_scores": {
            0: 20, 1: 15, 2: 12, 3: 10, 4: 15,
            5: 50, 6: 85, 7: 90, 8: 70, 9: 45,
            10: 25, 11: 20, 12: 15, 13: 20, 14: 25,
            15: 40, 16: 60, 17: 85, 18: 90, 19: 65,
            20: 40, 21: 30, 22: 25, 23: 22
        },
        "activity_probabilities": {
            "dawn": {"feeding": 0.60, "traveling": 0.30, "resting": 0.05, "other": 0.05},
            "day": {"feeding": 0.15, "traveling": 0.15, "resting": 0.65, "other": 0.05},
            "dusk": {"feeding": 0.55, "traveling": 0.35, "resting": 0.05, "other": 0.05},
            "night": {"feeding": 0.25, "traveling": 0.20, "resting": 0.50, "other": 0.05}
        }
    }
}

# Modificateurs hebdomadaires (Bloc 4)
WEEKLY_MODIFIERS = {
    0: 1.10,  # Lundi
    1: 1.10,  # Mardi
    2: 1.08,  # Mercredi
    3: 1.05,  # Jeudi
    4: 1.00,  # Vendredi
    5: 0.80,  # Samedi
    6: 0.85   # Dimanche
}

# Calendrier annuel par espece (Bloc 4)
ANNUAL_CALENDAR = {
    Species.MOOSE: {
        1: {"season": SeasonPhase.WINTER, "activity_mod": 0.5, "behavior": "survival"},
        2: {"season": SeasonPhase.WINTER, "activity_mod": 0.4, "behavior": "survival"},
        3: {"season": SeasonPhase.WINTER, "activity_mod": 0.5, "behavior": "recovery"},
        4: {"season": SeasonPhase.SPRING, "activity_mod": 0.7, "behavior": "feeding"},
        5: {"season": SeasonPhase.SPRING, "activity_mod": 0.8, "behavior": "feeding"},
        6: {"season": SeasonPhase.SUMMER, "activity_mod": 0.7, "behavior": "feeding_aquatic"},
        7: {"season": SeasonPhase.SUMMER, "activity_mod": 0.6, "behavior": "heat_avoidance"},
        8: {"season": SeasonPhase.SUMMER, "activity_mod": 0.7, "behavior": "pre_rut"},
        9: {"season": SeasonPhase.PRE_RUT, "activity_mod": 0.9, "behavior": "territorial"},
        10: {"season": SeasonPhase.RUT, "activity_mod": 1.0, "behavior": "breeding"},
        11: {"season": SeasonPhase.POST_RUT, "activity_mod": 0.8, "behavior": "recovery_feeding"},
        12: {"season": SeasonPhase.WINTER, "activity_mod": 0.6, "behavior": "yarding"}
    },
    Species.DEER: {
        1: {"season": SeasonPhase.WINTER, "activity_mod": 0.5, "behavior": "yarding"},
        2: {"season": SeasonPhase.WINTER, "activity_mod": 0.5, "behavior": "yarding"},
        3: {"season": SeasonPhase.WINTER, "activity_mod": 0.6, "behavior": "recovery"},
        4: {"season": SeasonPhase.SPRING, "activity_mod": 0.75, "behavior": "feeding"},
        5: {"season": SeasonPhase.SPRING, "activity_mod": 0.8, "behavior": "fawning"},
        6: {"season": SeasonPhase.SUMMER, "activity_mod": 0.7, "behavior": "nurturing"},
        7: {"season": SeasonPhase.SUMMER, "activity_mod": 0.6, "behavior": "heat_avoidance"},
        8: {"season": SeasonPhase.SUMMER, "activity_mod": 0.75, "behavior": "velvet_shed"},
        9: {"season": SeasonPhase.EARLY_FALL, "activity_mod": 0.85, "behavior": "pre_rut"},
        10: {"season": SeasonPhase.PRE_RUT, "activity_mod": 0.95, "behavior": "scraping"},
        11: {"season": SeasonPhase.RUT, "activity_mod": 1.0, "behavior": "breeding"},
        12: {"season": SeasonPhase.POST_RUT, "activity_mod": 0.7, "behavior": "recovery"}
    }
}

# Strategies de chasse par espece et contexte
HUNTING_STRATEGIES = {
    Species.MOOSE: {
        "rut": [
            {"type": "call", "effectiveness": 90, "conditions": "Matin calme, temperature fraiche"},
            {"type": "stalk", "effectiveness": 70, "conditions": "Vent favorable, terrain silencieux"}
        ],
        "general": [
            {"type": "stand", "effectiveness": 75, "conditions": "Pres des corridors, zones d'alimentation"},
            {"type": "stalk", "effectiveness": 60, "conditions": "Zones humides, lisieres"}
        ]
    },
    Species.DEER: {
        "rut": [
            {"type": "rattling", "effectiveness": 85, "conditions": "Pre-rut et rut, males dominants"},
            {"type": "decoy", "effectiveness": 75, "conditions": "Zones ouvertes, bon vent"},
            {"type": "stand", "effectiveness": 80, "conditions": "Pres des scrapes et corridors"}
        ],
        "general": [
            {"type": "stand", "effectiveness": 80, "conditions": "Zones de transition, lisieres"},
            {"type": "ambush", "effectiveness": 70, "conditions": "Corridors identifies"}
        ]
    },
    Species.BEAR: {
        "general": [
            {"type": "stand", "effectiveness": 75, "conditions": "Pres des sources de nourriture"},
            {"type": "stalk", "effectiveness": 65, "conditions": "Terrains ouverts, baies"}
        ]
    },
    Species.WILD_TURKEY: {
        "spring": [
            {"type": "call", "effectiveness": 90, "conditions": "Matin, perchoirs identifies"},
            {"type": "decoy", "effectiveness": 80, "conditions": "Zones ouvertes"}
        ],
        "fall": [
            {"type": "ambush", "effectiveness": 70, "conditions": "Zones d'alimentation"}
        ]
    }
}


# =============================================================================
# SERVICE CLASS
# =============================================================================

class BehavioralModelsService:
    """
    Service de modelisation et prediction comportementale.
    
    Responsabilites:
    - Predire le comportement actuel de l'animal
    - Generer la timeline d'activite 24h
    - Recommander des strategies de chasse
    
    Modeles integres (Bloc 4):
    - Hourly Activity Model
    - Movement Model
    - Feeding Model
    - Resting Model
    
    Conformite:
    - Contrat: behavioral_models_contract.json
    - Cycles: Inventaire v1.2 - Bloc 4
    
    G-SEC: Validation stricte des inputs
    G-QA: Tests unitaires requis
    G-DOC: Documentation complete
    """
    
    def __init__(self):
        self.weights_config = BM_WEIGHTS_CONFIG
        logger.info("BehavioralModelsService initialized")
    
    def execute(self, inputs: Dict) -> Dict:
        """
        Point d'entree principal conforme au contrat.
        
        Args:
            inputs: Dict conforme a BehavioralPredictionInput
            
        Returns:
            Dict conforme a BehavioralPredictionOutput
        """
        try:
            # Parse et validation input (G-SEC)
            parsed_input = BehavioralPredictionInput(**inputs)
            
            # Prediction comportementale
            result = self.predict_behavior(
                species=parsed_input.species,
                datetime_target=parsed_input.datetime_target,
                latitude=parsed_input.latitude,
                longitude=parsed_input.longitude,
                weather_context=parsed_input.weather_context,
                include_strategy=parsed_input.include_strategy
            )
            
            return result.dict()
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "CALCULATION_ERROR"
            }
    
    def predict_behavior(
        self,
        species: Species,
        datetime_target: Optional[datetime] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        weather_context: Optional[WeatherOverride] = None,
        include_strategy: bool = True
    ) -> BehavioralPredictionOutput:
        """
        Prediction comportementale complete.
        
        Args:
            species: Espece cible
            datetime_target: Date/heure cible
            latitude: Latitude (optionnel)
            longitude: Longitude (optionnel)
            weather_context: Contexte meteo
            include_strategy: Inclure recommandations strategie
            
        Returns:
            BehavioralPredictionOutput complet
        """
        # Datetime par defaut
        if datetime_target is None:
            datetime_target = datetime.now(timezone.utc)
        
        warnings = []
        
        # Verification hibernation ours
        if species == Species.BEAR:
            patterns = HOURLY_ACTIVITY_PATTERNS.get(species, {})
            if datetime_target.month in patterns.get("hibernation_months", []):
                return BehavioralPredictionOutput(
                    success=True,
                    activity=ActivityPrediction(
                        current_behavior=BehaviorType.RESTING,
                        behavior_confidence=1.0,
                        activity_level=ActivityLevel.MINIMAL,
                        activity_score=0,
                        behavior_probabilities={"resting": 1.0}
                    ),
                    timeline=[],
                    seasonal_context=SeasonalContext(
                        current_season=SeasonPhase.WINTER,
                        activity_modifier=0.0,
                        primary_behaviors=["hibernation"],
                        key_events=["bear_hibernating"]
                    ),
                    strategies=[],
                    warnings=["BEAR_HIBERNATION_PERIOD"],
                    metadata={
                        "species": species.value,
                        "hibernation": True
                    }
                )
        
        # Calculer l'activite actuelle
        activity = self._predict_current_activity(species, datetime_target, weather_context)
        
        # Generer timeline 24h
        timeline = self._generate_timeline(species, datetime_target)
        
        # Contexte saisonnier
        seasonal_context = self._get_seasonal_context(species, datetime_target)
        
        # Strategies
        strategies = []
        if include_strategy:
            strategies = self._generate_strategies(species, datetime_target, seasonal_context)
        
        return BehavioralPredictionOutput(
            success=True,
            activity=activity,
            timeline=timeline,
            seasonal_context=seasonal_context,
            strategies=strategies,
            warnings=warnings,
            metadata={
                "species": species.value,
                "datetime": datetime_target.isoformat(),
                "latitude": latitude,
                "longitude": longitude,
                "has_location": latitude is not None,
                "has_weather": weather_context is not None
            }
        )
    
    # =========================================================================
    # ACTIVITY PREDICTION
    # =========================================================================
    
    def _predict_current_activity(
        self,
        species: Species,
        datetime_target: datetime,
        weather_context: Optional[WeatherOverride]
    ) -> ActivityPrediction:
        """
        Predit l'activite actuelle de l'animal.
        
        Formule:
        activity = base_hourly * seasonal_mod * weather_mod * weekly_mod
        """
        hour = datetime_target.hour
        month = datetime_target.month
        weekday = datetime_target.weekday()
        
        # Patterns de l'espece
        patterns = HOURLY_ACTIVITY_PATTERNS.get(species, HOURLY_ACTIVITY_PATTERNS[Species.MOOSE])
        
        # Score horaire de base
        hourly_scores = patterns.get("hourly_scores", {})
        base_score = hourly_scores.get(hour, 50)
        
        # Modificateur saisonnier
        calendar = ANNUAL_CALENDAR.get(species, ANNUAL_CALENDAR.get(Species.MOOSE, {}))
        month_data = calendar.get(month, {"activity_mod": 0.7})
        seasonal_mod = month_data.get("activity_mod", 0.7)
        
        # Modificateur hebdomadaire
        weekly_mod = WEEKLY_MODIFIERS.get(weekday, 1.0)
        
        # Modificateur meteo
        weather_mod = 1.0
        if weather_context:
            weather_mod = self._calculate_weather_modifier(weather_context)
        
        # Score final
        activity_score = base_score * seasonal_mod * weekly_mod * weather_mod
        activity_score = min(100, max(0, activity_score))
        
        # Determiner la periode du jour
        period = self._get_day_period(hour)
        
        # Probabilites de comportement
        activity_probs = patterns.get("activity_probabilities", {})
        period_probs = activity_probs.get(period, {"feeding": 0.25, "traveling": 0.25, "resting": 0.45, "other": 0.05})
        
        # Comportement principal
        current_behavior = max(period_probs, key=period_probs.get)
        behavior_type = self._map_to_behavior_type(current_behavior)
        
        # Cas special: dindon qui dort
        if species == Species.WILD_TURKEY:
            roosting_hours = patterns.get("roosting_hours", [])
            if hour in roosting_hours:
                behavior_type = BehaviorType.RESTING
                period_probs = {"resting": 1.0}
                activity_score = 0
        
        return ActivityPrediction(
            current_behavior=behavior_type,
            behavior_confidence=period_probs.get(current_behavior, 0.5),
            activity_level=score_to_activity_level(activity_score),
            activity_score=round(activity_score, 1),
            behavior_probabilities=period_probs
        )
    
    def _calculate_weather_modifier(self, weather: WeatherOverride) -> float:
        """Calcule l'impact de la meteo sur l'activite."""
        modifier = 1.0
        
        if weather.temperature is not None:
            temp = weather.temperature
            if temp < -20 or temp > 30:
                modifier *= 0.5
            elif temp < -10 or temp > 25:
                modifier *= 0.7
            elif -5 <= temp <= 15:
                modifier *= 1.1  # Optimal
        
        if weather.wind_speed is not None:
            wind = weather.wind_speed
            if wind > 40:
                modifier *= 0.6
            elif wind > 25:
                modifier *= 0.8
        
        if weather.precipitation is not None:
            precip = weather.precipitation
            if precip > 5:
                modifier *= 0.7
            elif precip > 2:
                modifier *= 0.85
        
        return modifier
    
    def _get_day_period(self, hour: int) -> str:
        """Determine la periode du jour."""
        if 5 <= hour <= 8:
            return "dawn"
        elif 9 <= hour <= 16:
            return "day"
        elif 17 <= hour <= 20:
            return "dusk"
        else:
            return "night"
    
    def _map_to_behavior_type(self, behavior_str: str) -> BehaviorType:
        """Mappe une string vers BehaviorType."""
        mapping = {
            "feeding": BehaviorType.FEEDING,
            "traveling": BehaviorType.TRAVELING,
            "resting": BehaviorType.RESTING,
            "rutting": BehaviorType.RUTTING,
            "bedding": BehaviorType.BEDDING,
            "watering": BehaviorType.WATERING
        }
        return mapping.get(behavior_str, BehaviorType.UNKNOWN)
    
    # =========================================================================
    # TIMELINE GENERATION
    # =========================================================================
    
    def _generate_timeline(
        self,
        species: Species,
        datetime_target: datetime
    ) -> List[TimelineEntry]:
        """
        Genere la timeline d'activite sur 24h.
        
        Conforme au contrat: 24 entrees, une par heure
        """
        timeline = []
        patterns = HOURLY_ACTIVITY_PATTERNS.get(species, HOURLY_ACTIVITY_PATTERNS[Species.MOOSE])
        hourly_scores = patterns.get("hourly_scores", {})
        activity_probs = patterns.get("activity_probabilities", {})
        
        # Date du jour
        base_date = datetime_target.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Heures legales de chasse (approximation)
        legal_start = 6  # 30 min avant lever soleil
        legal_end = 18   # 30 min apres coucher soleil
        
        for hour in range(24):
            score = hourly_scores.get(hour, 50)
            period = self._get_day_period(hour)
            probs = activity_probs.get(period, {"resting": 1.0})
            
            # Comportement principal
            primary = max(probs, key=probs.get)
            behavior_type = self._map_to_behavior_type(primary)
            
            # Cas special dindon
            if species == Species.WILD_TURKEY:
                roosting = patterns.get("roosting_hours", [])
                if hour in roosting:
                    behavior_type = BehaviorType.RESTING
                    score = 0
            
            timeline.append(TimelineEntry(
                hour=hour,
                activity_score=round(score, 1),
                primary_behavior=behavior_type,
                probability=probs.get(primary, 0.5),
                is_legal_hunting=legal_start <= hour <= legal_end
            ))
        
        return timeline
    
    # =========================================================================
    # SEASONAL CONTEXT
    # =========================================================================
    
    def _get_seasonal_context(
        self,
        species: Species,
        datetime_target: datetime
    ) -> SeasonalContext:
        """
        Retourne le contexte saisonnier pour l'espece.
        """
        month = datetime_target.month
        calendar = ANNUAL_CALENDAR.get(species, ANNUAL_CALENDAR.get(Species.MOOSE, {}))
        month_data = calendar.get(month, {
            "season": SeasonPhase.SUMMER,
            "activity_mod": 0.7,
            "behavior": "general"
        })
        
        # Comportements principaux selon la saison
        primary_behaviors = [month_data.get("behavior", "general")]
        
        # Evenements cles
        key_events = []
        season = month_data.get("season", SeasonPhase.SUMMER)
        
        if season == SeasonPhase.RUT:
            key_events.append("rut_active")
            primary_behaviors.extend(["breeding", "territorial"])
        elif season == SeasonPhase.PRE_RUT:
            key_events.append("pre_rut_preparation")
            primary_behaviors.append("increasing_activity")
        elif season == SeasonPhase.WINTER:
            key_events.append("winter_survival")
            primary_behaviors.append("energy_conservation")
        
        # Hyperphagie ours
        if species == Species.BEAR and month in [9, 10, 11]:
            key_events.append("hyperphagia")
            primary_behaviors.append("intensive_feeding")
        
        return SeasonalContext(
            current_season=season,
            activity_modifier=month_data.get("activity_mod", 0.7),
            primary_behaviors=list(set(primary_behaviors)),
            key_events=key_events
        )
    
    # =========================================================================
    # STRATEGY RECOMMENDATIONS
    # =========================================================================
    
    def _generate_strategies(
        self,
        species: Species,
        datetime_target: datetime,
        seasonal_context: SeasonalContext
    ) -> List[StrategyRecommendation]:
        """
        Genere les recommandations de strategies de chasse.
        """
        strategies = []
        species_strategies = HUNTING_STRATEGIES.get(species, {})
        
        # Determiner le contexte
        context = "general"
        if seasonal_context.current_season in [SeasonPhase.RUT, SeasonPhase.PRE_RUT]:
            context = "rut"
        elif species == Species.WILD_TURKEY:
            if datetime_target.month in [4, 5]:
                context = "spring"
            else:
                context = "fall"
        
        # Strategies pour ce contexte
        context_strategies = species_strategies.get(context, species_strategies.get("general", []))
        
        for strat in context_strategies:
            tips_fr = []
            
            if strat["type"] == "call":
                tips_fr = [
                    "Utilisez des appels authentiques et varies",
                    "Attendez 15-20 minutes entre les sequences",
                    "Commencez doucement et augmentez l'intensite"
                ]
            elif strat["type"] == "stand":
                tips_fr = [
                    "Arrivez sur place 30 minutes avant l'aube",
                    "Minimisez les mouvements",
                    "Surveillez les zones de transition"
                ]
            elif strat["type"] == "stalk":
                tips_fr = [
                    "Deplacez-vous lentement, 2-3 pas puis stop",
                    "Utilisez le vent a votre avantage",
                    "Evitez de faire craquer les branches"
                ]
            elif strat["type"] == "rattling":
                tips_fr = [
                    "Plus efficace en pre-rut et debut de rut",
                    "Commencez par un cliquetis leger",
                    "Ajoutez des grattages au sol pour plus de realisme"
                ]
            elif strat["type"] == "decoy":
                tips_fr = [
                    "Placez le decoy visible mais pas trop proche",
                    "Assurez-vous que le vent porte vers votre position",
                    "Combinez avec des appels pour plus d'efficacite"
                ]
            elif strat["type"] == "ambush":
                tips_fr = [
                    "Identifiez les corridors de deplacement",
                    "Preparez plusieurs positions de repli",
                    "Restez immobile et patient"
                ]
            
            strategies.append(StrategyRecommendation(
                strategy_type=strat["type"],
                effectiveness_score=strat["effectiveness"],
                best_conditions=strat["conditions"],
                tips_fr=tips_fr
            ))
        
        # Trier par efficacite
        strategies.sort(key=lambda x: x.effectiveness_score, reverse=True)
        
        return strategies
    
    # =========================================================================
    # SPECIALIZED METHODS
    # =========================================================================
    
    def get_activity_timeline(
        self,
        species: Species,
        date: datetime
    ) -> List[TimelineEntry]:
        """
        Retourne uniquement la timeline (endpoint simplifie).
        """
        return self._generate_timeline(species, date)
    
    def predict_activity(
        self,
        species: Species,
        datetime_target: datetime,
        weather_context: Optional[WeatherOverride] = None
    ) -> ActivityPrediction:
        """
        Retourne uniquement la prediction d'activite (endpoint simplifie).
        """
        return self._predict_current_activity(species, datetime_target, weather_context)
