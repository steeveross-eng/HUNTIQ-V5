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
# Phase 2 Migration - Content & Backup
from .services.content_admin import ContentAdminService
from .services.backup_admin import BackupAdminService
# Phase 3 Migration - Infrastructure + Contacts
from .services.maintenance_admin import MaintenanceAdminService
from .services.contacts_admin import ContactsAdminService
# Phase 4 Migration - Hotspots & Networking
from .services.hotspots_admin import HotspotsAdminService
from .services.networking_admin import NetworkingAdminService

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
        "version": "1.3.0",
        "description": "Administration Premium V5-ULTIME - Phase 3 Migration",
        "access": "admin_only",
        "sub_modules": [
            "ecommerce", "content", "backup", "maintenance", "contacts",
            "payments", "freemium", "upsell", "onboarding",
            "tutorials", "rules", "strategy", "users", "logs", "settings"
        ],
        "features": [
            "Gestion E-Commerce (dashboard, sales, products, suppliers, customers, commissions, performance)",
            "Gestion Contenu (categories, SEO, content depot)",
            "Gestion Backups (code, prompts, database)",
            "Gestion Maintenance (mode maintenance, access control, scheduled maintenance)",
            "Gestion Contacts (fournisseurs, fabricants, partenaires, formateurs, experts)",
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


# ==============================================
# E-COMMERCE ADMIN (Phase 1 Migration)
# ==============================================

@router.get("/ecommerce/dashboard")
async def get_ecommerce_dashboard():
    """Dashboard E-Commerce avec stats globales"""
    return await EcommerceAdminService.get_dashboard_stats(get_db())

@router.get("/ecommerce/orders")
async def get_ecommerce_orders(
    limit: int = Query(50, le=500),
    status: Optional[str] = None,
    skip: int = 0
):
    """Liste des commandes"""
    return await EcommerceAdminService.get_orders(get_db(), limit, status, skip)

@router.put("/ecommerce/orders/{order_id}/status")
async def update_ecommerce_order_status(order_id: str, status: str):
    """Mettre à jour le statut d'une commande"""
    return await EcommerceAdminService.update_order_status(get_db(), order_id, status)

@router.get("/ecommerce/products")
async def get_ecommerce_products(
    limit: int = Query(50, le=500),
    category: Optional[str] = None
):
    """Liste des produits"""
    return await EcommerceAdminService.get_products(get_db(), limit, category)

@router.post("/ecommerce/products")
async def create_ecommerce_product(product_data: dict = Body(...)):
    """Créer un nouveau produit"""
    return await EcommerceAdminService.create_product(get_db(), product_data)

@router.put("/ecommerce/products/{product_id}")
async def update_ecommerce_product(product_id: str, updates: dict = Body(...)):
    """Mettre à jour un produit"""
    return await EcommerceAdminService.update_product(get_db(), product_id, updates)

@router.delete("/ecommerce/products/{product_id}")
async def delete_ecommerce_product(product_id: str):
    """Supprimer un produit"""
    return await EcommerceAdminService.delete_product(get_db(), product_id)

@router.get("/ecommerce/suppliers")
async def get_ecommerce_suppliers(
    limit: int = Query(50, le=500),
    partnership_type: Optional[str] = None
):
    """Liste des fournisseurs"""
    return await EcommerceAdminService.get_suppliers(get_db(), limit, partnership_type)

@router.post("/ecommerce/suppliers")
async def create_ecommerce_supplier(supplier_data: dict = Body(...)):
    """Créer un nouveau fournisseur"""
    return await EcommerceAdminService.create_supplier(get_db(), supplier_data)

@router.get("/ecommerce/customers")
async def get_ecommerce_customers(
    limit: int = Query(50, le=500),
    sort_by: str = Query("total_spent")
):
    """Liste des clients"""
    return await EcommerceAdminService.get_customers(get_db(), limit, sort_by)

@router.get("/ecommerce/commissions")
async def get_ecommerce_commissions(
    limit: int = Query(50, le=500),
    status: Optional[str] = None
):
    """Liste des commissions"""
    return await EcommerceAdminService.get_commissions(get_db(), limit, status)

@router.put("/ecommerce/commissions/{commission_id}/status")
async def update_ecommerce_commission_status(commission_id: str, status: str):
    """Mettre à jour le statut d'une commission"""
    return await EcommerceAdminService.update_commission_status(get_db(), commission_id, status)

@router.get("/ecommerce/performance")
async def get_ecommerce_performance():
    """Rapport de performance des produits"""
    return await EcommerceAdminService.get_performance_report(get_db())

@router.get("/ecommerce/alerts")
async def get_ecommerce_alerts(
    limit: int = Query(20, le=100),
    unread_only: bool = False
):
    """Liste des alertes admin"""
    return await EcommerceAdminService.get_alerts(get_db(), limit, unread_only)


# ==============================================
# CONTENT ADMIN (Phase 2 Migration)
# ==============================================

@router.get("/content/categories")
async def get_content_categories():
    """Liste toutes les catégories"""
    return await ContentAdminService.get_categories(get_db())

@router.post("/content/categories")
async def create_content_category(category_data: dict = Body(...)):
    """Créer une nouvelle catégorie"""
    return await ContentAdminService.create_category(get_db(), category_data)

@router.put("/content/categories/{category_id}")
async def update_content_category(category_id: str, updates: dict = Body(...)):
    """Mettre à jour une catégorie"""
    return await ContentAdminService.update_category(get_db(), category_id, updates)

@router.delete("/content/categories/{category_id}")
async def delete_content_category(category_id: str):
    """Supprimer une catégorie"""
    return await ContentAdminService.delete_category(get_db(), category_id)

@router.post("/content/categories/init-defaults")
async def init_default_categories():
    """Initialiser les catégories par défaut"""
    return await ContentAdminService.init_default_categories(get_db())

@router.get("/content/depot")
async def get_content_depot_items(
    status: Optional[str] = None,
    limit: int = Query(50, le=500)
):
    """Liste les items du Content Depot"""
    return await ContentAdminService.get_content_items(get_db(), status, limit)

@router.post("/content/depot")
async def create_content_depot_item(item_data: dict = Body(...)):
    """Créer un nouvel item de contenu"""
    return await ContentAdminService.create_content_item(get_db(), item_data)

@router.put("/content/depot/{item_id}")
async def update_content_depot_item(item_id: str, updates: dict = Body(...)):
    """Mettre à jour un item de contenu"""
    return await ContentAdminService.update_content_item(get_db(), item_id, updates)

@router.put("/content/depot/{item_id}/status")
async def update_content_depot_status(item_id: str, status: str):
    """Mettre à jour le statut d'un item"""
    return await ContentAdminService.update_content_status(get_db(), item_id, status)

@router.delete("/content/depot/{item_id}")
async def delete_content_depot_item(item_id: str):
    """Supprimer un item de contenu"""
    return await ContentAdminService.delete_content_item(get_db(), item_id)

@router.get("/content/seo-analytics")
async def get_seo_analytics():
    """Statistiques SEO globales"""
    return await ContentAdminService.get_seo_analytics(get_db())

# ==============================================
# BACKUP ADMIN (Phase 2 Migration)
# ==============================================

@router.get("/backup/stats")
async def get_backup_stats():
    """Statistiques globales des backups"""
    return await BackupAdminService.get_backup_stats(get_db())

@router.get("/backup/code/files")
async def get_backup_code_files(
    search: Optional[str] = None,
    limit: int = Query(50, le=500)
):
    """Liste les fichiers de code suivis"""
    return await BackupAdminService.get_code_files(get_db(), search, limit)

@router.get("/backup/code/files/{file_path:path}/versions")
async def get_backup_file_versions(file_path: str, limit: int = Query(20, le=100)):
    """Récupérer les versions d'un fichier"""
    return await BackupAdminService.get_file_versions(get_db(), file_path, limit)

@router.post("/backup/code/files")
async def create_code_backup(
    file_path: str,
    content: str = Body(...),
    commit_message: str = ""
):
    """Créer une nouvelle version d'un fichier"""
    return await BackupAdminService.create_code_backup(get_db(), file_path, content, commit_message)

@router.get("/backup/code/restore/{file_path:path}/{version}")
async def restore_code_version(file_path: str, version: int):
    """Restaurer une version spécifique"""
    return await BackupAdminService.restore_version(get_db(), file_path, version)

@router.get("/backup/prompts")
async def get_backup_prompt_versions(
    prompt_type: Optional[str] = None,
    limit: int = Query(50, le=500)
):
    """Liste les versions de prompts"""
    return await BackupAdminService.get_prompt_versions(get_db(), prompt_type, limit)

@router.get("/backup/prompts/{version_id}")
async def get_backup_prompt_version_detail(version_id: str):
    """Détail d'une version de prompt"""
    return await BackupAdminService.get_prompt_version_detail(get_db(), version_id)

@router.post("/backup/prompts")
async def save_prompt_version(
    prompt_type: str,
    content: str = Body(...),
    metadata: dict = Body(default={})
):
    """Sauvegarder une nouvelle version de prompt"""
    return await BackupAdminService.save_prompt_version(get_db(), prompt_type, content, metadata)

@router.get("/backup/database")
async def get_database_backups(limit: int = Query(20, le=100)):
    """Liste les backups de base de données"""
    return await BackupAdminService.get_db_backups(get_db(), limit)

@router.post("/backup/database")
async def create_database_backup(
    backup_type: str = "manual",
    description: str = ""
):
    """Créer un backup de base de données"""
    return await BackupAdminService.create_db_backup(get_db(), backup_type, description)

@router.delete("/backup/database/{backup_id}")
async def delete_database_backup(backup_id: str):
    """Supprimer un backup"""
    return await BackupAdminService.delete_db_backup(get_db(), backup_id)



# ==============================================
# MAINTENANCE ADMIN (Phase 3 Migration)
# ==============================================

@router.get("/maintenance/status")
async def get_maintenance_status():
    """Récupérer le statut de maintenance actuel"""
    return await MaintenanceAdminService.get_maintenance_status(get_db())

@router.put("/maintenance/toggle")
async def toggle_maintenance_mode(
    enabled: bool,
    message: str = None,
    estimated_end: str = None
):
    """Activer/Désactiver le mode maintenance"""
    return await MaintenanceAdminService.toggle_maintenance_mode(get_db(), enabled, message, estimated_end)

@router.put("/maintenance/config")
async def update_maintenance_config(config_updates: dict = Body(...)):
    """Mettre à jour la configuration de maintenance"""
    return await MaintenanceAdminService.update_maintenance_config(get_db(), config_updates)

@router.get("/maintenance/access-rules")
async def get_access_rules():
    """Récupérer les règles d'accès"""
    return await MaintenanceAdminService.get_access_rules(get_db())

@router.post("/maintenance/access-rules")
async def create_access_rule(rule_data: dict = Body(...)):
    """Créer une nouvelle règle d'accès"""
    return await MaintenanceAdminService.create_access_rule(get_db(), rule_data)

@router.put("/maintenance/access-rules/{rule_id}")
async def update_access_rule(rule_id: str, updates: dict = Body(...)):
    """Mettre à jour une règle d'accès"""
    return await MaintenanceAdminService.update_access_rule(get_db(), rule_id, updates)

@router.delete("/maintenance/access-rules/{rule_id}")
async def delete_access_rule(rule_id: str):
    """Supprimer une règle d'accès"""
    return await MaintenanceAdminService.delete_access_rule(get_db(), rule_id)

@router.put("/maintenance/access-rules/{rule_id}/toggle")
async def toggle_access_rule(rule_id: str, enabled: bool):
    """Activer/Désactiver une règle d'accès"""
    return await MaintenanceAdminService.toggle_access_rule(get_db(), rule_id, enabled)

@router.get("/maintenance/allowed-ips")
async def get_allowed_ips():
    """Récupérer les IPs autorisées en mode maintenance"""
    return await MaintenanceAdminService.get_allowed_ips(get_db())

@router.post("/maintenance/allowed-ips")
async def add_allowed_ip(ip: str, label: str = ""):
    """Ajouter une IP autorisée"""
    return await MaintenanceAdminService.add_allowed_ip(get_db(), ip, label)

@router.delete("/maintenance/allowed-ips/{ip}")
async def remove_allowed_ip(ip: str):
    """Retirer une IP autorisée"""
    return await MaintenanceAdminService.remove_allowed_ip(get_db(), ip)

@router.get("/maintenance/logs")
async def get_maintenance_logs(limit: int = Query(50, le=500)):
    """Récupérer les logs de maintenance"""
    return await MaintenanceAdminService.get_maintenance_logs(get_db(), limit)

@router.get("/maintenance/scheduled")
async def get_scheduled_maintenances():
    """Récupérer les maintenances planifiées"""
    return await MaintenanceAdminService.get_scheduled_maintenances(get_db())

@router.post("/maintenance/scheduled")
async def create_scheduled_maintenance(schedule_data: dict = Body(...)):
    """Créer une maintenance planifiée"""
    return await MaintenanceAdminService.create_scheduled_maintenance(get_db(), schedule_data)

@router.delete("/maintenance/scheduled/{schedule_id}")
async def delete_scheduled_maintenance(schedule_id: str):
    """Supprimer une maintenance planifiée"""
    return await MaintenanceAdminService.delete_scheduled_maintenance(get_db(), schedule_id)

@router.get("/maintenance/system-status")
async def get_system_status():
    """Récupérer le statut système global"""
    return await MaintenanceAdminService.get_system_status(get_db())


# ==============================================
# CONTACTS ADMIN (Directory - Source de vérité V5)
# ==============================================

@router.get("/contacts")
async def get_contacts(
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=500)
):
    """Liste les contacts avec filtres"""
    return await ContactsAdminService.get_contacts(get_db(), entity_type, status, search, limit)

