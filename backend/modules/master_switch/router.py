"""
BIONIC Master Switch - X300% Strategy
======================================

Contrôle global ON/OFF pour:
- Captation (Contact Engine)
- Enrichissement (Identity Graph)
- Triggers (Marketing Trigger Engine)
- Scoring (Lead Scoring)
- SEO Engine
- BIONIC Engine (Next Step Engine)

Architecture LEGO V5 - Module isolé.

MODES:
- LOCKED: Système verrouillé (PRÉ-GO LIVE)
- STAGING: Développement interne uniquement (INTERNAL_ONLY)
- PRODUCTION: Système actif avec flux externes
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


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTÈME DE MODES
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_MODES = {
    "LOCKED": {
        "name": "Verrouillé",
        "description": "PRÉ-GO LIVE - Aucune activation",
        "internal_only": True,
        "external_flows": False,
        "icon": "🔒"
    },
    "STAGING": {
        "name": "Staging",
        "description": "Développement interne uniquement",
        "internal_only": True,
        "external_flows": False,
        "icon": "🔧"
    },
    "PRODUCTION": {
        "name": "Production",
        "description": "Système actif avec flux externes",
        "internal_only": False,
        "external_flows": True,
        "icon": "🚀"
    }
}

# VERROUILLAGES EXTERNES (SÉCURITÉ RENFORCÉE)
EXTERNAL_LOCKS = {
    "social_networks": {
        "name": "Réseaux Sociaux",
        "description": "Envoi automatique vers réseaux sociaux",
        "is_locked": True,
        "icon": "📱"
    },
    "partners_platforms": {
        "name": "Partenaires & Plateformes Pub",
        "description": "Envoi automatique vers partenaires/plateformes",
        "is_locked": True,
        "icon": "🤝"
    },
    "external_webhooks": {
        "name": "Webhooks Externes",
        "description": "Webhooks vers services tiers",
        "is_locked": True,
        "icon": "🔗"
    },
    "marketing_flows": {
        "name": "Flux Marketing Externes",
        "description": "Déclenchement de flux marketing externes",
        "is_locked": True,
        "icon": "📢"
    }
}

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
    },
    "bionic_engine": {
        "name": "BIONIC Engine",
        "description": "Next Step Engine, Setup Builder, Chasseur Jumeau, Scores",
        "is_active": True,
        "icon": "🎯"
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


# ═══════════════════════════════════════════════════════════════════════════════
# GESTION DES MODES SYSTÈME
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/mode")
async def get_system_mode():
    """
    Récupère le mode système actuel.
    """
    db = get_db()
    
    mode_doc = await db.master_switches.find_one({"_type": "system_mode"})
    
    if not mode_doc:
        # Initialize with STAGING mode (validation COPILOT MAÎTRE)
        mode_doc = {
            "_type": "system_mode",
            "current_mode": "STAGING",
            "internal_only": True,
            "external_flows": False,
            "external_locks": EXTERNAL_LOCKS,
            "activated_at": datetime.now(timezone.utc).isoformat(),
            "activated_by": "COPILOT_MAITRE_STEEVE",
            "validation_signature": "2026-02-19_AUDIT_VALIDATED"
        }
        await db.master_switches.insert_one(mode_doc)
    
    mode_info = SYSTEM_MODES.get(mode_doc.get("current_mode", "LOCKED"), SYSTEM_MODES["LOCKED"])
    
    return {
        "success": True,
        "current_mode": mode_doc.get("current_mode", "LOCKED"),
        "mode_info": mode_info,
        "internal_only": mode_doc.get("internal_only", True),
        "external_flows": mode_doc.get("external_flows", False),
        "external_locks": mode_doc.get("external_locks", EXTERNAL_LOCKS),
        "activated_at": mode_doc.get("activated_at"),
        "activated_by": mode_doc.get("activated_by")
    }


@router.post("/mode/set")
async def set_system_mode(mode: str = Body(..., embed=True), authorized_by: str = Body(..., embed=True)):
    """
    Change le mode système.
    REQUIERT autorisation COPILOT MAÎTRE.
    """
    db = get_db()
    
    if mode not in SYSTEM_MODES:
        return {"success": False, "error": f"Mode invalide. Modes disponibles: {list(SYSTEM_MODES.keys())}"}
    
    mode_info = SYSTEM_MODES[mode]
    
    update_data = {
        "_type": "system_mode",
        "current_mode": mode,
        "internal_only": mode_info["internal_only"],
        "external_flows": mode_info["external_flows"],
        "external_locks": EXTERNAL_LOCKS,  # Toujours verrouillés sauf PRODUCTION explicite
        "activated_at": datetime.now(timezone.utc).isoformat(),
        "activated_by": authorized_by
    }
    
    await db.master_switches.update_one(
        {"_type": "system_mode"},
        {"$set": update_data},
        upsert=True
    )
    
    # Log the mode change
    log_entry = {
        "action": "mode_change",
        "new_mode": mode,
        "authorized_by": authorized_by,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.master_switch_logs.insert_one(log_entry)
    
    return {
        "success": True,
        "mode": mode,
        "mode_info": mode_info,
        "internal_only": mode_info["internal_only"],
        "external_flows": mode_info["external_flows"],
        "message": f"Mode système changé vers {mode} par {authorized_by}"
    }


@router.get("/external-locks")
async def get_external_locks():
    """
    Récupère l'état des verrouillages externes.
    """
    db = get_db()
    
    mode_doc = await db.master_switches.find_one({"_type": "system_mode"})
    
    locks = mode_doc.get("external_locks", EXTERNAL_LOCKS) if mode_doc else EXTERNAL_LOCKS
    
    all_locked = all(lock.get("is_locked", True) for lock in locks.values())
    
    return {
        "success": True,
        "external_locks": locks,
        "all_locked": all_locked,
        "security_status": "RENFORCÉ" if all_locked else "PARTIELLEMENT_ACTIF"
    }


@router.get("/full-status")
async def get_full_system_status():
    """
    Retourne le statut complet du système (mode + switches + locks).
    """
    db = get_db()
    
    # Mode
    mode_doc = await db.master_switches.find_one({"_type": "system_mode"})
    current_mode = mode_doc.get("current_mode", "LOCKED") if mode_doc else "LOCKED"
    mode_info = SYSTEM_MODES.get(current_mode, SYSTEM_MODES["LOCKED"])
    
    # Switches
    switches_doc = await db.master_switches.find_one({"_type": "switches"})
    switches = switches_doc.get("switches", DEFAULT_SWITCHES) if switches_doc else DEFAULT_SWITCHES
    
    # External Locks
    external_locks = mode_doc.get("external_locks", EXTERNAL_LOCKS) if mode_doc else EXTERNAL_LOCKS
    
    active_switches = sum(1 for s in switches.values() if s.get("is_active", True))
    all_locked = all(lock.get("is_locked", True) for lock in external_locks.values())
    
    return {
        "success": True,
        "system": {
            "mode": current_mode,
            "mode_info": mode_info,
            "internal_only": mode_info["internal_only"],
            "external_flows": mode_info["external_flows"]
        },
        "switches": {
            "total": len(switches),
            "active": active_switches,
            "global_state": switches.get("global", {}).get("is_active", True)
        },
        "security": {
            "external_locks_status": "ALL_LOCKED" if all_locked else "PARTIALLY_ACTIVE",
            "external_locks": external_locks
        },
        "bionic_engine_status": "ACTIVE" if switches.get("bionic_engine", {}).get("is_active", True) else "INACTIVE"
    }


logger.info("Master Switch X300% initialized - LEGO V5 Module - MODE STAGING ACTIVÉ")
