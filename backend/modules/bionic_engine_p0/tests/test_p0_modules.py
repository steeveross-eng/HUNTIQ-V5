"""
BIONIC ENGINE - P0 Unit Tests
PHASE G - G-QA Compliance

Tests unitaires pour les modules P0:
- predictive_territorial.py
- behavioral_models.py

Conformite: Plan de Tests G-QA
"""

import pytest
from datetime import datetime, timezone
from typing import Dict

from modules.bionic_engine_p0.modules.predictive_territorial import (
    PredictiveTerritorialService,
    HOURLY_ACTIVITY_PATTERNS as PT_PATTERNS,
    SEASON_FACTORS,
    WEEKLY_MODIFIERS,
    RUT_PERIODS,
    BEAR_HIBERNATION_MONTHS
)
from modules.bionic_engine_p0.modules.behavioral_models import (
    BehavioralModelsService,
    HOURLY_ACTIVITY_PATTERNS as BM_PATTERNS,
    ANNUAL_CALENDAR,
    HUNTING_STRATEGIES
)
from modules.bionic_engine_p0.contracts.data_contracts import (
    Species,
    ScoreRating,
    ActivityLevel,
    BehaviorType,
    SeasonPhase,
    WeatherOverride,
    score_to_rating,
    score_to_activity_level,
    normalize_weights
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def pt_service():
    """Service Predictive Territorial"""
    return PredictiveTerritorialService()


@pytest.fixture
def bm_service():
    """Service Behavioral Models"""
    return BehavioralModelsService()


@pytest.fixture
def sample_coordinates():
    """Coordonnees de test (Laurentides)"""
    return {"latitude": 47.5, "longitude": -70.5}


@pytest.fixture
def optimal_hunting_datetime():
    """Date/heure optimale (octobre, 7h du matin, mardi)"""
    return datetime(2025, 10, 7, 7, 0, tzinfo=timezone.utc)


# =============================================================================
# PREDICTIVE TERRITORIAL - TESTS UNITAIRES
# =============================================================================

class TestPredictiveTerritorialBasic:
    """Tests basiques du score territorial"""
    
    def test_basic_score_calculation(self, pt_service, sample_coordinates):
        """Score basique avec toutes les donnees"""
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 7, 0, tzinfo=timezone.utc)
        )
        
        assert result.success is True
        assert 0 <= result.overall_score <= 100
        assert 0 <= result.confidence <= 1
        assert result.rating in ScoreRating
    
    def test_score_components_present(self, pt_service, sample_coordinates):
        """Verifier que toutes les composantes sont presentes"""
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE
        )
        
        components = result.components
        assert components.habitat_score is not None
        assert components.weather_score is not None
        assert components.temporal_score is not None
        assert components.pressure_score is not None
        assert components.microclimate_score is not None
        assert components.historical_score is not None
    
    def test_score_reproducibility(self, pt_service, sample_coordinates):
        """Meme input = meme output"""
        dt = datetime(2025, 10, 15, 7, 0, tzinfo=timezone.utc)
        
        result1 = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=dt
        )
        
        result2 = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=dt
        )
        
        assert result1.overall_score == result2.overall_score


class TestPredictiveTerritorialSpecies:
    """Tests par espece"""
    
    @pytest.mark.parametrize("species", [
        Species.MOOSE, Species.DEER, Species.BEAR, 
        Species.WILD_TURKEY, Species.ELK
    ])
    def test_all_species_supported(self, pt_service, sample_coordinates, species):
        """Toutes les especes produisent un score valide"""
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=species,
            datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        assert result.success is True
        assert result.overall_score is not None
    
    def test_bear_hibernation_zero_score(self, pt_service, sample_coordinates):
        """Ours en hibernation = score 0"""
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.BEAR,
            datetime_target=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        assert result.overall_score == 0
        assert "BEAR_HIBERNATION_PERIOD" in result.warnings
    
    def test_moose_rut_bonus(self, pt_service, sample_coordinates):
        """Orignal en rut = facteur temporel booste"""
        october = datetime(2025, 10, 5, 7, 0, tzinfo=timezone.utc)
        july = datetime(2025, 7, 15, 7, 0, tzinfo=timezone.utc)
        
        result_rut = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=october
        )
        
        result_summer = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=july
        )
        
        # Le score temporel devrait etre plus eleve en rut
        assert result_rut.components.temporal_score > result_summer.components.temporal_score
        # Et le rut devrait etre detecte
        assert result_rut.metadata.get("is_rut") is True
        assert result_summer.metadata.get("is_rut") is False


