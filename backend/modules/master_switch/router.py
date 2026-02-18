"""
BIONIC Master Switch - X300% Strategy
======================================

Contrôle global ON/OFF pour:
- Captation (Contact Engine)
- Enrichissement (Identity Graph)
- Triggers (Marketing Trigger Engine)
- Scoring (Lead Scoring)
- SEO Engine

Architecture LEGO V5 - Module isolé.
"""

from fastapi import APIRouter, Body
from typing import Dict, Any
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/master-switch", tags=["Master Switch X300%"])

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'bionic_db')

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db


# Default switch states
DEFAULT_SWITCHES = {
    "global": {
        "name": "Master Switch Global",
        "description": "Contrôle global de tous les modules X300%",
        "is_active": True,
        "icon": "🔌"
    },
    "captation": {
        "name": "Captation",
        "description": "Tracking des visiteurs, publicités, interactions sociales",
        "is_active": True,
        "icon": "📡"
    },
    "enrichment": {
        "name": "Enrichissement",
        "description": "Identity Graph et fusion des profils",
        "is_active": True,
        "icon": "🔗"
    },
    "triggers": {
        "name": "Triggers Marketing",
        "description": "Déclencheurs automatiques et séquences",
        "is_active": True,
        "icon": "⚡"
    },
    "scoring": {
        "name": "Lead Scoring",
        "description": "Calcul automatique des scores de contact",
        "is_active": True,
        "icon": "📊"
    },
    "seo": {
        "name": "SEO Engine",
        "description": "Optimisation et génération de contenu SEO",
        "is_active": True,
        "icon": "🔍"
    },
    "marketing_calendar": {
        "name": "Marketing Calendar",
        "description": "Calendrier et planification des campagnes",
        "is_active": True,
        "icon": "📅"
    },
    "consent_layer": {
        "name": "Consent Layer",
        "description": "Gestion du consentement utilisateur",
        "is_active": True,
        "icon": "🛡️"
    }
}


@router.get("/status")
async def get_all_switches():
    """
    Récupère l'état de tous les switches.
    """
    db = get_db()
    
    # Check if switches exist
    switches_doc = await db.master_switches.find_one({"_type": "switches"})
    
    if not switches_doc:
        # Initialize with defaults
        switches_doc = {
            "_type": "switches",
            "switches": DEFAULT_SWITCHES,
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "updated_by": "system"
        }
        await db.master_switches.insert_one(switches_doc)
    
    switches = switches_doc.get("switches", DEFAULT_SWITCHES)
    
    # Check if global is OFF - all others should be OFF too
    if not switches.get("global", {}).get("is_active", True):
        for key in switches:
            if key != "global":
                switches[key]["effective_state"] = False
    else:
        for key in switches:
            switches[key]["effective_state"] = switches[key].get("is_active", True)
    
    active_count = sum(1 for s in switches.values() if s.get("effective_state", True))
    
    return {
        "success": True,
        "switches": switches,
        "summary": {
            "total": len(switches),
            "active": active_count,
            "inactive": len(switches) - active_count,
            "global_state": switches.get("global", {}).get("is_active", True)
        },
        "last_updated": switches_doc.get("last_updated")
    }


@router.post("/toggle/{switch_id}")
async def toggle_switch(switch_id: str, is_active: bool = Body(..., embed=True)):
    """
    Bascule l'état d'un switch spécifique.
    Si le switch global est désactivé, tous les autres sont désactivés.
    """
    db = get_db()
    
    switches_doc = await db.master_switches.find_one({"_type": "switches"})
    
    if not switches_doc:
        return {"success": False, "error": "Configuration non trouvée"}
    
    switches = switches_doc.get("switches", {})
    
    if switch_id not in switches:
        return {"success": False, "error": f"Switch '{switch_id}' non trouvé"}
    
    # Update the switch
    switches[switch_id]["is_active"] = is_active
    switches[switch_id]["toggled_at"] = datetime.now(timezone.utc).isoformat()
    
    # If toggling global OFF, mark but don't change individual states
    # If toggling global ON, restore individual states
    
    await db.master_switches.update_one(
        {"_type": "switches"},
        {
            "$set": {
                "switches": switches,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "updated_by": "admin"
            }
        }
    )
    
    # Log the action
    log_entry = {
        "action": "switch_toggle",
        "switch_id": switch_id,
        "new_state": is_active,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.master_switch_logs.insert_one(log_entry)
    
    return {
        "success": True,
        "switch_id": switch_id,
        "is_active": is_active,
        "message": f"Switch '{switches[switch_id]['name']}' {'activé' if is_active else 'désactivé'}"
    }


@router.post("/toggle-all")
async def toggle_all_switches(is_active: bool = Body(..., embed=True)):
    """
    Active ou désactive tous les switches d'un coup via le Master Switch Global.
    """
    db = get_db()
    
    switches_doc = await db.master_switches.find_one({"_type": "switches"})
    
    if not switches_doc:
        # Initialize
        switches_doc = {
            "_type": "switches",
            "switches": DEFAULT_SWITCHES
        }
    
    switches = switches_doc.get("switches", DEFAULT_SWITCHES)
    
    # Update global switch
    switches["global"]["is_active"] = is_active
    switches["global"]["toggled_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.master_switches.update_one(
        {"_type": "switches"},
        {
            "$set": {
                "switches": switches,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "updated_by": "admin"
            }
        },
        upsert=True
    )
    
    # Log
    log_entry = {
        "action": "global_toggle",
        "new_state": is_active,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.master_switch_logs.insert_one(log_entry)
    
    return {
        "success": True,
        "global_state": is_active,
        "message": f"Tous les modules X300% {'activés' if is_active else 'désactivés'}"
    }


@router.get("/check/{module}")
async def check_module_status(module: str):
    """
    Vérifie si un module spécifique est actif.
    Utilisé par les autres modules pour vérifier avant d'exécuter.
    """
    db = get_db()
    
    switches_doc = await db.master_switches.find_one({"_type": "switches"})
    
    if not switches_doc:
        return {"success": True, "is_active": True, "reason": "defaults"}
    
    switches = switches_doc.get("switches", {})
    
    # Check global first
    if not switches.get("global", {}).get("is_active", True):
        return {"success": True, "is_active": False, "reason": "global_off"}
    
    # Check specific module
    module_switch = switches.get(module, {})
    is_active = module_switch.get("is_active", True)
    
    return {
        "success": True,
        "module": module,
        "is_active": is_active,
        "reason": "module_state"
    }


@router.get("/logs")
async def get_switch_logs(limit: int = 50):
    """
    Historique des changements de switches.
    """
    db = get_db()
    
    logs = await db.master_switch_logs.find({}).sort("timestamp", -1).limit(limit).to_list(limit)
    
    for log in logs:
        log.pop("_id", None)
    
    return {
        "success": True,
        "logs": logs,
        "count": len(logs)
    }


logger.info("Master Switch X300% initialized - LEGO V5 Module")
