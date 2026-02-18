"""
BIONIC Messaging Engine - Communications Premium Bilingues
==========================================================

Système de messagerie bilingue (FR/EN) pour toutes les communications externes:
- Messages affiliés
- Notifications partenaires
- Emails automatiques
- Communications marketing

Architecture LEGO V5-ULTIME - Module isolé.

RÈGLE PERMANENTE: Toujours envoyer des messages bilingues Premium (FR/EN)
pour toute communication externe générée automatiquement.
"""

from fastapi import APIRouter, Body, Query, HTTPException
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from enum import Enum
import os
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/messaging", tags=["Messaging Engine"])

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

class MessageType(str, Enum):
    AFFILIATE_WELCOME = "affiliate_welcome"
    AFFILIATE_PRELAUNCH = "affiliate_prelaunch"
    PARTNER_NOTIFICATION = "partner_notification"
    MARKETING_CAMPAIGN = "marketing_campaign"
    SYSTEM_NOTIFICATION = "system_notification"


class MessageStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    FAILED = "failed"


class MessageChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    PUSH = "push"


# ============================================
# BILINGUAL MESSAGE TEMPLATES
# ============================================

BILINGUAL_TEMPLATES = {
    "affiliate_prelaunch": {
        "fr": {
            "subject": "🎯 BIONIC - Votre espace publicitaire est prêt",
            "greeting": "Bonjour,",
            "body": """Nous tenions à vous remercier pour votre confiance envers BIONIC.
Votre espace publicitaire est maintenant configuré dans notre système et prêt à être activé.

Nous finalisons actuellement la phase pré-lancement de la plateforme.
Aucune publicité n'est encore diffusée — tout est en mode pré-production afin d'assurer une expérience optimale dès le lancement officiel.

Nous vous recontacterons personnellement avant l'activation de votre campagne afin de :
• confirmer les détails,
• valider les créatifs,
• et vous présenter les premières statistiques dès les premières impressions.""",
            "closing": "Merci encore d'être parmi les premiers partenaires de BIONIC.",
            "signature": "Cordialement,\nL'équipe BIONIC"
        },
        "en": {
            "subject": "🎯 BIONIC - Your advertising placement is ready",
            "greeting": "Hello,",
            "body": """Thank you for your trust in BIONIC.
Your advertising placement is now configured in our system and ready for activation.

We are currently completing the pre-launch phase of the platform.
No ads are being displayed yet — everything is in pre-production to ensure the best possible experience on launch day.

We will contact you personally before your campaign goes live to:
• confirm all details,
• validate your creatives,
• and share the first performance metrics as soon as impressions begin.""",
            "closing": "Thank you again for being among the first BIONIC partners.",
            "signature": "Sincerely,\nThe BIONIC Team"
        }
    },
    "affiliate_welcome": {
        "fr": {
            "subject": "🎉 Bienvenue chez BIONIC",
            "greeting": "Bonjour,",
            "body": """Nous sommes ravis de vous accueillir parmi nos partenaires affiliés.

Votre compte a été créé avec succès et vous avez maintenant accès à notre plateforme d'affiliation premium.

Prochaines étapes :
• Complétez votre profil partenaire
• Découvrez nos options publicitaires
• Contactez notre équipe pour discuter de votre stratégie""",
            "closing": "Nous sommes impatients de collaborer avec vous.",
            "signature": "Cordialement,\nL'équipe BIONIC"
        },
        "en": {
            "subject": "🎉 Welcome to BIONIC",
            "greeting": "Hello,",
            "body": """We are delighted to welcome you among our affiliate partners.

Your account has been successfully created and you now have access to our premium affiliate platform.

Next steps:
• Complete your partner profile
• Discover our advertising options
• Contact our team to discuss your strategy""",
            "closing": "We look forward to collaborating with you.",
            "signature": "Sincerely,\nThe BIONIC Team"
        }
    }
}


# ============================================
# GLOBAL BILINGUAL RULE
# ============================================

GLOBAL_BILINGUAL_RULE = {
    "rule_id": "BIONIC_BILINGUAL_PREMIUM",
    "name": "Messages Bilingues Premium",
    "description": "Toujours envoyer des messages bilingues Premium (FR/EN) pour toute communication externe générée automatiquement.",
    "is_permanent": True,
    "is_priority": True,
    "applies_to": ["SEO", "Marketing", "Affiliate", "Ads", "Calendar"],
    "enforcement_level": "mandatory",
    "created_at": "2026-02-18T00:00:00Z",
    "created_by": "COPILOT_MAITRE"
}


