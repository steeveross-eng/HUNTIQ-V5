"""
BIONIC Global Master Switch - Contrôle Central du Système
==========================================================

Gros Bouton ROUGE pour le contrôle global du système publicitaire:
- ON / OFF / LOCKED status
- Contrôle de tous les engines publicitaires
- Journalisation complète des actions
- Accessible uniquement par COPILOT MAÎTRE

Engines contrôlés:
- Affiliate Ad Automation Engine
- Ad Spaces Engine
- Ad Slot Manager
- Ad Render Engine
- Marketing Engine
- Calendar Engine

Architecture LEGO V5-ULTIME - Module isolé.
"""

from fastapi import APIRouter, Body, Query, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from enum import Enum
import os
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/global-switch", tags=["Global Master Switch"])

# Database connection
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


# ============================================
# ENUMS & CONSTANTS
# ============================================

class SwitchStatus(str, Enum):
    ON = "ON"
    OFF = "OFF"
    LOCKED = "LOCKED"


class ControlledEngine(str, Enum):
    AFFILIATE_ADS = "affiliate_ad_automation_engine"
    AD_SPACES = "ad_spaces_engine"
    AD_SLOTS = "ad_slot_manager"
    AD_RENDER = "ad_render_engine"
    MARKETING = "marketing_engine"
    CALENDAR = "calendar_engine"


CONTROLLED_ENGINES = [
    {
        "id": ControlledEngine.AFFILIATE_ADS.value,
        "name": "Affiliate Ad Automation Engine",
        "description": "Cycle de vente publicitaire automatisé",
        "api_prefix": "/api/v1/affiliate-ads"
    },
    {
        "id": ControlledEngine.AD_SPACES.value,
        "name": "Ad Spaces Engine",
        "description": "Gestion des 18 espaces publicitaires",
        "api_prefix": "/api/v1/ad-spaces"
    },
    {
        "id": ControlledEngine.AD_SLOTS.value,
        "name": "Ad Slot Manager",
        "description": "Attribution et réservation des emplacements",
        "api_prefix": "/api/v1/ad-spaces/slots"
    },
    {
        "id": ControlledEngine.AD_RENDER.value,
        "name": "Ad Render Engine",
        "description": "Injection et affichage des publicités",
        "api_prefix": "/api/v1/ad-spaces/render"
    },
    {
        "id": ControlledEngine.MARKETING.value,
        "name": "Marketing Engine",
        "description": "Campagnes marketing automatisées",
        "api_prefix": "/api/v1/marketing"
    },
    {
        "id": ControlledEngine.CALENDAR.value,
        "name": "Calendar Engine",
        "description": "Planification des campagnes",
        "api_prefix": "/api/v1/calendar"
    }
]


# ============================================
# MODULE INFO
# ============================================

@router.get("/")
async def get_module_info():
    """Information sur le Global Master Switch"""
    db = get_db()
    
    # Get current state
    switch = await db.global_master_switch.find_one({"switch_id": "BIONIC_GLOBAL"})
    
    return {
        "module": "global_master_switch",
        "version": "1.0.0",
        "description": "🔴 GROS BOUTON ROUGE - Contrôle global du système publicitaire BIONIC",
        "architecture": "LEGO_V5_ULTIME",
        "features": [
            "Contrôle ON/OFF/LOCKED global",
            "Synchronisation de tous les engines publicitaires",
            "Blocage du déploiement automatique",
            "Journalisation horodatée des actions",
            "Accès restreint (COPILOT MAÎTRE uniquement)"
        ],
        "current_status": switch.get("status") if switch else "NOT_INITIALIZED",
        "controlled_engines": [e["name"] for e in CONTROLLED_ENGINES]
    }


# ============================================
# GLOBAL MASTER SWITCH CONTROL
# ============================================

