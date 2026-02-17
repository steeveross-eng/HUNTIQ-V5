# HUNTIQ-V5 — Product Requirements Document

## Document Version History
| Date | Version | Changes |
|------|---------|---------|
| 2025-12-01 | 1.0.0 | Initial BIONIC Knowledge Layer |
| 2025-12-10 | 1.1.0 | SEO Engine V5 Integration |
| 2025-12-15 | 1.2.0 | Marketing Controls Module |
| 2026-02-17 | 1.3.0 | **Phase 7 Analytics Complete** |
| 2026-02-17 | 1.4.0 | **COMMANDE MAÎTRE - Optimisation Ergonomique Full Viewport** |

---

## Original Problem Statement
Application HUNTIQ-V5 selon une architecture "LEGO" modulaire très stricte. Le projet vise à créer une plateforme de chasse intelligente au Québec avec des fonctionnalités avancées de cartographie, d'analytique, de tracking et de monétisation.

---

## Architecture Overview
```
/app/
├── backend/
│   ├── modules/           # ~60+ modules modulaires
│   │   ├── analytics_engine/        # ✅ COMPLÉTÉ - Hunting trips analytics
│   │   ├── tracking_engine/v1/      # ✅ COMPLÉTÉ - Events, Funnels, Heatmaps
│   │   ├── bionic_knowledge_engine/ # ✅ COMPLÉTÉ - Data foundation
│   │   ├── seo_engine/              # ✅ COMPLÉTÉ - SEO automation
│   │   └── admin_engine/            # ✅ COMPLÉTÉ - Marketing controls
│   └── server.py
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── AdminPremiumPage.jsx # ✅ Vitrine Admin Premium
│       └── ui/administration/       # ✅ 24+ admin modules
└── docs/
    ├── SEO_PLAN_BIONIC_V5.md       # ✅ Strategic SEO plan
    └── generated_pillar_*.md       # ✅ 9 SEO pillar articles
```

---

## Completed Phases

### ✅ Phase 1-6: Foundation (Pre-existing)
- User authentication (JWT + Google OAuth)
- Territory management
- Map layers (BIONIC, IQHO, Satellite, etc.)
- E-Commerce integration
- 60+ modular engines

### ✅ BIONIC Knowledge Layer
- 5 species (deer, moose, bear, wild_turkey, elk)
- 17 habitat variables
- 11 scientific sources
- Seasonal models

### ✅ SEO Engine V5
- Backend: `/api/v1/bionic/seo/*`
- Frontend: `admin_seo` module
- 9 pillar articles generated (~13,000 words)
- LLM integration via `emergentintegrations`

### ✅ Marketing Controls Module
- Backend: `/api/v1/admin/marketing-controls/*`
- Frontend: `admin_marketing_controls` module
- Global ON/OFF toggles for campaigns

### ✅ Phase 7 — Analytics (2026-02-17)
**Partie A — AdminAnalytics dans Vitrine Admin Premium:**
- Module `admin_analytics` intégré
- 7 onglets: Dashboard, KPIs, Espèces, Météo, Horaires, Sorties, Admin
- Filtres temporels: Semaine, Mois, Saison, Année, Tout
- 51 hunting trips de démo seeded

**Partie B — Tracking Engine V1:**
- Events tracking (page_view, click, scroll, form_submit, etc.)
- Conversion funnels (création, analyse, drop-off rates)
- Heatmaps (click aggregation by 10px grid)
- Session analysis
- Engagement metrics (bounce rate, pages/session, device/country breakdown)
- 386+ demo events seeded

**API Endpoints:**
- `GET /api/v1/analytics/dashboard` - Hunting analytics
- `GET /api/v1/tracking-engine/` - Module info
- `POST /api/v1/tracking-engine/events` - Track event
- `POST /api/v1/tracking-engine/funnels` - Create funnel
- `GET /api/v1/tracking-engine/funnels/{id}/analyze` - Funnel analysis
- `GET /api/v1/tracking-engine/heatmap` - Heatmap data
- `GET /api/v1/tracking-engine/engagement` - Engagement metrics

**Test Results:** 100% success (iteration_10.json)

### ✅ UI/UX — Centrage Global BIONIC™ (2026-02-17)
**Composant créé:** `/app/frontend/src/core/layouts/GlobalContainer.jsx`

**Pages centrées (max-width: 1440px):**
- AnalyticsPage, BusinessPage, ComparePage, DashboardPage
- ForecastPage, NetworkPage, PaymentCancelPage, PaymentSuccessPage
- PlanMaitrePage, PricingPage, ShopPage, TripsPage

