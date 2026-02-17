"""
Content Admin Service - V5-ULTIME Administration Premium
========================================================

Service d'administration du contenu pour la gestion de:
- Catégories d'analyse (analysis-categories)
- Content Depot (SEO, marketing content)
- Workflow de validation du contenu

Module isolé - aucun import croisé.
Phase 2 Migration.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)


class ContentAdminService:
    """Service isolé pour l'administration du contenu"""
    
    # ============ CATEGORIES ============
    @staticmethod
    async def get_categories(db) -> dict:
        """Liste toutes les catégories d'analyse"""
        categories = await db.analysis_categories.find(
            {}, {"_id": 0}
        ).sort("order", 1).to_list(length=100)
        
        return {
            "success": True,
            "total": len(categories),
            "categories": categories
        }
    
    @staticmethod
    async def create_category(db, category_data: dict) -> dict:
        """Créer une nouvelle catégorie"""
        # Vérifier si existe déjà
        existing = await db.analysis_categories.find_one({"id": category_data.get("id")})
        if existing:
            return {"success": False, "error": "Category ID already exists"}
        
        category = {
            "id": category_data.get("id") or str(uuid.uuid4()),
            "name": category_data.get("name", ""),
            "icon": category_data.get("icon", "📦"),
            "order": category_data.get("order", 0),
            "subcategories": category_data.get("subcategories", []),
            "created_at": datetime.now(timezone.utc)
        }
        
        await db.analysis_categories.insert_one(category)
        category.pop("_id", None)
        
        return {"success": True, "category": category}
    
    @staticmethod
    async def update_category(db, category_id: str, updates: dict) -> dict:
        """Mettre à jour une catégorie"""
        updates["updated_at"] = datetime.now(timezone.utc)
        
        result = await db.analysis_categories.update_one(
            {"id": category_id},
            {"$set": updates}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Category not found"}
        
        return {"success": True, "category_id": category_id, "updated": True}
    
    @staticmethod
    async def delete_category(db, category_id: str) -> dict:
        """Supprimer une catégorie"""
        result = await db.analysis_categories.delete_one({"id": category_id})
        
        if result.deleted_count == 0:
            return {"success": False, "error": "Category not found"}
        
        return {"success": True, "category_id": category_id, "deleted": True}
    
    @staticmethod
    async def init_default_categories(db) -> dict:
        """Initialiser les catégories par défaut"""
        default_categories = [
            {"id": "chasse", "name": "Équipement de Chasse", "icon": "🎯", "order": 1, "subcategories": []},
            {"id": "vetements", "name": "Vêtements", "icon": "👕", "order": 2, "subcategories": []},
            {"id": "optique", "name": "Optique", "icon": "🔭", "order": 3, "subcategories": []},
            {"id": "accessoires", "name": "Accessoires", "icon": "🎒", "order": 4, "subcategories": []},
            {"id": "formation", "name": "Formation", "icon": "📚", "order": 5, "subcategories": []}
        ]
        
        inserted = 0
        for cat in default_categories:
            existing = await db.analysis_categories.find_one({"id": cat["id"]})
            if not existing:
                cat["created_at"] = datetime.now(timezone.utc)
                await db.analysis_categories.insert_one(cat)
                inserted += 1
        
        return {"success": True, "inserted": inserted, "total_defaults": len(default_categories)}
    
    # ============ CONTENT DEPOT ============
    @staticmethod
    async def get_content_items(db, status: Optional[str] = None, limit: int = 50) -> dict:
        """Liste les items du Content Depot"""
        query = {}
        if status and status != 'all':
            query["status"] = status
        
        items = await db.content_depot.find(
            query, {"_id": 0}
        ).sort("created_at", -1).limit(limit).to_list(length=limit)
        
        total = await db.content_depot.count_documents(query)
        
        # Stats par status
        status_counts = {}
        for s in ["pending", "optimized", "accepted", "published"]:
            status_counts[s] = await db.content_depot.count_documents({"status": s})
        
        return {
            "success": True,
            "total": total,
            "status_counts": status_counts,
            "items": items
        }
    
    @staticmethod
    async def create_content_item(db, item_data: dict) -> dict:
        """Créer un nouvel item de contenu"""
        item = {
            "id": str(uuid.uuid4()),
            "title": item_data.get("title", ""),
            "content_type": item_data.get("content_type", "article"),
            "platform": item_data.get("platform", "website"),
            "original_content": item_data.get("original_content", ""),
            "optimized_content": "",
            "status": "pending",
            "seo_score": 0,
            "keywords": item_data.get("keywords", []),
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        await db.content_depot.insert_one(item)
        item.pop("_id", None)
        
        return {"success": True, "item": item}
    
    @staticmethod
    async def update_content_item(db, item_id: str, updates: dict) -> dict:
        """Mettre à jour un item de contenu"""
        updates["updated_at"] = datetime.now(timezone.utc)
        
        result = await db.content_depot.update_one(
            {"id": item_id},
            {"$set": updates}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Item not found"}
        
        return {"success": True, "item_id": item_id, "updated": True}
    
    @staticmethod
    async def update_content_status(db, item_id: str, new_status: str) -> dict:
        """Mettre à jour le statut d'un item"""
        valid_statuses = ["pending", "optimized", "accepted", "published"]
        if new_status not in valid_statuses:
            return {"success": False, "error": f"Invalid status. Must be one of: {valid_statuses}"}
        
        update = {
            "status": new_status,
            "updated_at": datetime.now(timezone.utc)
        }
        
        if new_status == "published":
            update["published_at"] = datetime.now(timezone.utc)
        
        result = await db.content_depot.update_one(
            {"id": item_id},
            {"$set": update}
        )
        
        if result.matched_count == 0:
            return {"success": False, "error": "Item not found"}
        
        return {"success": True, "item_id": item_id, "new_status": new_status}
    
    @staticmethod
    async def delete_content_item(db, item_id: str) -> dict:
        """Supprimer un item de contenu"""
        result = await db.content_depot.delete_one({"id": item_id})
        
        if result.deleted_count == 0:
            return {"success": False, "error": "Item not found"}
        
        return {"success": True, "item_id": item_id, "deleted": True}
    
    # ============ SEO ANALYTICS ============
    @staticmethod
    async def get_seo_analytics(db) -> dict:
        """Statistiques SEO globales"""
        # Content stats
        total_content = await db.content_depot.count_documents({})
        published_content = await db.content_depot.count_documents({"status": "published"})
        
        # Récupérer les scores SEO
        items_with_score = await db.content_depot.find(
            {"seo_score": {"$gt": 0}},
            {"seo_score": 1, "_id": 0}
        ).to_list(length=1000)
        
        avg_seo_score = 0
        if items_with_score:
            avg_seo_score = sum(i.get("seo_score", 0) for i in items_with_score) / len(items_with_score)
        
        # Categories count
        categories_count = await db.analysis_categories.count_documents({})
        
        return {
            "success": True,
            "analytics": {
                "total_content": total_content,
                "published_content": published_content,
                "pending_content": total_content - published_content,
                "avg_seo_score": round(avg_seo_score, 1),
                "categories_count": categories_count,
                "publish_rate": round((published_content / max(total_content, 1)) * 100, 1)
            }
        }