@router.get("/status")
async def get_global_switch_status():
    """
    Obtenir le statut actuel du Global Master Switch.
    """
    db = get_db()
    
    switch = await db.global_master_switch.find_one({"switch_id": "BIONIC_GLOBAL"})
    
    if not switch:
        # Initialize in LOCKED state (PRÉ-PRODUCTION)
        switch = {
            "switch_id": "BIONIC_GLOBAL",
            "status": SwitchStatus.LOCKED.value,
            "is_active": False,
            "auto_deploy_blocked": True,
            "reason": "Mode PRÉ-PRODUCTION - En attente du signal GO LIVE de COPILOT MAÎTRE",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "last_updated_by": "system_init",
            "engines_status": {e["id"]: False for e in CONTROLLED_ENGINES},
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.global_master_switch.insert_one(switch)
    
    switch.pop("_id", None)
    
    # Get ad system status
    ad_master = await db.ad_master_switch.find_one({"switch_id": "global"})
    
    return {
        "success": True,
        "global_switch": switch,
        "ad_master_switch": {
            "is_active": ad_master.get("is_active") if ad_master else False,
            "reason": ad_master.get("reason") if ad_master else "Non initialisé"
        },
        "controlled_engines": CONTROLLED_ENGINES,
        "mode": "PRÉ-PRODUCTION" if switch["status"] != SwitchStatus.ON.value else "PRODUCTION"
    }


@router.post("/toggle")
async def toggle_global_switch(
    new_status: str = Body(..., embed=True),
    reason: Optional[str] = Body(None, embed=True),
    admin_user: str = Body("admin", embed=True)
):
    """
    Basculer le Global Master Switch.
    
    Args:
        new_status: "ON" | "OFF" | "LOCKED"
        reason: Raison du changement
        admin_user: Utilisateur effectuant l'action
    """
    db = get_db()
    
    if new_status not in [s.value for s in SwitchStatus]:
        raise HTTPException(
            status_code=400, 
            detail=f"Statut invalide. Valeurs acceptées: {[s.value for s in SwitchStatus]}"
        )
    
    now = datetime.now(timezone.utc).isoformat()
    
    # Determine if system should be active
    is_active = new_status == SwitchStatus.ON.value
    
    # Update global switch
    switch_updates = {
        "status": new_status,
        "is_active": is_active,
        "auto_deploy_blocked": not is_active,
        "reason": reason or f"Basculement vers {new_status}",
        "last_updated": now,
        "last_updated_by": admin_user
    }
    
    await db.global_master_switch.update_one(
        {"switch_id": "BIONIC_GLOBAL"},
        {"$set": switch_updates},
        upsert=True
    )
    
    # Sync with ad_master_switch
    await db.ad_master_switch.update_one(
        {"switch_id": "global"},
        {
            "$set": {
                "is_active": is_active,
                "auto_deploy_enabled": is_active,
                "reason": switch_updates["reason"],
                "updated_at": now,
                "updated_by": admin_user
            }
        },
        upsert=True
    )
    
    # Update all controlled engines status
    engines_status = {}
    for engine in CONTROLLED_ENGINES:
        engines_status[engine["id"]] = is_active
    
    await db.global_master_switch.update_one(
        {"switch_id": "BIONIC_GLOBAL"},
        {"$set": {"engines_status": engines_status}}
    )
    
    # If turning OFF or LOCKED, deactivate all ads
    if not is_active:
        # Pause active campaigns
        await db.ad_opportunities.update_many(
            {"status": "active"},
            {"$set": {"status": "paused", "paused_at": now, "pause_reason": switch_updates["reason"]}}
        )
        
        # Suspend pending opportunities
        await db.ad_opportunities.update_many(
            {"status": {"$in": ["pending", "email_sent", "checkout_started", "payment_pending"]}},
            {"$set": {"status": "suspended", "suspended_at": now, "suspend_reason": switch_updates["reason"]}}
        )
        
        # Deactivate deployed ads
        await db.deployed_ads.update_many(
            {"is_active": True},
            {"$set": {"is_active": False, "deactivated_at": now}}
        )
        
        # Deactivate slots
        await db.ad_slot_reservations.update_many(
            {"status": "active"},
            {"$set": {"status": "paused", "paused_at": now}}
        )
    
    # Log action
    await _log_switch_action(db, "global_toggle", admin_user, {
        "previous_status": "unknown",
        "new_status": new_status,
        "reason": switch_updates["reason"],
        "is_active": is_active
    })
    
    return {
        "success": True,
        "status": new_status,
        "is_active": is_active,
        "auto_deploy_blocked": not is_active,
        "engines_affected": len(CONTROLLED_ENGINES),
        "message": f"🔴 Global Master Switch → {new_status}" + (" (Système ACTIF)" if is_active else " (Système VERROUILLÉ)")
    }


@router.post("/lock")
async def lock_system(
    reason: str = Body(..., embed=True),
    admin_user: str = Body("COPILOT_MAITRE", embed=True)
):
    """
    Verrouiller le système publicitaire (mode LOCKED).
    Aucune publicité ne sera diffusée jusqu'au déverrouillage.
    """
    return await toggle_global_switch(
        new_status=SwitchStatus.LOCKED.value,
        reason=reason,
        admin_user=admin_user
    )


@router.post("/unlock")
async def unlock_system(
    admin_user: str = Body("COPILOT_MAITRE", embed=True)
):
    """
    Déverrouiller et activer le système (GO LIVE).
    """
    return await toggle_global_switch(
        new_status=SwitchStatus.ON.value,
        reason="🚀 GO LIVE - Activation par COPILOT MAÎTRE",
        admin_user=admin_user
    )


# ============================================
# ENGINE-SPECIFIC CONTROL
# ============================================

@router.get("/engines")
async def get_engines_status():
    """
    Obtenir le statut de tous les engines contrôlés.
    """
    db = get_db()
    
    switch = await db.global_master_switch.find_one({"switch_id": "BIONIC_GLOBAL"})
    engines_status = switch.get("engines_status", {}) if switch else {}
    
    engines = []
    for engine in CONTROLLED_ENGINES:
        engines.append({
            **engine,
            "is_active": engines_status.get(engine["id"], False),
            "status": "ACTIVE" if engines_status.get(engine["id"]) else "DISABLED"
        })
    
    return {
        "success": True,
        "global_status": switch.get("status") if switch else "NOT_INITIALIZED",
        "engines": engines,
        "total_active": sum(1 for e in engines if e["is_active"]),
        "total_disabled": sum(1 for e in engines if not e["is_active"])
    }


@router.post("/engines/{engine_id}/toggle")
async def toggle_engine(
    engine_id: str,
    is_active: bool = Body(..., embed=True),
    admin_user: str = Body("admin", embed=True)
):
    """
    Contrôler un engine spécifique (si le Global Switch est ON).
    """
    db = get_db()
    
    # Check global switch
    switch = await db.global_master_switch.find_one({"switch_id": "BIONIC_GLOBAL"})
    
    if switch and switch.get("status") == SwitchStatus.LOCKED.value:
        return {
            "success": False,
            "error": "Système verrouillé - Impossible de modifier les engines individuels",
            "global_status": "LOCKED"
        }
    
    # Validate engine_id
    valid_ids = [e["id"] for e in CONTROLLED_ENGINES]
    if engine_id not in valid_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Engine non trouvé. Engines valides: {valid_ids}"
        )
    
    # Update engine status
    await db.global_master_switch.update_one(
        {"switch_id": "BIONIC_GLOBAL"},
        {"$set": {f"engines_status.{engine_id}": is_active}}
    )
    
    # Log action
    await _log_switch_action(db, "engine_toggle", admin_user, {
        "engine_id": engine_id,
        "new_status": is_active
    })
    
    return {
        "success": True,
        "engine_id": engine_id,
        "is_active": is_active,
        "message": f"Engine '{engine_id}' → {'ACTIVÉ' if is_active else 'DÉSACTIVÉ'}"
    }


