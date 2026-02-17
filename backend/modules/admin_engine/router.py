"""
Admin Engine Router - V5-ULTIME Administration Premium
======================================================

Point d'entrée API pour l'administration premium.
Prefix: /api/v1/admin

Sous-routes:
- /ecommerce/* : Gestion E-Commerce (Phase 1 Migration)
- /payments/* : Gestion paiements Stripe
- /freemium/* : Gestion quotas et tiers
- /upsell/* : Gestion campagnes
- /onboarding/* : Gestion parcours
- /tutorials/* : Gestion tutoriels
- /rules/* : Gestion règles Plan Maître
- /strategy/* : Gestion stratégies
- /users/* : Gestion utilisateurs
- /logs/* : Logs système
- /settings/* : Paramètres globaux

Version: 1.1.0 - Phase 1 Migration E-Commerce
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Services modulaires
from .services.payments_admin import PaymentsAdminService
from .services.freemium_admin import FreemiumAdminService
from .services.upsell_admin import UpsellAdminService
from .services.onboarding_admin import OnboardingAdminService
from .services.tutorials_admin import TutorialsAdminService
from .services.rules_admin import RulesAdminService
from .services.strategy_admin import StrategyAdminService
from .services.users_admin import UsersAdminService
from .services.logs_admin import LogsAdminService
from .services.settings_admin import SettingsAdminService
# Phase 1 Migration - E-Commerce
from .services.ecommerce_admin import EcommerceAdminService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Engine - Premium"])

# Database
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

# ==============================================
# ADMIN AUTHENTICATION DEPENDENCY
# ==============================================

async def verify_admin_role(authorization: str = None):
    """Vérifie que l'utilisateur a le rôle admin"""
    # Note: En production, implémenter vérification JWT complète
    # Pour l'instant, vérification basique
    if not authorization:
        # Mode développement - permettre l'accès
        return {"role": "admin", "user_id": "admin_dev"}
    
    # Vérification JWT à implémenter
    return {"role": "admin", "user_id": "admin_user"}

# ==============================================
# MODULE INFO
# ==============================================

@router.get("/")
async def admin_engine_info():
    """Information sur le module Admin Engine"""
    return {
        "module": "admin_engine",
        "version": "1.1.0",
        "description": "Administration Premium V5-ULTIME - Phase 1 Migration",
        "access": "admin_only",
        "sub_modules": [
            "ecommerce", "payments", "freemium", "upsell", "onboarding",
            "tutorials", "rules", "strategy", "users", "logs", "settings"
        ],
        "features": [
            "Gestion E-Commerce (dashboard, sales, products, suppliers, customers, commissions, performance)",
            "Gestion paiements Stripe",
            "Gestion quotas freemium",
            "Gestion campagnes upsell",
            "Gestion parcours onboarding",
            "Gestion tutoriels",
            "Gestion règles Plan Maître",
            "Gestion stratégies",
            "Gestion utilisateurs",
            "Logs système",
            "Paramètres globaux"
        ]
    }

@router.get("/dashboard")
async def admin_dashboard():
    """Dashboard principal avec KPIs"""
    db = get_db()
    
    # Compter les documents
    users_count = await db.users.count_documents({})
    subscriptions_count = await db.subscriptions.count_documents({})
    premium_count = await db.subscriptions.count_documents({"tier": {"$in": ["premium", "pro"]}})
    transactions_count = await db.payment_transactions.count_documents({})
    
    # Revenus (transactions payées)
    paid_transactions = await db.payment_transactions.find(
        {"payment_status": "paid"},
        {"amount": 1}
    ).to_list(length=1000)
    total_revenue = sum(t.get("amount", 0) for t in paid_transactions)
    
    # KPIs onboarding
    completed_onboarding = await db.onboarding_status.count_documents({"completed": True})
    
    # KPIs upsell
    upsell_impressions = await db.upsell_impressions.count_documents({})
    upsell_clicks = await db.upsell_clicks.count_documents({})
    
    return {
        "success": True,
        "dashboard": {
            "users": {
                "total": users_count,
                "with_subscription": subscriptions_count,
                "premium": premium_count,
                "free": subscriptions_count - premium_count
            },
            "revenue": {
                "total": round(total_revenue, 2),
                "currency": "CAD",
                "transactions": transactions_count
            },
            "onboarding": {
                "completed": completed_onboarding,
                "completion_rate": round((completed_onboarding / max(users_count, 1)) * 100, 1)
            },
            "upsell": {
                "impressions": upsell_impressions,
                "clicks": upsell_clicks,
                "ctr": round((upsell_clicks / max(upsell_impressions, 1)) * 100, 2)
            }
        },
        "generated_at": datetime.now(timezone.utc).isoformat()
    }