# ============================================
# MODULE INFO
# ============================================

@router.get("/")
async def get_module_info():
    """Information sur le Messaging Engine"""
    return {
        "module": "messaging_engine",
        "version": "1.0.0",
        "description": "Système de messagerie bilingue Premium (FR/EN) BIONIC",
        "architecture": "LEGO_V5_ULTIME",
        "features": [
            "Messages bilingues automatiques (FR/EN)",
            "Templates Premium pré-configurés",
            "Règle permanente de communication bilingue",
            "Intégration multi-canal (email, SMS, in-app, push)",
            "Journalisation complète",
            "Tracking des ouvertures et clics"
        ],
        "global_rule": GLOBAL_BILINGUAL_RULE,
        "templates_available": list(BILINGUAL_TEMPLATES.keys()),
        "channels": [c.value for c in MessageChannel]
    }


# ============================================
# GLOBAL BILINGUAL RULE ENDPOINTS
# ============================================

@router.get("/rule/bilingual")
async def get_bilingual_rule():
    """
    Obtenir la règle permanente de communication bilingue.
    """
    db = get_db()
    
    # Check if rule exists in DB, if not create it
    rule = await db.messaging_rules.find_one({"rule_id": "BIONIC_BILINGUAL_PREMIUM"})
    
    if not rule:
        rule = {**GLOBAL_BILINGUAL_RULE}
        await db.messaging_rules.insert_one(rule)
    
    rule.pop("_id", None)
    
    return {
        "success": True,
        "rule": rule,
        "status": "ACTIVE",
        "enforcement": "MANDATORY"
    }


@router.post("/rule/bilingual/verify")
async def verify_bilingual_compliance(
    message_content: Dict[str, Any] = Body(...)
):
    """
    Vérifier si un message est conforme à la règle bilingue.
    """
    has_french = bool(message_content.get("fr"))
    has_english = bool(message_content.get("en"))
    
    is_compliant = has_french and has_english
    
    return {
        "success": True,
        "is_compliant": is_compliant,
        "has_french": has_french,
        "has_english": has_english,
        "rule": GLOBAL_BILINGUAL_RULE["name"],
        "message": "Message conforme à la règle bilingue" if is_compliant else "Message NON conforme - Versions FR et EN requises"
    }


# ============================================
# BILINGUAL MESSAGE CREATION
# ============================================

@router.post("/messages/create-bilingual")
async def create_bilingual_message(
    message_data: Dict[str, Any] = Body(...)
):
    """
    Créer un message bilingue Premium.
    
    Args:
        message_data: {
            "template": "affiliate_prelaunch" | "affiliate_welcome" | custom,
            "recipients": [{"affiliate_id": "...", "email": "...", "company_name": "..."}],
            "custom_content_fr": "...",  # Optional override
            "custom_content_en": "...",  # Optional override
            "channel": "email" | "sms" | "in_app" | "push",
            "scheduled_at": "ISO datetime" | null for immediate
        }
    """
    db = get_db()
    
    template_name = message_data.get("template", "affiliate_prelaunch")
    recipients = message_data.get("recipients", [])
    channel = message_data.get("channel", "email")
    scheduled_at = message_data.get("scheduled_at")
    
    # Get template
    template = BILINGUAL_TEMPLATES.get(template_name)
    
    if not template:
        return {
            "success": False,
            "error": f"Template '{template_name}' non trouvé",
            "available_templates": list(BILINGUAL_TEMPLATES.keys())
        }
    
    # Allow custom content override
    content_fr = message_data.get("custom_content_fr") or template["fr"]
    content_en = message_data.get("custom_content_en") or template["en"]
    
    # Create message batch
    batch_id = str(uuid.uuid4())
    messages_created = []
    
    for recipient in recipients:
        message_id = str(uuid.uuid4())
        
        message = {
            "message_id": message_id,
            "batch_id": batch_id,
            "template": template_name,
            "recipient": {
                "affiliate_id": recipient.get("affiliate_id"),
                "email": recipient.get("email"),
                "company_name": recipient.get("company_name")
            },
            "content": {
                "fr": content_fr,
                "en": content_en
            },
            "channel": channel,
            "status": MessageStatus.PENDING.value,
            "scheduled_at": scheduled_at or datetime.now(timezone.utc).isoformat(),
            "sent_at": None,
            "delivered_at": None,
            "opened_at": None,
            "clicked_at": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "created_by": message_data.get("created_by", "system")
        }
        
        await db.bilingual_messages.insert_one(message)
        message.pop("_id", None)
        messages_created.append(message)
    
    # Log batch creation
    await _log_message_action(db, batch_id, "batch_created", "system", {
        "template": template_name,
        "recipients_count": len(recipients),
        "channel": channel
    })
    
    return {
        "success": True,
        "batch_id": batch_id,
        "messages_created": len(messages_created),
        "messages": messages_created,
        "bilingual_compliant": True,
        "message": f"{len(messages_created)} messages bilingues Premium créés"
    }