# ============================================
# AUDIT LOG
# ============================================

@router.get("/logs")
async def get_switch_logs(
    limit: int = Query(100, le=500)
):
    """
    Historique des actions sur le Global Master Switch.
    """
    db = get_db()
    
    logs = await db.global_switch_logs.find({}).sort("timestamp", -1).limit(limit).to_list(limit)
    
    for log in logs:
        log.pop("_id", None)
    
    return {
        "success": True,
        "logs": logs,
        "count": len(logs)
    }


async def _log_switch_action(db, action: str, admin_user: str, details: Dict = None):
    """Journaliser une action sur le switch."""
    log_entry = {
        "log_id": str(uuid.uuid4()),
        "action": action,
        "admin_user": admin_user,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    await db.global_switch_logs.insert_one(log_entry)


# ============================================
# DASHBOARD
# ============================================

@router.get("/dashboard")
async def get_switch_dashboard():
    """
    Dashboard du Global Master Switch.
    """
    db = get_db()
    
    # Global switch
    switch = await db.global_master_switch.find_one({"switch_id": "BIONIC_GLOBAL"})
    
    # Ad system stats
    total_opportunities = await db.ad_opportunities.count_documents({})
    active_opportunities = await db.ad_opportunities.count_documents({"status": "active"})
    paused_opportunities = await db.ad_opportunities.count_documents({"status": "paused"})
    suspended_opportunities = await db.ad_opportunities.count_documents({"status": "suspended"})
    
    # Deployed ads
    active_ads = await db.deployed_ads.count_documents({"is_active": True})
    inactive_ads = await db.deployed_ads.count_documents({"is_active": False})
    
    # Slots
    active_slots = await db.ad_slot_reservations.count_documents({"status": "active"})
    paused_slots = await db.ad_slot_reservations.count_documents({"status": "paused"})
    
    # Recent logs
    recent_logs = await db.global_switch_logs.find({}).sort("timestamp", -1).limit(10).to_list(10)
    for log in recent_logs:
        log.pop("_id", None)
    
    return {
        "success": True,
        "dashboard": {
            "global_switch": {
                "status": switch.get("status") if switch else "NOT_INITIALIZED",
                "is_active": switch.get("is_active") if switch else False,
                "auto_deploy_blocked": switch.get("auto_deploy_blocked") if switch else True,
                "reason": switch.get("reason") if switch else "Non initialisé",
                "last_updated": switch.get("last_updated") if switch else None,
                "last_updated_by": switch.get("last_updated_by") if switch else None
            },
            "mode": "PRODUCTION" if (switch and switch.get("is_active")) else "PRÉ-PRODUCTION",
            "opportunities": {
                "total": total_opportunities,
                "active": active_opportunities,
                "paused": paused_opportunities,
                "suspended": suspended_opportunities
            },
            "deployed_ads": {
                "active": active_ads,
                "inactive": inactive_ads
            },
            "slots": {
                "active": active_slots,
                "paused": paused_slots
            },
            "controlled_engines": len(CONTROLLED_ENGINES),
            "recent_activity": recent_logs
        }
    }


logger.info("Global Master Switch initialized - LEGO V5-ULTIME Module")