# ==============================================
# PAYMENTS ADMIN
# ==============================================

@router.get("/payments/transactions")
async def get_all_transactions(
    limit: int = Query(50, le=500),
    status: Optional[str] = None,
    skip: int = 0
):
    """Liste toutes les transactions"""
    return await PaymentsAdminService.get_transactions(get_db(), limit, status, skip)

@router.get("/payments/transactions/{transaction_id}")
async def get_transaction_detail(transaction_id: str):
    """Détail d'une transaction"""
    return await PaymentsAdminService.get_transaction_detail(get_db(), transaction_id)

@router.get("/payments/revenue")
async def get_revenue_stats(days: int = Query(30, le=365)):
    """Statistiques de revenus"""
    return await PaymentsAdminService.get_revenue_stats(get_db(), days)

@router.get("/payments/subscriptions")
async def get_all_subscriptions(
    tier: Optional[str] = None,
    limit: int = Query(50, le=500)
):
    """Liste tous les abonnements"""
    return await PaymentsAdminService.get_subscriptions(get_db(), tier, limit)

# ==============================================
# FREEMIUM ADMIN
# ==============================================

@router.get("/freemium/quotas")
async def get_quota_overview():
    """Vue d'ensemble des quotas"""
    return await FreemiumAdminService.get_quota_overview(get_db())

@router.get("/freemium/users/{user_id}")
async def get_user_freemium_status(user_id: str):
    """Statut freemium d'un utilisateur"""
    return await FreemiumAdminService.get_user_status(get_db(), user_id)

@router.put("/freemium/users/{user_id}/override")
async def override_user_limits(user_id: str, overrides: dict):
    """Override les limites d'un utilisateur"""
    return await FreemiumAdminService.set_user_override(get_db(), user_id, overrides)

@router.get("/freemium/tiers/stats")
async def get_tier_distribution():
    """Distribution des utilisateurs par tier"""
    return await FreemiumAdminService.get_tier_distribution(get_db())

# ==============================================
# UPSELL ADMIN
# ==============================================

@router.get("/upsell/campaigns")
async def get_upsell_campaigns():
    """Liste des campagnes upsell"""
    return await UpsellAdminService.get_campaigns(get_db())

@router.put("/upsell/campaigns/{campaign_name}/toggle")
async def toggle_campaign(campaign_name: str, enabled: bool):
    """Activer/désactiver une campagne"""
    return await UpsellAdminService.toggle_campaign(get_db(), campaign_name, enabled)

@router.get("/upsell/analytics")
async def get_upsell_analytics(days: int = Query(30, le=90)):
    """Analytics des campagnes"""
    return await UpsellAdminService.get_analytics(get_db(), days)

@router.get("/upsell/conversions")
async def get_conversion_funnel():
    """Funnel de conversion"""
    return await UpsellAdminService.get_conversion_funnel(get_db())

# ==============================================
# ONBOARDING ADMIN
# ==============================================

@router.get("/onboarding/stats")
async def get_onboarding_stats():
    """Statistiques d'onboarding"""
    return await OnboardingAdminService.get_stats(get_db())

@router.get("/onboarding/flows")
async def get_onboarding_flows():
    """Configuration des flows"""
    return await OnboardingAdminService.get_flows(get_db())

@router.get("/onboarding/users")
async def get_users_onboarding_status(
    completed: Optional[bool] = None,
    limit: int = Query(50, le=500)
):
    """Liste des utilisateurs et leur statut onboarding"""
    return await OnboardingAdminService.get_users_status(get_db(), completed, limit)

# ==============================================
# TUTORIALS ADMIN
# ==============================================

@router.get("/tutorials/list")
async def get_all_tutorials():
    """Liste tous les tutoriels"""
    return await TutorialsAdminService.get_tutorials(get_db())

@router.put("/tutorials/{tutorial_id}/toggle")
async def toggle_tutorial(tutorial_id: str, enabled: bool):
    """Activer/désactiver un tutoriel"""
    return await TutorialsAdminService.toggle_tutorial(get_db(), tutorial_id, enabled)