@router.post("/messages/send-now")
async def send_bilingual_messages(
    send_config: Dict[str, Any] = Body(...)
):
    """
    Envoyer immédiatement les messages bilingues.
    Simule l'envoi (en production, intégrerait avec Resend/SendGrid).
    """
    db = get_db()
    
    batch_id = send_config.get("batch_id")
    message_ids = send_config.get("message_ids")
    
    query = {}
    if batch_id:
        query["batch_id"] = batch_id
    elif message_ids:
        query["message_id"] = {"$in": message_ids}
    else:
        query["status"] = MessageStatus.PENDING.value
    
    messages = await db.bilingual_messages.find(query).to_list(500)
    
    sent_count = 0
    failed_count = 0
    
    for msg in messages:
        try:
            # Simulate sending (in production, integrate with email service)
            # Email content would be formatted with both FR and EN versions
            
            await db.bilingual_messages.update_one(
                {"message_id": msg["message_id"]},
                {
                    "$set": {
                        "status": MessageStatus.SENT.value,
                        "sent_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            sent_count += 1
            
            # Log send
            await _log_message_action(db, msg["message_id"], "message_sent", "email_system", {
                "recipient_email": msg["recipient"].get("email"),
                "company_name": msg["recipient"].get("company_name")
            })
            
        except Exception as e:
            await db.bilingual_messages.update_one(
                {"message_id": msg["message_id"]},
                {
                    "$set": {
                        "status": MessageStatus.FAILED.value,
                        "error": str(e)
                    }
                }
            )
            failed_count += 1
    
    return {
        "success": True,
        "sent_count": sent_count,
        "failed_count": failed_count,
        "total_processed": sent_count + failed_count,
        "message": f"✅ {sent_count} messages bilingues envoyés"
    }


# ============================================
# SEND TO SPECIFIC AFFILIATES
# ============================================

@router.post("/affiliates/send-prelaunch")
async def send_prelaunch_to_affiliates(
    affiliate_ids: List[str] = Body(..., embed=True)
):
    """
    Envoyer le message pré-lancement bilingue aux affiliés spécifiés.
    """
    db = get_db()
    
    # Get affiliates from DB
    affiliates = await db.affiliate_switches.find({
        "affiliate_id": {"$in": affiliate_ids}
    }).to_list(100)
    
    if not affiliates:
        return {
            "success": False,
            "error": "Aucun affilié trouvé avec les IDs fournis"
        }
    
    # Prepare recipients
    recipients = [
        {
            "affiliate_id": a["affiliate_id"],
            "email": a.get("email") or f"contact@{a.get('website', '').replace('https://', '').replace('http://', '').split('/')[0]}",
            "company_name": a.get("company_name")
        }
        for a in affiliates
    ]
    
    # Create bilingual message
    message_data = {
        "template": "affiliate_prelaunch",
        "recipients": recipients,
        "channel": "email",
        "created_by": "COPILOT_MAITRE"
    }
    
    result = await create_bilingual_message(message_data)
    
    if result["success"]:
        # Immediately send
        send_result = await send_bilingual_messages({"batch_id": result["batch_id"]})
        
        return {
            "success": True,
            "batch_id": result["batch_id"],
            "affiliates_contacted": [a["company_name"] for a in affiliates],
            "messages_sent": send_result.get("sent_count", 0),
            "template_used": "affiliate_prelaunch",
            "bilingual": True,
            "message": f"✅ Message bilingue Premium envoyé à {len(affiliates)} affiliés"
        }
    
    return result


# ============================================
# MESSAGE TRACKING
# ============================================

@router.get("/messages")
async def get_all_messages(
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=200),
    status: Optional[str] = None,
    batch_id: Optional[str] = None
):
    """Liste tous les messages bilingues."""
    db = get_db()
    
    query = {}
    if status:
        query["status"] = status
    if batch_id:
        query["batch_id"] = batch_id
    
    skip = (page - 1) * limit
    
    messages = await db.bilingual_messages.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.bilingual_messages.count_documents(query)
    
    for msg in messages:
        msg.pop("_id", None)
    
    return {
        "success": True,
        "messages": messages,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/messages/{message_id}")
async def get_message(message_id: str):
    """Détail d'un message."""
    db = get_db()
    
    msg = await db.bilingual_messages.find_one({"message_id": message_id})
    
    if not msg:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    
    msg.pop("_id", None)
    
    return {
        "success": True,
        "message": msg
    }


@router.post("/messages/{message_id}/track-open")
async def track_message_open(message_id: str):
    """Tracker l'ouverture d'un message."""
    db = get_db()
    
    await db.bilingual_messages.update_one(
        {"message_id": message_id},
        {
            "$set": {
                "status": MessageStatus.OPENED.value,
                "opened_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {"success": True, "tracked": "open"}


@router.post("/messages/{message_id}/track-click")
async def track_message_click(message_id: str):
    """Tracker un clic dans un message."""
    db = get_db()
    
    await db.bilingual_messages.update_one(
        {"message_id": message_id},
        {
            "$set": {
                "status": MessageStatus.CLICKED.value,
                "clicked_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {"success": True, "tracked": "click"}


# ============================================
# DASHBOARD
# ============================================

@router.get("/dashboard")
async def get_messaging_dashboard():
    """Dashboard du Messaging Engine."""
    db = get_db()
    
    # Count by status
    status_counts = {}
    for status in MessageStatus:
        count = await db.bilingual_messages.count_documents({"status": status.value})
        if count > 0:
            status_counts[status.value] = count
    
    # Count by template
    template_pipeline = [
        {"$group": {"_id": "$template", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    by_template = await db.bilingual_messages.aggregate(template_pipeline).to_list(20)
    
    # Recent messages
    recent = await db.bilingual_messages.find({}).sort("created_at", -1).limit(10).to_list(10)
    for msg in recent:
        msg.pop("_id", None)
    
    return {
        "success": True,
        "dashboard": {
            "global_rule": {
                "name": GLOBAL_BILINGUAL_RULE["name"],
                "status": "ACTIVE",
                "enforcement": "MANDATORY"
            },
            "messages": {
                "by_status": status_counts,
                "by_template": by_template,
                "total": sum(status_counts.values())
            },
            "recent_messages": recent,
            "templates_available": list(BILINGUAL_TEMPLATES.keys())
        }
    }


# ============================================
# HELPERS
# ============================================

async def _log_message_action(db, message_id: str, action: str, source: str, details: Dict = None):
    """Journaliser une action de messagerie."""
    log_entry = {
        "message_id": message_id,
        "action": action,
        "source": source,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    await db.messaging_logs.insert_one(log_entry)


# ============================================
# TEMPLATES MANAGEMENT
# ============================================

@router.get("/templates")
async def get_all_templates():
    """Liste tous les templates bilingues disponibles."""
    templates = []
    for name, content in BILINGUAL_TEMPLATES.items():
        templates.append({
            "name": name,
            "languages": ["fr", "en"],
            "fr_subject": content["fr"]["subject"],
            "en_subject": content["en"]["subject"]
        })
    
    return {
        "success": True,
        "templates": templates,
        "count": len(templates)
    }


@router.get("/templates/{template_name}")
async def get_template(template_name: str):
    """Obtenir un template bilingue spécifique."""
    template = BILINGUAL_TEMPLATES.get(template_name)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' non trouvé")
    
    return {
        "success": True,
        "template_name": template_name,
        "content": template
    }


@router.get("/templates/{template_name}/preview")
async def preview_template(
    template_name: str,
    company_name: str = Query("ACME Corp")
):
    """
    Prévisualiser un template bilingue formaté.
    """
    template = BILINGUAL_TEMPLATES.get(template_name)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' non trouvé")
    
    # Format preview
    preview_fr = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇫🇷 VERSION FRANÇAISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{template['fr']['subject']}

{template['fr']['greeting']}

{template['fr']['body']}

{template['fr']['closing']}

{template['fr']['signature']}
"""
    
    preview_en = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇺🇸 ENGLISH VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{template['en']['subject']}

{template['en']['greeting']}

{template['en']['body']}

{template['en']['closing']}

{template['en']['signature']}
"""
    
    return {
        "success": True,
        "template_name": template_name,
        "preview": {
            "fr": preview_fr,
            "en": preview_en
        },
        "bilingual_compliant": True
    }


logger.info("Messaging Engine initialized - LEGO V5-ULTIME Module")
