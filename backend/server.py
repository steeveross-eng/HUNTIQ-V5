"""
HUNTIQ V5-ULTIME-FUSION Server
==============================

Architecture Modulaire v2.0 - Phase 6 Complete

Ce fichier est le point d'entrée de l'API.
L'orchestration est déléguée à server_orchestrator.py

Modules unifiés V5:
- admin_unified_engine (fusion admin_engine + admin_advanced_engine)
- notification_unified_engine (fusion notification_engine + communication_engine)

Version: 5.0.0
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================================
# MODULE IMPORTS
# ==============================================
from modules.routers import CORE_ROUTERS, MODULE_STATUS
from server_orchestrator import create_orchestrator


# ==============================================
# APPLICATION LIFECYCLE
# ==============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    logger.info("=" * 60)
    logger.info("HUNTIQ V5-ULTIME-FUSION - Server Starting")
    logger.info("=" * 60)
    logger.info("Architecture: Modular v2.0 (Pure Orchestrator)")
    logger.info(f"Total Modules: {MODULE_STATUS['total_modules']}")
    
    # Initialize database
    try:
        from database import init_database
        await init_database()
        logger.info("✓ Database initialized with indexes and seed data")
    except Exception as e:
        logger.warning(f"Database initialization warning: {e}")
    
    # Initialize geo engine indexes
    try:
        from modules.geo_engine.v1 import ensure_indexes
        await ensure_indexes()
        logger.info("✓ Geo Engine 2dsphere indexes created")
    except ImportError:
        logger.info("Geo Engine indexes skipped (module not loaded)")
    except Exception as e:
        logger.warning(f"Geo Engine index creation warning: {e}")
    
    # Initialize territory sync
    try:
        from territory_sync import startup_sync
        await startup_sync()
        logger.info("✓ Territory sync initialized")
    except ImportError:
        logger.info("Territory sync not available")
    except Exception as e:
        logger.warning(f"Territory sync startup failed: {e}")
    
    logger.info("=" * 60)
    logger.info("✓ All modules loaded successfully")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Server shutting down...")
    try:
        from territory_sync import shutdown_sync
        await shutdown_sync()
    except Exception:
        pass


# ==============================================
# FASTAPI APPLICATION
# ==============================================
app = FastAPI(
    title="HUNTIQ V5-ULTIME-FUSION API",
    description="""
## Chasse Bionic™ - API Modulaire Intelligente

HUNTIQ V5-ULTIME-FUSION est la fusion complète de toutes les versions (V2, V3, V4, BASE) 
en une architecture modulaire unifiée.

### Modules Unifiés V5
- **admin_unified_engine**: Fusion de admin_engine (V4) + admin_advanced_engine (BASE)
- **notification_unified_engine**: Fusion de notification_engine (V4) + communication_engine (BASE)

### Architecture Modulaire (56+ modules)
- **Phase 2**: Core Engines (weather, scoring, ai, nutrition, strategy)
- **Phase 3-6**: Business & Plan Maître Engines
- **Phase 7**: Decoupled Engines
- **V5-BASE**: Modules importés de HUNTIQ-BASE
- **V5-UNIFIED**: Modules fusionnés et unifiés

### Fonctionnalités Clés
- 🕐 **Legal Time Engine**: Calcul heures légales de chasse
- 🔮 **Predictive Engine**: Prédiction succès de chasse
- 🤖 **AI Engine**: GPT-5.2 pour analyse et recommandations
- 📊 **Analytics Engine**: Statistiques et KPIs de chasse
- 🔔 **Notifications**: Multi-canal (in-app, email, push, SMS)

### Authentification
Certains endpoints nécessitent une authentification via JWT Bearer token.
    """,
    version="5.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=[
        {"name": "Orchestrator", "description": "System status and health"},
        {"name": "Admin Unified Engine", "description": "Administration unifiée V5"},
        {"name": "Notification Unified Engine", "description": "Notifications unifiées V5"},
        {"name": "Analytics Engine", "description": "Statistiques et KPIs de chasse"},
        {"name": "Legal Time Engine", "description": "Calcul des heures légales de chasse"},
        {"name": "Predictive Engine", "description": "Prédiction de succès de chasse"},
        {"name": "AI Engine", "description": "Intelligence artificielle GPT-5.2"},
        {"name": "Weather Engine", "description": "Analyse météorologique"},
        {"name": "Scoring Engine", "description": "Évaluation des produits"},
    ]
)


# ==============================================
# CORS MIDDLEWARE
# ==============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================
# ORCHESTRATOR REGISTRATION (Phase 6)
# ==============================================
orchestrator = create_orchestrator(app)

# 1. Register orchestrator endpoints (health, status, modules)
orchestrator.finalize()

# 2. Register core modular routers
orchestrator.register_core_routers(CORE_ROUTERS)

# 3. Register special routers (root-level)
orchestrator.register_special_routers()

# 4. Register legacy router (backward compatibility)
orchestrator.register_legacy_router()

# 5. Register BIONIC Engine P0 router (Phase G)
try:
    from modules.bionic_engine.router import router as bionic_p0_router
    app.include_router(bionic_p0_router, prefix="/api")
    logger.info("✓ BIONIC Engine P0 registered (/api/v1/bionic)")
except ImportError as e:
    logger.warning(f"BIONIC Engine P0 not loaded: {e}")
except Exception as e:
    logger.error(f"BIONIC Engine P0 registration failed: {e}")

logger.info("=" * 60)
logger.info(f"✓ V5-ULTIME-FUSION: {len(CORE_ROUTERS)} modules registered")
logger.info("✓ PHASE G: BIONIC Engine P0 active")
logger.info("=" * 60)


# ==============================================
# CUSTOM OPENAPI SCHEMA
# ==============================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="HUNTIQ V5-ULTIME-FUSION API",
        version="5.0.0",
        description="API modulaire de chasse intelligente - Fusion V2+V3+V4+BASE",
        routes=app.routes,
    )
    
    openapi_schema["tags"] = [
        {"name": "Orchestrator", "description": "System status and health"},
        {"name": "V5-Unified", "description": "Modules unifiés V5 (admin, notifications)"},
        {"name": "Core Engines", "description": "Phase 2 - Nutrition, Scoring, AI, Weather, Geospatial"},
        {"name": "Business Engines", "description": "Phase 3 - User, Territory, Referral"},
        {"name": "Master Plan", "description": "Phase 4 - Recommendations, Collaborative, Wildlife"},
        {"name": "Data Layers", "description": "Phase 5 - Ecoforestry, Behavioral, Simulation"},
        {"name": "Live Heading", "description": "Phase 6 - Immersive navigation"},
        {"name": "V5-BASE", "description": "Modules importés de HUNTIQ-BASE"},
        {"name": "Legacy", "description": "Backward compatibility endpoints"},
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