@router.get("/contacts/stats")
async def get_contacts_stats():
    """Statistiques globales des contacts"""
    return await ContactsAdminService.get_contacts_stats(get_db())

@router.get("/contacts/tags")
async def get_all_tags():
    """Récupérer tous les tags utilisés"""
    return await ContactsAdminService.get_all_tags(get_db())

# Shortcuts pour types spécifiques - MUST be before {contact_id} route
@router.get("/contacts/suppliers")
async def get_suppliers(limit: int = Query(50, le=500)):
    """Liste les fournisseurs"""
    return await ContactsAdminService.get_suppliers(get_db(), limit)

@router.get("/contacts/manufacturers")
async def get_manufacturers(limit: int = Query(50, le=500)):
    """Liste les fabricants"""
    return await ContactsAdminService.get_manufacturers(get_db(), limit)

@router.get("/contacts/partners")
async def get_partners(limit: int = Query(50, le=500)):
    """Liste les partenaires"""
    return await ContactsAdminService.get_partners(get_db(), limit)

@router.get("/contacts/trainers")
async def get_trainers(limit: int = Query(50, le=500)):
    """Liste les formateurs"""
    return await ContactsAdminService.get_trainers(get_db(), limit)

@router.get("/contacts/experts")
async def get_experts(limit: int = Query(50, le=500)):
    """Liste les experts"""
    return await ContactsAdminService.get_experts(get_db(), limit)