class TestPredictiveTerritorialBoundaries:
    """Tests des valeurs limites"""
    
    def test_latitude_at_boundary(self, pt_service):
        """Latitude aux limites Quebec"""
        # Limite sud
        result_south = pt_service.calculate_score(
            latitude=45.0,
            longitude=-71.0,
            species=Species.MOOSE
        )
        assert result_south.success is True
        
        # Limite nord
        result_north = pt_service.calculate_score(
            latitude=62.0,
            longitude=-71.0,
            species=Species.MOOSE
        )
        assert result_north.success is True
    
    def test_score_never_negative(self, pt_service, sample_coordinates):
        """Score jamais negatif"""
        # Pires conditions: ours en hibernation
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.BEAR,
            datetime_target=datetime(2025, 1, 15, 13, 0, tzinfo=timezone.utc)
        )
        
        assert result.overall_score >= 0
    
    def test_score_never_above_100(self, pt_service, sample_coordinates):
        """Score jamais > 100"""
        # Meilleures conditions: rut + aube
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 5, 7, 0, tzinfo=timezone.utc)
        )
        
        assert result.overall_score <= 100


class TestPredictiveTerritorialWeather:
    """Tests avec override meteo"""
    
    def test_extreme_cold(self, pt_service, sample_coordinates):
        """Temperature extreme froide"""
        weather = WeatherOverride(temperature=-35, wind_speed=10)
        
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            weather_override=weather
        )
        
        assert result.success is True
        # Conditions extremes detectees
        assert any("EXTREME" in w for w in result.warnings)
    
    def test_optimal_weather(self, pt_service, sample_coordinates):
        """Conditions meteo optimales"""
        weather = WeatherOverride(temperature=5, wind_speed=8, pressure=1015)
        
        result = pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE,
            weather_override=weather,
            datetime_target=datetime(2025, 10, 5, 7, 0, tzinfo=timezone.utc)
        )
        
        # Score meteo devrait etre eleve
        assert result.components.weather_score >= 70


# =============================================================================
# BEHAVIORAL MODELS - TESTS UNITAIRES
# =============================================================================

class TestBehavioralModelsBasic:
    """Tests basiques des modeles comportementaux"""
    
    def test_basic_prediction(self, bm_service):
        """Prediction basique"""
        result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 7, 0, tzinfo=timezone.utc)
        )
        
        assert result.success is True
        assert result.activity is not None
        assert result.timeline is not None
        assert result.seasonal_context is not None
    
    def test_activity_score_range(self, bm_service):
        """Score d'activite dans la plage 0-100"""
        result = bm_service.predict_behavior(
            species=Species.DEER,
            datetime_target=datetime(2025, 10, 15, 7, 0, tzinfo=timezone.utc)
        )
        
        assert 0 <= result.activity.activity_score <= 100
    
    def test_behavior_probabilities_sum(self, bm_service):
        """Probabilites comportements ~ 1.0"""
        result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 7, 0, tzinfo=timezone.utc)
        )
        
        probs = result.activity.behavior_probabilities
        total = sum(probs.values())
        
        assert 0.99 <= total <= 1.01


class TestBehavioralModelsTimeline:
    """Tests de la timeline 24h"""
    
    def test_timeline_complete(self, bm_service):
        """Timeline complete = 24 entrees"""
        result = bm_service.predict_behavior(
            species=Species.DEER,
            datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        assert len(result.timeline) == 24
    
    def test_timeline_hours_complete(self, bm_service):
        """Toutes les heures presentes"""
        result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        hours = [entry.hour for entry in result.timeline]
        assert sorted(hours) == list(range(24))
    
    def test_timeline_legal_hours_flagged(self, bm_service):
        """Heures legales correctement marquees"""
        result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        # 7h devrait etre legal
        hour_7 = next(e for e in result.timeline if e.hour == 7)
        assert hour_7.is_legal_hunting is True
        
        # 3h ne devrait pas etre legal
        hour_3 = next(e for e in result.timeline if e.hour == 3)
        assert hour_3.is_legal_hunting is False


class TestBehavioralModelsActivity:
    """Tests des patterns d'activite"""
    
    def test_dawn_high_activity(self, bm_service):
        """Activite elevee a l'aube"""
        result = bm_service.predict_activity(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 6, 30, tzinfo=timezone.utc)
        )
        
        assert result.activity_level in [ActivityLevel.VERY_HIGH, ActivityLevel.HIGH]
        assert result.activity_score >= 60
    
    def test_midday_low_activity(self, bm_service):
        """Activite faible en milieu de journee"""
        result = bm_service.predict_activity(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 15, 13, 0, tzinfo=timezone.utc)
        )
        
        assert result.activity_level in [ActivityLevel.LOW, ActivityLevel.MODERATE, ActivityLevel.MINIMAL]
        assert result.activity_score <= 50
    
    def test_turkey_no_night_activity(self, bm_service):
        """Dindon inactif la nuit"""
        result = bm_service.predict_activity(
            species=Species.WILD_TURKEY,
            datetime_target=datetime(2025, 10, 15, 22, 0, tzinfo=timezone.utc)
        )
        
        assert result.activity_score == 0
        assert result.current_behavior == BehaviorType.RESTING