**Exceptions full-width intentionnelles:**
- AdminPremiumPage (sidebar fixe)
- MapPage, MonTerritoireBionicPage (cartes)
- BionicHomePage (landing page avec sections full-width)
- OnboardingPage (flow modal)

**Variantes disponibles:**
- `GlobalContainer` (1440px)
- `PageContainer` (avec titre)
- `SectionContainer` (espacement vertical)
- `AdminContainer` (full-width)
- `ContentContainer` (960px)
- `MapViewportContainer` (full-viewport pour cartes) ✅ **NOUVEAU**

### ✅ COMMANDE MAÎTRE — Optimisation Ergonomique Full Viewport (2026-02-17)

**Objectif :** Corriger les problèmes d'affichage où la carte n'est pas centrée, où certains éléments débordent de la fenêtre, et créer une ergonomie premium sans scroll.

**Composants créés/modifiés :**
- `MapViewportContainer.jsx` — Nouveau container full-viewport avec panneaux collapsibles
- `FloatingPanel.jsx` — Panneau flottant positionné librement
- `CoordinatesOverlay.jsx` — Affichage des coordonnées GPS en overlay

**Pages optimisées (layout full-viewport) :**
1. `/map` — Carte Interactive ✅ (overflow: 0px)
2. `/territoire` — Mon Territoire BIONIC™ ✅ (overflow: 0px)
3. `/forecast` — Prévisions WQS ✅ (overflow: 0px)
4. `/analyze` — Analyseur BIONIC™ ✅ (scroll pour contenu abondant)
5. `/admin-geo` — Admin Géospatial ✅

**Modifications ergonomiques :**
- `fixed inset-0` avec `paddingTop: 64px` pour le header
- `flex flex-col` avec `flex-1 overflow-hidden` pour le contenu
- Headers compacts (tailles réduites, espace optimisé)
- Panneaux latéraux collapsibles (`flex-shrink-0 overflow-hidden`)
- Footer masqué sur pages cartographiques

**ScrollNavigator adaptatif :**
- Auto-masquage sur les routes full-viewport
- Liste des routes : `/map`, `/territoire`, `/forecast`, `/analyze`, `/admin-geo`, `/admin-premium`

**Fichiers modifiés :**
- `/app/frontend/src/core/layouts/MapViewportContainer.jsx` (créé)
- `/app/frontend/src/core/layouts/index.js` (exports ajoutés)
- `/app/frontend/src/pages/MapPage.jsx` (refactoré)
- `/app/frontend/src/pages/MonTerritoireBionicPage.jsx` (refactoré)
- `/app/frontend/src/pages/ForecastPage.jsx` (refactoré)
- `/app/frontend/src/pages/AnalyticsPage.jsx` (refactoré)
- `/app/frontend/src/pages/AdminGeoPage.jsx` (refactoré)
- `/app/frontend/src/components/ScrollNavigator.jsx` (adaptatif)
- `/app/frontend/src/modules/territory/components/WaypointMap.jsx` (hauteur flexible)
- `/app/frontend/src/App.js` (Footer conditionnel)

### ✅ Phases 8-9 — Modularisation Frontend (2026-02-17)

**Phase 8 — Extraction Core :**
- Structure `/core/` créée : `layouts/`, `components/`, `hooks/`, `utils/`
- 10 composants Core : GlobalContainer, LoadingSpinner, EmptyState, ConfirmDialog, CookieConsent, OfflineIndicator, RefreshButton, BionicLogo, SEOHead, ScrollNavigator, BackButton
- 4 hooks Core : useToast, useLocalStorage, useDebounce, useMediaQuery (+ variantes)
- 3 utils Core : formatters (11 fn), validators (9 fn), api (6 fn)

**Phase 9 — Réorganisation Métier :**
- 42 composants métier migrés vers `/modules/`
- Modules enrichis : territory, affiliate, marketplace, scoring, notifications, collaborative, tracking, admin, analytics, realestate, products
- 15+ barrel exports créés
- Build : 100% succès

**Architecture finale :**
```
/frontend/src/
├── core/              # UI générique (AUCUNE logique métier)
│   ├── components/    # 10 composants
│   ├── hooks/         # 4 hooks
│   ├── layouts/       # 5 layouts
│   └── utils/         # 3 modules utils
├── modules/           # Logique métier (44 modules)
│   ├── territory/components/     # 5 composants
│   ├── affiliate/components/     # 9 composants
│   ├── admin/components/         # 14 composants
│   └── ...
└── components/        # Composants transversaux (Auth, Pages système)
```

### ✅ Phases 10-13 — Tunnel Utilisateur (Validé 2026-02-17)

