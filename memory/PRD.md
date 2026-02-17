# HUNTIQ-V5 — Product Requirements Document

## Document Version History
| Date | Version | Changes |
|------|---------|---------|
| 2025-12-01 | 1.0.0 | Initial BIONIC Knowledge Layer |
| 2025-12-10 | 1.1.0 | SEO Engine V5 Integration |
| 2025-12-15 | 1.2.0 | Marketing Controls Module |
| 2026-02-17 | 1.3.0 | **Phase 7 Analytics Complete** |

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
