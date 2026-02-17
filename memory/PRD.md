# HUNTIQ V5-ULTIME-FUSION - PRD

## Date de création: 16 Février 2026
## Dernière mise à jour: 17 Février 2026

---

## Problem Statement Original

Construire la version V5-ULTIME-FUSION de HUNTIQ en fusionnant les modules de:
- **HUNTIQ-V4** (branche conflict_120226_1312, commit 1072e0f) - Ossature modulaire
- **HUNTIQ-V3** (branche conflict_050226_1749, commit 200cca5) - Frontpage analytique  
- **HUNTIQ-V2** (branche conflict_030226_0855, commit 886bc5d) - Backup cloud + formations
- **HUNTIQ-BASE** (branche main, commit cc8ab6f) - Social, rental, admin avancé, partners

Architecture: 100% modulaire "LEGO", sans perte, sans dérive.

---

## Directives Exécutives - État Actuel

### ✅ P0 — URGENCE ABSOLUE (COMPLÉTÉ)
- ✅ Fusionné modules admin/notification en `admin_unified_engine` et `notification_unified_engine`
- ✅ Créé `server_orchestrator.py` pour architecture modulaire v2.0
- ✅ Réparé erreur "t is not defined" dans Analytics
- ✅ Analytics réactivé dans menu et page Admin

### ✅ P1 — MODULARISATION FRONTEND (COMPLÉTÉ)
- ✅ Structure modulaire stricte créée: `/app/frontend/src/ui`, `/data_layers`, `/components/core`
- ✅ Placeholders modules UI créés (Scoring, Météo, Stratégie, Territoire)
- ✅ Live Heading View intégré

### ✅ P2 — PLAN MAÎTRE (COMPLÉTÉ)
- ✅ `rules_engine` backend avec 12 règles dynamiques
- ✅ `strategy_master_engine` backend
- ✅ UI `PlanMaitreDashboard` complète avec Timeline, Rules, Stats
- ✅ Intégration navigation modulaire

### ✅ P3 — MONÉTISATION (COMPLÉTÉ - 17 Fév 2026)
- ✅ `payment_engine` - Intégration Stripe (checkout, abonnements, webhooks)
- ✅ `freemium_engine` - Gestion quotas, tiers (free/premium/pro), limites
- ✅ `upsell_engine` - Popups intelligents, 7 campagnes, rate limiting
- ✅ `onboarding_engine` - Parcours 4 étapes, création auto Plan Maître
- ✅ `tutorial_engine` - 7 tutoriels dynamiques, tips du jour
- ✅ Frontend `/pricing` avec 3 cartes tarifaires
- ✅ Navigation Premium bouton
- ✅ Pages success/cancel payment

### ✅ ADMINISTRATION PREMIUM (COMPLÉTÉ - 17 Fév 2026)
- ✅ `admin_engine` backend avec 10 services modulaires
- ✅ Frontend `/admin-premium` avec 11 sous-modules UI
- ✅ Dashboard KPIs (Utilisateurs, Revenus, Onboarding, CTR Upsell)
- ✅ Gestion complète: Paiements, Freemium, Upsell, Onboarding, Tutoriels
- ✅ Gestion avancée: Rules, Strategy, Users, Logs, Settings
- ✅ Thème dark premium avec accents or/bronze
- ✅ Feature toggles (10 toggles système)
- ✅ Statut clés API (masquées)

---

## Architecture Actuelle (60 modules)

```
/app/backend/
├── modules/
│   ├── admin_engine/           # ADMIN PREMIUM - 10 services
│   │   ├── router.py
│   │   └── services/
│   │       ├── payments_admin.py
│   │       ├── freemium_admin.py
│   │       ├── upsell_admin.py
│   │       ├── onboarding_admin.py
│   │       ├── tutorials_admin.py
│   │       ├── rules_admin.py
│   │       ├── strategy_admin.py
│   │       ├── users_admin.py
│   │       ├── logs_admin.py
│   │       └── settings_admin.py
│   ├── payment_engine/         # P3 - Stripe
│   ├── freemium_engine/        # P3 - Quotas
│   ├── upsell_engine/          # P3 - Popups
│   ├── onboarding_engine/      # P3 - Onboarding
│   ├── tutorial_engine/        # P3 - Tutoriels
│   ├── rules_engine/           # P2 - Plan Maître
│   ├── strategy_master_engine/ # P2
│   └── ... (52+ autres modules)
├── routers.py                  # Registre centralisé
├── server.py                   # Point d'entrée
└── server_orchestrator.py      # Orchestrateur v2.0

/app/frontend/src/
├── ui/
│   ├── administration/         # ADMIN PREMIUM - 11 modules
│   │   ├── AdminService.js
│   │   ├── admin_dashboard/
│   │   ├── admin_payments/
│   │   ├── admin_freemium/
│   │   ├── admin_upsell/
│   │   ├── admin_onboarding/
│   │   ├── admin_tutorials/
│   │   ├── admin_rules/
│   │   ├── admin_strategy/
│   │   ├── admin_users/
│   │   ├── admin_logs/
│   │   └── admin_settings/
│   ├── monetisation/           # P3
│   ├── plan_maitre/            # P2
│   └── ...
├── pages/
│   ├── AdminPremiumPage.jsx    # ADMIN PREMIUM
│   ├── PricingPage.jsx         # P3
│   └── ...
└── App.js
```

---

## Test Results (17 Fév 2026)

| Test Session | Backend | Frontend |
|--------------|---------|----------|
| P3 Monétisation (iteration_2) | 100% (18/18) | 100% |
| Admin Premium (iteration_3) | 100% (13/13) | 100% |

---

## Prioritized Backlog

### P4 — IA + OPTIMISATION (À faire)
- [ ] Historical Learning Engine
- [ ] Weather Optimization Engine
- [ ] Scoring Optimization Engine
- [ ] Strategy Optimization Engine
- [ ] Marketing Engine
- [ ] Tracking Optimization Engine

### P5 — FINALISATION (À faire)
- [ ] Tests E2E complets
- [ ] Documentation API
- [ ] Release Candidate
- [ ] Go Live

### Nice to Have
- [ ] `empirical_knowledge_layer`
- [ ] Résoudre échecs anciens (iteration_1.json)
- [ ] Migration complète modules `/modules` → `/ui`

---

## API Endpoints - Admin Premium

| Endpoint | Description |
|----------|-------------|
| `/api/v1/admin/` | Info module admin |
| `/api/v1/admin/dashboard` | KPIs globaux |
| `/api/v1/admin/payments/*` | Gestion paiements Stripe |
| `/api/v1/admin/freemium/*` | Gestion quotas/tiers |
| `/api/v1/admin/upsell/*` | Gestion campagnes |
| `/api/v1/admin/onboarding/*` | Gestion parcours |
| `/api/v1/admin/tutorials/*` | Gestion tutoriels |
| `/api/v1/admin/rules/*` | Gestion règles Plan Maître |
| `/api/v1/admin/strategy/*` | Gestion stratégies |
| `/api/v1/admin/users/*` | Gestion utilisateurs |
| `/api/v1/admin/logs/*` | Logs système |
| `/api/v1/admin/settings/*` | Paramètres & toggles |

---

## URLs

- **Preview**: https://apex-huntiq.preview.emergentagent.com
- **Pricing**: https://apex-huntiq.preview.emergentagent.com/pricing
- **Admin Premium**: https://apex-huntiq.preview.emergentagent.com/admin-premium
- **API Status**: https://apex-huntiq.preview.emergentagent.com/api/modules/status