**Phase 10 — Onboarding :**
- Backend : `onboarding_engine` ✅
- Frontend : OnboardingFlow, ProfileSelector, TerritorySelector, ExperienceSelector, ObjectivesSelector ✅
- 4 étapes : profile → territory → objectives → plan_maitre

**Phase 11 — Tutorial :**
- Backend : `tutorial_engine` ✅
- Frontend : TutorialProvider, TutorialOverlay, TutorialStep, TutorialTooltip, TutorialHighlight, TutorialProgress ✅
- 7 tutoriels : feature, workflow, premium_preview, tip

**Phase 12 — Freemium :**
- Backend : `freemium_engine` ✅
- Frontend : FreemiumGate, QuotaIndicator, FreemiumService ✅
- 3 tiers : free, premium, pro
- 8 features gérées

**Phase 13 — Payment (Stripe) :**
- Backend : `payment_engine` ✅
- Frontend : PaymentDashboard, PricingCard, PaymentService ✅
- 4 packages : Premium/Pro × Mensuel/Annuel
- Provider : Stripe avec Apple Pay, Google Pay, Webhooks

**Tests validés :** Tous les endpoints opérationnels (curl OK)

### ✅ Phase 14 — Marketing Automation Engine (2026-02-17)

**Router API dédié créé:** `/api/v1/marketing/`

**Fonctionnalités implémentées :**
- ✅ Dashboard avec KPIs (campagnes, posts, engagement, by_platform)
- ✅ Gestion campagnes (CRUD, statuts, analytics)
- ✅ Publications multi-plateformes (Facebook, Instagram, Twitter, LinkedIn)
- ✅ Génération de contenu IA (6 types : promo, educational, seasonal, testimonial, tip, engagement)
- ✅ Segments d'audience (5 par défaut + custom)
- ✅ Automations (welcome_series, cart_abandonment, reengagement)
- ✅ **Triggers comportementaux** connectés au Tracking Engine

**Intégration Tracking Engine :**
- `POST /api/v1/marketing/triggers` — Créer trigger lié aux événements tracking
- `POST /api/v1/marketing/triggers/check` — Vérifier et exécuter les triggers pour un user
- `GET /api/v1/marketing/triggers/executions` — Historique des exécutions

**Tests validés :** Tous les endpoints opérationnels (curl OK)

---

## Upcoming Tasks (Roadmap)

### 🟡 P1 — Phases 8-9: Frontend Modularisation
- Core component extraction
- Business logic separation
- State management optimization

### 🟡 P2 — Phases 10-13: User Tunnel
- Onboarding flow
- Tutorial system
- Freemium gates
- Payment integration

### 🔵 Future — Phase 14: Marketing Automation Engine
- Automated campaigns
- User segmentation
- A/B testing

### 🔵 À Faire — Module d'Interaction Cartographique Universel
**Note:** Cette commande maître a été interrompue pour prioriser l'optimisation ergonomique.
- Backend `waypoint_engine` créé et testé ✅
- Frontend `MapInteractionLayer` créé ⏳
- Intégration dans MonTerritoireBionic et MapPage ⏳
- Fonctionnalités : coordonnées GPS au survol, waypoint au double-clic

### 🔵 Future — Phases 17-20: AI Engines (6 modules)
- Weather AI
- Scoring AI
- Strategy AI
- Prediction AI
- Recommendation AI
- Analysis AI

### 🔵 Future — Phases 21-24: Finalization
- E2E Testing
- API Documentation
- Release Candidate
- GO LIVE

### 🔵 Backlog — Affiliation Platform
- Affiliate tracking
- Commission management
- Partner dashboard
- Revenue engine integration

---

## Technical Stack
- **Backend:** FastAPI + Python 3.11
- **Frontend:** React 18 + Tailwind CSS + Shadcn/UI
- **Database:** MongoDB (via Motor async)
- **LLM:** OpenAI/Claude/Gemini via `emergentintegrations`
- **Maps:** Leaflet + Stadia Maps + WMS layers
- **Payments:** Stripe

---

## Key Integrations
- MongoDB (MONGO_URL env)
- Stripe (payment processing)
- Stadia Maps (REACT_APP_STADIA_MAPS_API_KEY)
- emergentintegrations (EMERGENT_LLM_KEY)

---

## Files of Reference
- `/app/backend/modules/analytics_engine/v1/` - Analytics Engine
- `/app/backend/modules/tracking_engine/v1/` - Tracking Engine
- `/app/frontend/src/ui/administration/admin_analytics/` - Admin Analytics UI
- `/app/frontend/src/pages/AdminPremiumPage.jsx` - Admin Premium Page
- `/app/test_reports/iteration_10.json` - Latest test report