@router.get("/tutorials/progress")
async def get_tutorials_progress():
    """Progression globale des tutoriels"""
    return await TutorialsAdminService.get_progress_stats(get_db())

# ==============================================
# RULES ADMIN
# ==============================================

@router.get("/rules/list")
async def get_all_rules():
    """Liste toutes les règles"""
    return await RulesAdminService.get_rules(get_db())

@router.put("/rules/{rule_id}/toggle")
async def toggle_rule(rule_id: str, enabled: bool):
    """Activer/désactiver une règle"""
    return await RulesAdminService.toggle_rule(get_db(), rule_id, enabled)

@router.put("/rules/{rule_id}/weight")
async def update_rule_weight(rule_id: str, weight: float):
    """Modifier le poids d'une règle"""
    return await RulesAdminService.update_weight(get_db(), rule_id, weight)

@router.get("/rules/stats")
async def get_rules_stats():
    """Statistiques des règles"""
    return await RulesAdminService.get_stats(get_db())

# ==============================================
# STRATEGY ADMIN
# ==============================================

@router.get("/strategy/generated")
async def get_generated_strategies(
    limit: int = Query(50, le=500),
    user_id: Optional[str] = None
):
    """Liste les stratégies générées"""
    return await StrategyAdminService.get_strategies(get_db(), limit, user_id)

@router.get("/strategy/logs")
async def get_strategy_logs(limit: int = Query(100, le=1000)):
    """Logs de génération"""
    return await StrategyAdminService.get_logs(get_db(), limit)

@router.get("/strategy/diagnostics")
async def get_strategy_diagnostics():
    """Diagnostics du moteur"""
    return await StrategyAdminService.get_diagnostics(get_db())

# ==============================================
# USERS ADMIN
# ==============================================

@router.get("/users/list")
async def get_all_users(
    limit: int = Query(50, le=500),
    role: Optional[str] = None,
    tier: Optional[str] = None
):
    """Liste tous les utilisateurs"""
    return await UsersAdminService.get_users(get_db(), limit, role, tier)

@router.get("/users/{user_id}")
async def get_user_detail(user_id: str):
    """Détail d'un utilisateur"""
    return await UsersAdminService.get_user_detail(get_db(), user_id)

@router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, role: str):
    """Modifier le rôle d'un utilisateur"""
    return await UsersAdminService.update_role(get_db(), user_id, role)

@router.get("/users/{user_id}/activity")
async def get_user_activity(user_id: str, days: int = Query(30, le=90)):
    """Historique d'activité"""
    return await UsersAdminService.get_activity(get_db(), user_id, days)

# ==============================================
# LOGS ADMIN
# ==============================================

@router.get("/logs/errors")
async def get_error_logs(
    limit: int = Query(100, le=1000),
    severity: Optional[str] = None
):
    """Logs d'erreurs"""
    return await LogsAdminService.get_errors(get_db(), limit, severity)

@router.get("/logs/webhooks")
async def get_webhook_logs(limit: int = Query(100, le=500)):
    """Logs webhooks"""
    return await LogsAdminService.get_webhooks(get_db(), limit)

@router.get("/logs/events")
async def get_event_logs(
    limit: int = Query(100, le=1000),
    event_type: Optional[str] = None
):
    """Logs d'événements"""
    return await LogsAdminService.get_events(get_db(), limit, event_type)

# ==============================================
# SETTINGS ADMIN
# ==============================================

@router.get("/settings")
async def get_all_settings():
    """Récupérer tous les paramètres"""
    return await SettingsAdminService.get_settings(get_db())

@router.put("/settings/{key}")
async def update_setting(key: str, value: Any):
    """Modifier un paramètre"""
    return await SettingsAdminService.update_setting(get_db(), key, value)

@router.get("/settings/api-keys")
async def get_api_keys_status():
    """Statut des clés API (masquées)"""
    return await SettingsAdminService.get_api_keys_status(get_db())

@router.get("/settings/toggles")
async def get_feature_toggles():
    """Toggles de fonctionnalités"""
    return await SettingsAdminService.get_toggles(get_db())

@router.put("/settings/toggles/{toggle_id}")
async def update_toggle(toggle_id: str, enabled: bool):
    """Modifier un toggle"""
    return await SettingsAdminService.update_toggle(get_db(), toggle_id, enabled)
