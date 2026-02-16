"""
Formations Engine Router
API pour les formations FédéCP et BIONIC Academy
"""

from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/formations", tags=["formations"])

# ==================== MODELS ====================

class Formation(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    duration: str
    type: str
    topics: Optional[List[str]] = None
    modules: Optional[List[str]] = None
    link: Optional[str] = None
    available: bool = True

# ==================== DONNÉES STATIQUES ====================

FEDECP_FORMATIONS = [
    {
        "id": "securite",
        "title": "Sécurité à la chasse",
        "description": "Cours obligatoire pour l'obtention du permis de chasse au Québec.",
        "icon": "🛡️",
        "duration": "8 heures",
        "type": "Obligatoire",
        "link": "https://fedecp.com/la-chasse/japprends/initiation-des-chasseurs/",
        "topics": ["Maniement sécuritaire des armes", "Règles de sécurité", "Éthique du chasseur", "Réglementation"]
    },
    {
        "id": "piegeage",
        "title": "Formation au piégeage",
        "description": "Techniques de piégeage responsable et réglementation.",
        "icon": "🪤",
        "duration": "6 heures",
        "type": "Spécialisé",
        "link": "https://fedecp.com/la-chasse/japprends/initiation-des-chasseurs/",
        "topics": ["Types de pièges", "Espèces ciblées", "Réglementation", "Éthique"]
    },
    {
        "id": "arbalete",
        "title": "Formation arbalète",
        "description": "Utilisation sécuritaire de l'arbalète pour la chasse.",
        "icon": "🏹",
        "duration": "4 heures",
        "type": "Spécialisé",
        "link": "https://fedecp.com/la-chasse/japprends/initiation-des-chasseurs/",
        "topics": ["Équipement", "Technique de tir", "Sécurité", "Réglementation"]
    },
    {
        "id": "terres-privees",
        "title": "Accès aux terres privées",
        "description": "Bonnes pratiques et ententes chasseur/propriétaire.",
        "icon": "🏠",
        "duration": "2 heures",
        "type": "Recommandé",
        "link": "https://fedecp.com/la-chasse/je-pratique/ou-chasser/",
        "topics": ["Demande d'autorisation", "Respect des propriétés", "Ententes écrites", "Assurances"]
    }
]

BIONIC_FORMATIONS = [
    {
        "id": "analyse-territoire",
        "title": "Analyse de territoire BIONIC™",
        "description": "Maîtrisez les outils d'analyse géospatiale pour optimiser vos chasses.",
        "icon": "🗺️",
        "duration": "3 heures",
        "type": "BIONIC™",
        "available": False,
        "modules": [
            "Lecture des heatmaps d'activité",
            "Interprétation des zones de probabilité",
            "Utilisation des couches WMS",
            "Analyse par espèce"
        ]
    },
    {
        "id": "parcours-guide",
        "title": "Parcours guidé optimisé",
        "description": "Apprenez à créer et suivre des parcours de chasse intelligents.",
        "icon": "🧭",
        "duration": "2 heures",
        "type": "BIONIC™",
        "available": False,
        "modules": [
            "Création de waypoints stratégiques",
            "Génération de parcours optimisés",
            "Interprétation des probabilités",
            "Navigation GPS terrain"
        ]
    },
    {
        "id": "attractants",
        "title": "Science des attractants",
        "description": "Comprendre la composition et l'utilisation des produits BIONIC™.",
        "icon": "🧪",
        "duration": "2 heures",
        "type": "BIONIC™",
        "available": False,
        "modules": [
            "Types d'attractants par espèce",
            "Analyse nutritionnelle du gibier",
            "Placement stratégique",
            "Saisons et timing"
        ]
    }
]

# ==================== ENDPOINTS ====================

@router.get("/fedecp")
async def get_fedecp_formations():
    """Retourne les formations FédéCP"""
    return {
        "success": True,
        "source": "FédéCP",
        "formations": FEDECP_FORMATIONS,
        "total": len(FEDECP_FORMATIONS)
    }

@router.get("/bionic")
async def get_bionic_formations():
    """Retourne les formations BIONIC Academy"""
    return {
        "success": True,
        "source": "BIONIC Academy",
        "formations": BIONIC_FORMATIONS,
        "total": len(BIONIC_FORMATIONS),
        "available_soon": True
    }

@router.get("/all")
async def get_all_formations():
    """Retourne toutes les formations"""
    return {
        "success": True,
        "fedecp": FEDECP_FORMATIONS,
        "bionic": BIONIC_FORMATIONS,
        "total": len(FEDECP_FORMATIONS) + len(BIONIC_FORMATIONS)
    }

@router.get("/{formation_id}")
async def get_formation(formation_id: str):
    """Retourne une formation spécifique"""
    all_formations = FEDECP_FORMATIONS + BIONIC_FORMATIONS
    formation = next((f for f in all_formations if f["id"] == formation_id), None)
    if not formation:
        return {"success": False, "error": "Formation non trouvée"}
    return {"success": True, "formation": formation}
