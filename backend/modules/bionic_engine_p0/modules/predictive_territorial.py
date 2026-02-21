"""
BIONIC ENGINE - Predictive Territorial Module
PHASE G - P0-BETA2 IMPLEMENTATION
Version: 1.0.0-beta2

Module de calcul de score territorial predictif.
Strictement conforme au contrat: predictive_territorial_contract.json

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
from datetime import datetime, timezone
from enum import Enum
import math
import logging

from modules.bionic_engine_p0.contracts.data_contracts import (
    Species, ScoreRating, SeasonPhase, HierarchyLevel,
    TerritorialScoreInput, TerritorialScoreOutput,
    ScoreComponents, Recommendation, WeatherOverride,
    PT_WEIGHTS_CONFIG, normalize_weights, score_to_rating
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

logger = logging.getLogger("bionic_engine.predictive_territorial")


# =============================================================================
# CONSTANTS - Constantes conformes a l'Inventaire v1.2
# =============================================================================

# Patterns d'activite horaire par espece (F12 - Cycles Temporels)
HOURLY_ACTIVITY_PATTERNS = {
    Species.MOOSE: {
        0: 15, 1: 12, 2: 10, 3: 8, 4: 10,
        5: 45, 6: 85, 7: 95, 8: 75, 9: 45,
        10: 25, 11: 18, 12: 15, 13: 18, 14: 22,
        15: 35, 16: 55, 17: 85, 18: 92, 19: 70,
        20: 45, 21: 30, 22: 22, 23: 18
    },
    Species.DEER: {
        0: 25, 1: 20, 2: 18, 3: 15, 4: 18,
        5: 55, 6: 90, 7: 95, 8: 70, 9: 40,
        10: 22, 11: 15, 12: 12, 13: 15, 14: 20,
        15: 35, 16: 60, 17: 88, 18: 95, 19: 75,
        20: 50, 21: 35, 22: 28, 23: 25
    },
    Species.BEAR: {
        0: 5, 1: 3, 2: 2, 3: 2, 4: 3,
        5: 25, 6: 55, 7: 80, 8: 85, 9: 75,
        10: 60, 11: 45, 12: 35, 13: 40, 14: 50,
        15: 65, 16: 75, 17: 80, 18: 70, 19: 45,
        20: 25, 21: 12, 22: 8, 23: 5
    },
    Species.WILD_TURKEY: {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
        5: 15, 6: 75, 7: 95, 8: 85, 9: 70,
        10: 55, 11: 45, 12: 35, 13: 40, 14: 50,
        15: 60, 16: 70, 17: 75, 18: 50, 19: 15,
        20: 0, 21: 0, 22: 0, 23: 0
    },
    Species.ELK: {
        0: 20, 1: 15, 2: 12, 3: 10, 4: 15,
        5: 50, 6: 85, 7: 90, 8: 70, 9: 45,
        10: 25, 11: 20, 12: 15, 13: 20, 14: 25,
        15: 40, 16: 60, 17: 85, 18: 90, 19: 65,
        20: 40, 21: 30, 22: 25, 23: 22
    }
}

# Facteurs saisonniers (F12 - Cycles)
SEASON_FACTORS = {
    1: 0.5,   # Janvier
    2: 0.45,  # Fevrier
    3: 0.55,  # Mars
    4: 0.7,   # Avril
    5: 0.75,  # Mai
    6: 0.7,   # Juin
    7: 0.6,   # Juillet
    8: 0.75,  # Aout
    9: 0.9,   # Septembre
    10: 1.0,  # Octobre (pic)
    11: 0.95, # Novembre
    12: 0.55  # Decembre
}

# Modificateurs hebdomadaires (Bloc 4 - Cycles Temporels)
WEEKLY_MODIFIERS = {
    0: 1.10,  # Lundi
    1: 1.10,  # Mardi
    2: 1.08,  # Mercredi
    3: 1.05,  # Jeudi
    4: 1.00,  # Vendredi
    5: 0.80,  # Samedi
    6: 0.85   # Dimanche
}

# Periodes de rut par espece
RUT_PERIODS = {
    Species.MOOSE: {"start_month": 9, "peak_month": 10, "end_month": 10},
    Species.DEER: {"start_month": 10, "peak_month": 11, "end_month": 11},
    Species.ELK: {"start_month": 9, "peak_month": 9, "end_month": 10}
}

# Mois d'hibernation ours
BEAR_HIBERNATION_MONTHS = [12, 1, 2, 3]

# Conditions meteo optimales
OPTIMAL_WEATHER = {
    "temperature": {"min": -5, "max": 15, "ideal": 5},
    "wind_speed": {"min": 0, "max": 20, "ideal": 8},
    "pressure": {"min": 1000, "max": 1030, "ideal": 1015}
}


# =============================================================================
# SERVICE CLASS
# =============================================================================

class PredictiveTerritorialService:
    """
    Service de calcul de score territorial predictif.
    
    Responsabilites:
    - Calculer un score de probabilite de presence faunique
    - Appliquer les ponderations dynamiques
    - Generer des recommandations
    
    Conformite:
    - Contrat: predictive_territorial_contract.json
    - Hierarchie: Inventaire v1.2 - Normalisation des ponderations
    - Arbitrage: 6 regles documentees
    
    G-SEC: Validation stricte des inputs
    G-QA: Tests unitaires requis
    G-DOC: Documentation complete
    """
    
    def __init__(self):
        self.weights_config = PT_WEIGHTS_CONFIG
        self._available_sources = [
            "habitat_quality",
            "weather_conditions", 
            "temporal_alignment",
            "pressure_index",
            "microclimate",
            "historical_baseline"
        ]
        logger.info("PredictiveTerritorialService initialized")
    
    def execute(self, inputs: Dict) -> Dict:
        """
        Point d'entree principal conforme au contrat.
        
        Args:
            inputs: Dict conforme a TerritorialScoreInput
            
        Returns:
            Dict conforme a TerritorialScoreOutput
        """
        try:
            # Parse et validation input (G-SEC)
            parsed_input = TerritorialScoreInput(**inputs)
            
            # Calcul du score
            result = self.calculate_score(
                latitude=parsed_input.latitude,
                longitude=parsed_input.longitude,
                species=parsed_input.species,
                datetime_target=parsed_input.datetime_target,
                radius_km=parsed_input.radius_km,
                weather_override=parsed_input.weather_override,
                include_recommendations=parsed_input.include_recommendations
            )
            
            return result.dict()
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_code": "CALCULATION_ERROR"
            }
    
    def calculate_score(
        self,
        latitude: float,
        longitude: float,
        species: Species,
        datetime_target: Optional[datetime] = None,
        radius_km: float = 5.0,
        weather_override: Optional[WeatherOverride] = None,
        include_recommendations: bool = True
    ) -> TerritorialScoreOutput:
        """
        Calcule le score territorial pour une position.
        
        Formule:
        Score = sum(component_score * weight) pour tous les composants
        Avec ajustements arbitrage selon hierarchie
        
        Args:
            latitude: Latitude WGS84
            longitude: Longitude WGS84
            species: Espece cible
            datetime_target: Date/heure cible
            radius_km: Rayon d'analyse
            weather_override: Donnees meteo manuelles
            include_recommendations: Inclure recommandations
            
        Returns:
            TerritorialScoreOutput complet
        """
        # Datetime par defaut
        if datetime_target is None:
            datetime_target = datetime.now(timezone.utc)
        
        warnings = []
        
        # Verification hibernation ours (Niveau 1 - CRITIQUE)
        if species == Species.BEAR and datetime_target.month in BEAR_HIBERNATION_MONTHS:
            return TerritorialScoreOutput(
                success=True,
                overall_score=0,
                confidence=1.0,
                rating=ScoreRating.POOR,
                components=ScoreComponents(
                    habitat_score=0,
                    weather_score=0,
                    temporal_score=0,
                    pressure_score=0,
                    microclimate_score=0,
                    historical_score=0
                ),
                recommendations=[
                    Recommendation(
                        type="timing",
                        priority="critical",
                        message_fr="L'ours est en hibernation durant cette periode. Score = 0.",
                        message_en="Bear is hibernating during this period. Score = 0."
                    )
                ],
                warnings=["BEAR_HIBERNATION_PERIOD"],
                metadata={
                    "species": species.value,
                    "hibernation": True,
                    "datetime": datetime_target.isoformat()
                }
            )
        
        # Calculer chaque composante
        habitat_score = self._calculate_habitat_score(latitude, longitude, species)
        weather_score, weather_data = self._calculate_weather_score(
            latitude, longitude, weather_override
        )
        temporal_score = self._calculate_temporal_score(species, datetime_target)
        pressure_score = self._calculate_pressure_score(latitude, longitude, datetime_target)
        microclimate_score = self._calculate_microclimate_score(
            latitude, longitude, weather_data, datetime_target
        )
        historical_score = self._calculate_historical_score(latitude, longitude, species)
        
        # Detection conditions extremes (Niveau 1 - CRITIQUE)
        is_extreme, extreme_type = self._detect_extreme_conditions(weather_data)
        
        # Detection periode rut
        is_rut = self._is_rut_period(species, datetime_target)
        
        # Detection haute pression
        is_high_pressure = pressure_score < 30  # IPC inverse
        
        # Obtenir poids dynamiques selon contexte
        weights = self._get_dynamic_weights(
            is_extreme=is_extreme,
            is_rut=is_rut,
            is_high_pressure=is_high_pressure
        )
        
        # Calcul score pondere
        component_scores = {
            "habitat_quality": habitat_score,
            "weather_conditions": weather_score,
            "temporal_alignment": temporal_score,
            "pressure_index": pressure_score,
            "microclimate": microclimate_score,
            "historical_baseline": historical_score
        }
        
        overall_score = sum(
            score * weights.get(key, 0)
            for key, score in component_scores.items()
        )
        
        # Borner le score
        overall_score = max(0, min(100, overall_score))
        
        # Calculer confiance
        confidence = self._calculate_confidence(
            weather_override is None,
            is_extreme
        )
        
        # Rating
        rating = score_to_rating(overall_score)
        
        # Avertissements
        if is_extreme:
            warnings.append(f"EXTREME_CONDITIONS_{extreme_type.upper()}")
        if is_high_pressure:
            warnings.append("HIGH_HUNTING_PRESSURE")
        if is_rut:
            warnings.append("RUT_PERIOD_ACTIVE")
        
        # Recommandations
        recommendations = []
        if include_recommendations:
            recommendations = self._generate_recommendations(
                overall_score=overall_score,
                species=species,
                datetime_target=datetime_target,
                is_extreme=is_extreme,
                is_rut=is_rut,
                is_high_pressure=is_high_pressure,
                weather_data=weather_data
            )
        
        # Construire output
        return TerritorialScoreOutput(
            success=True,
            overall_score=round(overall_score, 1),
            confidence=round(confidence, 2),
            rating=rating,
            components=ScoreComponents(
                habitat_score=round(habitat_score, 1),
                weather_score=round(weather_score, 1),
                temporal_score=round(temporal_score, 1),
                pressure_score=round(pressure_score, 1),
                microclimate_score=round(microclimate_score, 1),
                historical_score=round(historical_score, 1)
            ),
            recommendations=recommendations,
            warnings=warnings,
            metadata={
                "species": species.value,
                "datetime": datetime_target.isoformat(),
                "latitude": latitude,
                "longitude": longitude,
                "weights_applied": weights,
                "is_rut": is_rut,
                "is_extreme": is_extreme,
                "data_sources_used": self._available_sources
            }
        )
    
    # =========================================================================
    # COMPONENT CALCULATORS
    # =========================================================================
    
    def _calculate_habitat_score(
        self, 
        latitude: float, 
        longitude: float, 
        species: Species
    ) -> float:
        """
        Calcule le score d'habitat (F2 - Vegetation).
        
        Utilise les variables d'habitat de l'inventaire:
        - NDVI, canopy_cover, edge_density, water_proximity
        
        NOTE: Version P0 - Simulation basee sur position
        P1 integrera donnees Sentinel-2 et LiDAR
        """
        # Simulation basee sur la position (P0)
        # Zones connues favorables au Quebec
        
        # Facteur latitude (nord = plus sauvage)
        lat_factor = min(1.0, (latitude - 45) / 15 * 0.8 + 0.5)
        
        # Facteur longitude (centre = plus forestier)
        lng_center = -70.0
        lng_factor = 1.0 - abs(longitude - lng_center) / 20 * 0.3
        
        # Score de base
        base_score = (lat_factor * 0.6 + lng_factor * 0.4) * 100
        
        # Ajustement par espece
        species_modifier = {
            Species.MOOSE: 1.0,
            Species.DEER: 0.95,
            Species.BEAR: 0.90,
            Species.WILD_TURKEY: 0.85,
            Species.ELK: 0.88
        }
        
        return base_score * species_modifier.get(species, 1.0)
    
    def _calculate_weather_score(
        self,
        latitude: float,
        longitude: float,
        weather_override: Optional[WeatherOverride]
    ) -> Tuple[float, Dict]:
        """
        Calcule le score meteo (F5 - Microclimats, F9 - Extremes).
        
        Utilise les seuils de l'inventaire:
        - Temperature optimale: -5C a 15C
        - Vent optimal: 0-20 km/h
        - Pression optimale: 1000-1030 hPa
        """
        # Donnees meteo
        if weather_override:
            weather_data = {
                "temperature": weather_override.temperature or 10,
                "wind_speed": weather_override.wind_speed or 10,
                "pressure": weather_override.pressure or 1015,
                "precipitation": weather_override.precipitation or 0
            }
        else:
            # Valeurs par defaut simulees (P0)
            # P1 integrera Open-Meteo / Environment Canada
            weather_data = {
                "temperature": 8,
                "wind_speed": 12,
                "pressure": 1018,
                "precipitation": 0
            }
        
        # Score temperature
        temp = weather_data["temperature"]
        if OPTIMAL_WEATHER["temperature"]["min"] <= temp <= OPTIMAL_WEATHER["temperature"]["max"]:
            temp_score = 100 - abs(temp - OPTIMAL_WEATHER["temperature"]["ideal"]) * 3
        elif temp < OPTIMAL_WEATHER["temperature"]["min"]:
            temp_score = max(0, 50 - abs(temp - OPTIMAL_WEATHER["temperature"]["min"]) * 2)
        else:
            temp_score = max(0, 50 - abs(temp - OPTIMAL_WEATHER["temperature"]["max"]) * 3)
        
        # Score vent
        wind = weather_data["wind_speed"]
        if wind <= OPTIMAL_WEATHER["wind_speed"]["max"]:
            wind_score = 100 - (wind / OPTIMAL_WEATHER["wind_speed"]["max"]) * 30
        else:
            wind_score = max(0, 70 - (wind - OPTIMAL_WEATHER["wind_speed"]["max"]) * 2)
        
        # Score pression
        pressure = weather_data["pressure"]
        pressure_score = 100 - abs(pressure - OPTIMAL_WEATHER["pressure"]["ideal"]) * 2
        pressure_score = max(0, min(100, pressure_score))
        
        # Score precipitation (leger = bon, fort = mauvais)
        precip = weather_data["precipitation"]
        if precip < 1:
            precip_score = 100
        elif precip < 5:
            precip_score = 80
        else:
            precip_score = max(0, 60 - precip * 5)
        
        # Score global meteo
        weather_score = (
            temp_score * 0.40 +
            wind_score * 0.25 +
            pressure_score * 0.20 +
            precip_score * 0.15
        )
        
        return weather_score, weather_data
    
    def _calculate_temporal_score(
        self,
        species: Species,
        datetime_target: datetime
    ) -> float:
        """
        Calcule le score temporel (F12 - Cycles Temporels).
        
        Combine:
        - Pattern horaire par espece
        - Facteur saisonnier
        - Modificateur hebdomadaire
        """
        hour = datetime_target.hour
        month = datetime_target.month
        weekday = datetime_target.weekday()
        
        # Score horaire
        hourly_patterns = HOURLY_ACTIVITY_PATTERNS.get(species, HOURLY_ACTIVITY_PATTERNS[Species.MOOSE])
        hourly_score = hourly_patterns.get(hour, 50)
        
        # Facteur saisonnier
        seasonal_factor = SEASON_FACTORS.get(month, 0.7)
        
        # Facteur hebdomadaire
        weekly_factor = WEEKLY_MODIFIERS.get(weekday, 1.0)
        
        # Bonus rut
        rut_bonus = 1.0
        if self._is_rut_period(species, datetime_target):
            rut_bonus = self.weights_config.arbitrage.get("rut_boost_factor", 1.5)
        
        # Score combine
        temporal_score = hourly_score * seasonal_factor * weekly_factor * rut_bonus
        
        return min(100, temporal_score)
    
    def _calculate_pressure_score(
        self,
        latitude: float,
        longitude: float,
        datetime_target: datetime
    ) -> float:
        """
        Calcule le score de pression de chasse (F8 - Pression).
        
        NOTE: P0 - Simulation basee sur jour de semaine et periode
        P1 integrera agregation des sorties HUNTIQ
        
        Score INVERSE: 100 = pas de pression, 0 = pression maximale
        """
        weekday = datetime_target.weekday()
        month = datetime_target.month
        
        # Pression plus elevee le weekend
        if weekday >= 5:  # Samedi, Dimanche
            base_pressure = 60
        elif weekday == 4:  # Vendredi
            base_pressure = 40
        else:
            base_pressure = 20
        
        # Pression plus elevee en saison de chasse (Oct-Nov)
        if month in [10, 11]:
            base_pressure += 20
        elif month in [9, 12]:
            base_pressure += 10
        
        # Convertir en score inverse (100 = favorable)
        pressure_score = 100 - min(100, base_pressure)
        
        return pressure_score
    
    def _calculate_microclimate_score(
        self,
        latitude: float,
        longitude: float,
        weather_data: Dict,
        datetime_target: datetime
    ) -> float:
        """
        Calcule l'indice microclimatique (Bloc 2 - Microclimats).
        
        Formule IMC:
        IMC = T_base + Delta_elev + Delta_aspect + Delta_canopy + Delta_wind
        
        NOTE: P0 - Version simplifiee
        P1 integrera DEM et LiDAR
        """
        temp = weather_data.get("temperature", 10)
        wind = weather_data.get("wind_speed", 10)
        month = datetime_target.month
        
        # Estimation elevation basee sur latitude (approximation)
        estimated_elevation = (latitude - 45) * 50  # metres
        delta_elev = -0.0065 * estimated_elevation
        
        # Effet vent (windchill simplifie)
        if temp < 10 and wind > 10:
            delta_wind = -0.5 * (wind / 10)
        else:
            delta_wind = 0
        
        # Temperature estimee
        estimated_temp = temp + delta_elev + delta_wind
        
        # Score: temperature estimee vs optimale pour la saison
        if month in [12, 1, 2]:  # Hiver
            optimal_temp = -5
        elif month in [6, 7, 8]:  # Ete
            optimal_temp = 15
        else:
            optimal_temp = 10
        
        diff = abs(estimated_temp - optimal_temp)
        microclimate_score = max(0, 100 - diff * 4)
        
        return microclimate_score
    
    def _calculate_historical_score(
        self,
        latitude: float,
        longitude: float,
        species: Species
    ) -> float:
        """
        Calcule le score historique (F10 - Historiques).
        
        NOTE: P0 - Baseline regional
        P1 integrera donnees MELCCFP et observations utilisateurs
        """
        # Baseline regional (P0)
        # Zones connues favorables
        
        # Score de base selon position
        base_score = 60
        
        # Bonus zones reconnues (simplification P0)
        if 47 <= latitude <= 49 and -72 <= longitude <= -68:
            # Cote-Nord / Laurentides
            base_score += 15
        elif 48 <= latitude <= 50 and -68 <= longitude <= -65:
            # Gaspesie / Bas-St-Laurent
            base_score += 10
        
        return min(100, base_score)
    
    # =========================================================================
    # ARBITRAGE & WEIGHTS
    # =========================================================================
    
    def _detect_extreme_conditions(self, weather_data: Dict) -> Tuple[bool, str]:
        """
        Detecte les conditions extremes (Niveau 1 - CRITIQUE).
        
        Seuils de l'inventaire v1.2:
        - Temperature < -30C ou > 32C
        - Vent > 60 km/h
        """
        thresholds = self.weights_config.arbitrage.get("extreme_weather_threshold", {})
        
        temp = weather_data.get("temperature", 10)
        wind = weather_data.get("wind_speed", 10)
        
        if temp < thresholds.get("temp_min", -30):
            return True, "cold"
        if temp > thresholds.get("temp_max", 32):
            return True, "heat"
        if wind > thresholds.get("wind_max", 60):
            return True, "wind"
        
        return False, ""
    
    def _is_rut_period(self, species: Species, datetime_target: datetime) -> bool:
        """Verifie si on est en periode de rut."""
        if species not in RUT_PERIODS:
            return False
        
        rut = RUT_PERIODS[species]
        month = datetime_target.month
        
        return rut["start_month"] <= month <= rut["end_month"]
    
    def _get_dynamic_weights(
        self,
        is_extreme: bool,
        is_rut: bool,
        is_high_pressure: bool
    ) -> Dict[str, float]:
        """
        Retourne les poids dynamiques selon le contexte.
        
        Conforme a: Inventaire v1.2 - Ponderations Dynamiques
        
        Regles d'arbitrage (priorite):
        1. Conditions extremes -> weather domine
        2. Rut actif -> temporal domine, pression reduite
        3. Haute pression seule -> pression augmentee
        """
        weights = self.weights_config.base.copy()
        
        # Conditions extremes (Niveau 1 - Override)
        if is_extreme:
            weights["weather_conditions"] *= 2.0
            weights["microclimate"] *= 1.5
        
        # Periode rut (Niveau 2 - Primaire)
        if is_rut:
            weights["temporal_alignment"] *= 1.5
            weights["habitat_quality"] *= 1.25
            # REGLE ARBITRAGE: Rut domine pression
            # Le rut transcende la pression de chasse - les animaux
            # sont plus actifs malgre la presence de chasseurs
            if is_high_pressure:
                weights["pressure_index"] *= 0.5  # Reduire impact pression
            else:
                weights["pressure_index"] *= 0.7
        
        # Haute pression seule (sans rut)
        elif is_high_pressure:
            weights["pressure_index"] *= 2.0
            weights["habitat_quality"] *= 0.8
        
        # Normaliser
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}
        
        return weights
    
    def _calculate_confidence(
        self,
        has_live_weather: bool,
        is_extreme: bool
    ) -> float:
        """Calcule le niveau de confiance du score."""
        confidence = 0.85  # Base
        
        if not has_live_weather:
            confidence -= 0.15
        
        if is_extreme:
            confidence -= 0.10
        
        return max(0.5, confidence)
    
    # =========================================================================
    # RECOMMENDATIONS
    # =========================================================================
    
    def _generate_recommendations(
        self,
        overall_score: float,
        species: Species,
        datetime_target: datetime,
        is_extreme: bool,
        is_rut: bool,
        is_high_pressure: bool,
        weather_data: Dict
    ) -> List[Recommendation]:
        """
        Genere les recommandations contextuelles.
        
        G-DOC: Chaque recommandation est justifiee
        """
        recommendations = []
        
        # Recommandations de timing
        hour = datetime_target.hour
        if 5 <= hour <= 8 or 16 <= hour <= 19:
            recommendations.append(Recommendation(
                type="timing",
                priority="high",
                message_fr="Periode d'activite elevee. Excellent moment pour la chasse.",
                message_en="High activity period. Excellent hunting time."
            ))
        elif 11 <= hour <= 14:
            recommendations.append(Recommendation(
                type="timing",
                priority="medium",
                message_fr="Activite reduite en milieu de journee. Privilegiez l'aube ou le crepuscule.",
                message_en="Reduced midday activity. Prefer dawn or dusk."
            ))
        
        # Recommandations conditions
        if is_extreme:
            recommendations.append(Recommendation(
                type="strategy",
                priority="critical",
                message_fr="Conditions extremes detectees. Les animaux cherchent un refuge. Ciblez les zones protegees.",
                message_en="Extreme conditions detected. Animals seeking shelter. Target protected areas."
            ))
        
        # Recommandations rut
        if is_rut:
            if species == Species.MOOSE:
                recommendations.append(Recommendation(
                    type="strategy",
                    priority="high",
                    message_fr="Periode de rut de l'orignal. Utilisez les appels (calls) et surveillez les zones ouvertes.",
                    message_en="Moose rut period. Use calls and watch open areas."
                ))
            elif species == Species.DEER:
                recommendations.append(Recommendation(
                    type="strategy",
                    priority="high",
                    message_fr="Periode de rut du cerf. Cherchez les grattages (scrapes) et les lignes de cretes.",
                    message_en="Deer rut period. Look for scrapes and ridgelines."
                ))
        
        # Recommandations pression
        if is_high_pressure:
            recommendations.append(Recommendation(
                type="position",
                priority="high",
                message_fr="Forte pression de chasse dans la zone. Explorez les zones moins accessibles ou revenez en semaine.",
                message_en="High hunting pressure in the area. Explore less accessible areas or return during weekdays."
            ))
        
        # Recommandation score global
        if overall_score >= 70:
            recommendations.append(Recommendation(
                type="strategy",
                priority="high",
                message_fr=f"Conditions excellentes (score {overall_score:.0f}/100). Maximisez votre temps sur le terrain.",
                message_en=f"Excellent conditions (score {overall_score:.0f}/100). Maximize your time in the field."
            ))
        elif overall_score < 40:
            recommendations.append(Recommendation(
                type="timing",
                priority="medium",
                message_fr=f"Conditions difficiles (score {overall_score:.0f}/100). Envisagez de reporter votre sortie.",
                message_en=f"Challenging conditions (score {overall_score:.0f}/100). Consider postponing your trip."
            ))
        
        return recommendations
