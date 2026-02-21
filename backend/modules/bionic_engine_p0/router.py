"""
BIONIC ENGINE - API Router
PHASE G - P0 IMPLEMENTATION
Version: 1.0.0-alpha

Routes API pour les modules P0 du moteur BIONIC.
Prefixe: /api/v1/bionic/

Conformite: G-SEC | G-QA | G-DOC
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import logging

from modules.bionic_engine.modules.predictive_territorial import PredictiveTerritorialService
from modules.bionic_engine.modules.behavioral_models import BehavioralModelsService
from modules.bionic_engine.contracts.data_contracts import (
    Species,
    TerritorialScoreInput,
    BehavioralPredictionInput
)
from modules.bionic_engine.core import get_engine

logger = logging.getLogger("bionic_engine.router")

# Router principal
router = APIRouter(prefix="/v1/bionic", tags=["BIONIC Engine P0"])

# Instances des services
_pt_service = PredictiveTerritorialService()
_bm_service = BehavioralModelsService()


# =============================================================================
# HEALTH & STATUS
# =============================================================================

@router.get("/health")
async def bionic_health():
    """
    Verification sante du moteur BIONIC.
    
    G-QA: Monitoring endpoint
    """
    engine = get_engine()
    return engine.health_check()


@router.get("/modules")
async def list_modules():
    """
    Liste les modules enregistres.
    
    G-DOC: Documentation des modules actifs
    """
    return {
        "modules": [
            {
                "id": "predictive_territorial",
                "phase": "P0",
                "status": "active",
                "endpoint": "/api/v1/bionic/territorial/score"
            },
            {
                "id": "behavioral_models",
                "phase": "P0",
                "status": "active",
                "endpoint": "/api/v1/bionic/behavioral/predict"
            }
        ],
        "phase": "P0",
        "version": "1.0.0-alpha"
    }


# =============================================================================
# PREDICTIVE TERRITORIAL ENDPOINTS
# =============================================================================

@router.post("/territorial/score")
async def calculate_territorial_score(request: TerritorialScoreInput):
    """
    Calcule le score territorial predictif.
    
    Conforme a: predictive_territorial_contract.json
    
    Args:
        request: TerritorialScoreInput conforme au contrat
        
    Returns:
        TerritorialScoreOutput avec score 0-100 et recommandations
    
    G-SEC: Validation automatique via Pydantic
    G-QA: P95 < 500ms
    """
    try:
        result = _pt_service.calculate_score(
            latitude=request.latitude,
            longitude=request.longitude,
            species=request.species,
            datetime_target=request.datetime_target,
            radius_km=request.radius_km,
            weather_override=request.weather_override,
            include_recommendations=request.include_recommendations
        )
        
        return result.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Territorial score error: {e}")
        raise HTTPException(status_code=500, detail="Calculation error")


@router.get("/territorial/score")
async def calculate_territorial_score_get(
    latitude: float = Query(..., ge=45.0, le=62.0),
    longitude: float = Query(..., ge=-80.0, le=-57.0),
    species: str = Query(default="moose"),
    datetime_str: Optional[str] = Query(default=None, alias="datetime"),
    radius_km: float = Query(default=5.0, ge=0.5, le=25.0)
):
    """
    Calcule le score territorial (version GET simplifiee).
    
    G-DOC: Endpoint simplifie pour tests rapides
    """
    try:
        # Parse species
        species_enum = Species(species)
        
        # Parse datetime
        dt = None
        if datetime_str:
            dt = datetime.fromisoformat(datetime_str)
        
        result = _pt_service.calculate_score(
            latitude=latitude,
            longitude=longitude,
            species=species_enum,
            datetime_target=dt,
            radius_km=radius_km,
            include_recommendations=True
        )
        
        return result.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Territorial score error: {e}")
        raise HTTPException(status_code=500, detail="Calculation error")


# =============================================================================
# BEHAVIORAL MODELS ENDPOINTS
# =============================================================================

@router.post("/behavioral/predict")
async def predict_behavior(request: BehavioralPredictionInput):
    """
    Prediction comportementale complete.
    
    Conforme a: behavioral_models_contract.json
    
    Args:
        request: BehavioralPredictionInput conforme au contrat
        
    Returns:
        BehavioralPredictionOutput avec activite, timeline, strategies
    
    G-SEC: Validation automatique via Pydantic
    G-QA: P95 < 300ms
    """
    try:
        result = _bm_service.predict_behavior(
            species=request.species,
            datetime_target=request.datetime_target,
            latitude=request.latitude,
            longitude=request.longitude,
            weather_context=request.weather_context,
            include_strategy=request.include_strategy
        )
        
        return result.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Behavioral prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")


@router.get("/behavioral/activity")
async def get_current_activity(
    species: str = Query(...),
    datetime_str: Optional[str] = Query(default=None, alias="datetime")
):
    """
    Obtient le niveau d'activite actuel (endpoint simplifie).
    
    G-DOC: Pour integration rapide
    """
    try:
        species_enum = Species(species)
        dt = None
        if datetime_str:
            dt = datetime.fromisoformat(datetime_str)
        
        result = _bm_service.predict_activity(
            species=species_enum,
            datetime_target=dt or datetime.now()
        )
        
        return result.dict()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Activity error: {e}")
        raise HTTPException(status_code=500, detail="Error")


@router.get("/behavioral/timeline")
async def get_activity_timeline(
    species: str = Query(...),
    date: Optional[str] = Query(default=None)
):
    """
    Obtient la timeline d'activite 24h.
    
    G-DOC: 24 entrees, une par heure
    """
    try:
        species_enum = Species(species)
        dt = datetime.now()
        if date:
            dt = datetime.fromisoformat(date)
        
        timeline = _bm_service.get_activity_timeline(
            species=species_enum,
            date=dt
        )
        
        return {
            "species": species,
            "date": dt.date().isoformat(),
            "timeline": [entry.dict() for entry in timeline]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Timeline error: {e}")
        raise HTTPException(status_code=500, detail="Error")


# =============================================================================
# COMBINED ENDPOINTS
# =============================================================================

@router.get("/analysis")
async def combined_analysis(
    latitude: float = Query(..., ge=45.0, le=62.0),
    longitude: float = Query(..., ge=-80.0, le=-57.0),
    species: str = Query(default="moose"),
    datetime_str: Optional[str] = Query(default=None, alias="datetime")
):
    """
    Analyse combinee: territorial + behavioral.
    
    Retourne les deux analyses en un seul appel.
    
    G-QA: Optimisation pour frontend
    """
    try:
        species_enum = Species(species)
        dt = None
        if datetime_str:
            dt = datetime.fromisoformat(datetime_str)
        
        # Score territorial
        territorial = _pt_service.calculate_score(
            latitude=latitude,
            longitude=longitude,
            species=species_enum,
            datetime_target=dt,
            include_recommendations=True
        )
        
        # Prediction comportementale
        behavioral = _bm_service.predict_behavior(
            species=species_enum,
            datetime_target=dt,
            latitude=latitude,
            longitude=longitude,
            include_strategy=True
        )
        
        return {
            "success": True,
            "territorial": territorial.dict(),
            "behavioral": behavioral.dict(),
            "combined_score": round(
                (territorial.overall_score * 0.5 + behavioral.activity.activity_score * 0.5),
                1
            ),
            "metadata": {
                "species": species,
                "latitude": latitude,
                "longitude": longitude,
                "datetime": (dt or datetime.now()).isoformat()
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Combined analysis error: {e}")
        raise HTTPException(status_code=500, detail="Analysis error")
