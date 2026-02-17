"""
BIONIC SEO Engine - V5-ULTIME
=============================

Module SEO premium intégré au Knowledge Layer.
Architecture LEGO V5 stricte - Module isolé, autonome et testable.

Composants:
- seo_router.py: Routes API
- seo_service.py: Service principal
- seo_models.py: Modèles Pydantic
- seo_clusters.py: Gestion des clusters SEO
- seo_pages.py: Pages piliers/satellites/opportunités
- seo_jsonld.py: Schémas JSON-LD
- seo_automation.py: Automatisation SEO
- seo_analytics.py: Analytics et KPIs
- seo_generation.py: Génération IA + Knowledge Layer

Version: 1.0.0
"""

from .seo_router import router
from .seo_service import SEOService
from .seo_models import (
    SEOCluster,
    SEOPage,
    SEOJsonLD,
    SEOCampaign,
    SEOAnalytics
)

__all__ = [
    "router",
    "SEOService",
    "SEOCluster",
    "SEOPage",
    "SEOJsonLD",
    "SEOCampaign",
    "SEOAnalytics"
]

__version__ = "1.0.0"
__module__ = "seo_engine"