class TestBehavioralModelsSeasons:
    """Tests des cycles saisonniers"""
    
    def test_rut_detection_moose(self, bm_service):
        """Detection du rut orignal"""
        result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=datetime(2025, 10, 5, 10, 0, tzinfo=timezone.utc)
        )
        
        assert result.seasonal_context.current_season == SeasonPhase.RUT
        assert "rut_active" in result.seasonal_context.key_events
    
    def test_bear_hibernation(self, bm_service):
        """Hibernation ours"""
        result = bm_service.predict_behavior(
            species=Species.BEAR,
            datetime_target=datetime(2025, 1, 15, 10, 0, tzinfo=timezone.utc)
        )
        
        assert result.activity.activity_score == 0
        assert "BEAR_HIBERNATION_PERIOD" in result.warnings


# =============================================================================
# DATA CONTRACTS - TESTS UNITAIRES
# =============================================================================

class TestDataContracts:
    """Tests des contrats de donnees"""
    
    def test_score_to_rating_exceptional(self):
        """Score 85+ = exceptional"""
        assert score_to_rating(90) == ScoreRating.EXCEPTIONAL
        assert score_to_rating(85) == ScoreRating.EXCEPTIONAL
    
    def test_score_to_rating_poor(self):
        """Score < 25 = poor"""
        assert score_to_rating(20) == ScoreRating.POOR
        assert score_to_rating(0) == ScoreRating.POOR
    
    def test_score_to_activity_level(self):
        """Conversion score vers niveau d'activite"""
        assert score_to_activity_level(85) == ActivityLevel.VERY_HIGH
        assert score_to_activity_level(65) == ActivityLevel.HIGH
        assert score_to_activity_level(45) == ActivityLevel.MODERATE
        assert score_to_activity_level(25) == ActivityLevel.LOW
        assert score_to_activity_level(10) == ActivityLevel.MINIMAL
    
    def test_normalize_weights_sum_to_one(self):
        """Poids normalises somment a 1"""
        weights = {"a": 0.3, "b": 0.5, "c": 0.2}
        available = ["a", "b", "c"]
        
        normalized = normalize_weights(weights, available)
        
        assert abs(sum(normalized.values()) - 1.0) < 0.01
    
    def test_normalize_weights_missing_source(self):
        """Redistribution avec source manquante"""
        weights = {"a": 0.3, "b": 0.5, "c": 0.2}
        available = ["a", "b"]  # c manquant
        
        normalized = normalize_weights(weights, available)
        
        assert "c" not in normalized
        assert abs(sum(normalized.values()) - 1.0) < 0.01


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestModuleIntegration:
    """Tests d'integration entre modules"""
    
    def test_consistent_species_data(self, pt_service, bm_service):
        """Donnees especes coherentes entre modules"""
        # Les deux modules devraient supporter les memes especes
        for species in [Species.MOOSE, Species.DEER, Species.BEAR]:
            pt_result = pt_service.calculate_score(
                latitude=47.5, longitude=-70.5,
                species=species,
                datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
            )
            
            bm_result = bm_service.predict_behavior(
                species=species,
                datetime_target=datetime(2025, 10, 15, 10, 0, tzinfo=timezone.utc)
            )
            
            assert pt_result.success is True
            assert bm_result.success is True
    
    def test_rut_detection_consistent(self, pt_service, bm_service):
        """Detection du rut coherente entre modules"""
        dt = datetime(2025, 10, 10, 7, 0, tzinfo=timezone.utc)
        
        pt_result = pt_service.calculate_score(
            latitude=47.5, longitude=-70.5,
            species=Species.MOOSE,
            datetime_target=dt
        )
        
        bm_result = bm_service.predict_behavior(
            species=Species.MOOSE,
            datetime_target=dt
        )
        
        # Les deux devraient detecter le rut
        pt_is_rut = pt_result.metadata.get("is_rut", False)
        bm_is_rut = bm_result.seasonal_context.current_season == SeasonPhase.RUT
        
        assert pt_is_rut == bm_is_rut


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Tests de performance"""
    
    def test_territorial_response_time(self, pt_service, sample_coordinates):
        """Temps de reponse PT < 100ms"""
        import time
        
        start = time.time()
        pt_service.calculate_score(
            latitude=sample_coordinates["latitude"],
            longitude=sample_coordinates["longitude"],
            species=Species.MOOSE
        )
        elapsed = (time.time() - start) * 1000
        
        assert elapsed < 100  # < 100ms
    
    def test_behavioral_response_time(self, bm_service):
        """Temps de reponse BM < 100ms"""
        import time
        
        start = time.time()
        bm_service.predict_behavior(
            species=Species.DEER,
            datetime_target=datetime.now(timezone.utc)
        )
        elapsed = (time.time() - start) * 1000
        
        assert elapsed < 100  # < 100ms


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