@router.put("/contacts/bulk/status")
async def bulk_update_status(contact_ids: List[str] = Body(...), new_status: str = Body(...)):
    """Mettre à jour le statut de plusieurs contacts"""
    return await ContactsAdminService.bulk_update_status(get_db(), contact_ids, new_status)

@router.delete("/contacts/bulk/delete")
async def bulk_delete_contacts(contact_ids: List[str] = Body(...)):
    """Supprimer plusieurs contacts"""
    return await ContactsAdminService.bulk_delete(get_db(), contact_ids)

@router.get("/contacts/export/all")
async def export_contacts(entity_type: Optional[str] = None):
    """Exporter les contacts"""
    return await ContactsAdminService.export_contacts(get_db(), entity_type)

@router.post("/contacts/import")
async def import_contacts(contacts_data: List[dict] = Body(...)):
    """Importer des contacts"""
    return await ContactsAdminService.import_contacts(get_db(), contacts_data)

# Generic contact routes - MUST be after specific routes
@router.get("/contacts/{contact_id}")
async def get_contact_by_id(contact_id: str):
    """Récupérer un contact par ID"""
    return await ContactsAdminService.get_contact_by_id(get_db(), contact_id)

@router.post("/contacts")
async def create_contact(contact_data: dict = Body(...)):
    """Créer un nouveau contact"""
    return await ContactsAdminService.create_contact(get_db(), contact_data)

@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: str, updates: dict = Body(...)):
    """Mettre à jour un contact"""
    return await ContactsAdminService.update_contact(get_db(), contact_id, updates)

@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: str):
    """Supprimer un contact"""
    return await ContactsAdminService.delete_contact(get_db(), contact_id)

@router.post("/contacts/{contact_id}/tags")
async def add_tag_to_contact(contact_id: str, tag: str):
    """Ajouter un tag à un contact"""
    return await ContactsAdminService.add_tag_to_contact(get_db(), contact_id, tag)

@router.delete("/contacts/{contact_id}/tags/{tag}")
async def remove_tag_from_contact(contact_id: str, tag: str):
    """Retirer un tag d'un contact"""
    return await ContactsAdminService.remove_tag_from_contact(get_db(), contact_id, tag)
