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

## Directives Exécutives

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

---

## Architecture Actuelle (59 modules)

```
/app/backend/
├── modules/
│   ├── payment_engine/       # P3 - Stripe
│   ├── freemium_engine/      # P3 - Quotas
│   ├── upsell_engine/        # P3 - Popups
│   ├── onboarding_engine/    # P3 - Onboarding
│   ├── tutorial_engine/      # P3 - Tutoriels
│   ├── rules_engine/         # P2 - Plan Maître
│   ├── strategy_master_engine/ # P2
│   ├── admin_unified_engine/ # P0 - Unifié
│   ├── notification_unified_engine/ # P0 - Unifié
│   └── ... (50+ autres modules)
├── routers.py                # Registre centralisé
├── server.py                 # Point d'entrée
└── server_orchestrator.py    # Orchestrateur v2.0

/app/frontend/src/
├── ui/
│   ├── monetisation/         # P3 - NEW
│   │   ├── payment/
│   │   ├── freemium/
│   │   ├── upsell/
│   │   ├── onboarding/
│   │   └── tutorial/
│   ├── plan_maitre/          # P2
│   ├── scoring/
│   ├── meteo/
│   └── strategie/
├── pages/
│   ├── PricingPage.jsx       # P3 - NEW
│   ├── PaymentSuccessPage.jsx # P3 - NEW
│   └── PaymentCancelPage.jsx # P3 - NEW
└── App.js                    # Routes mises à jour
```

---

## Test Results P3 (17 Fév 2026)

| Composant | Résultat |
|-----------|----------|
| payment_engine API | ✅ 100% |
| freemium_engine API | ✅ 100% |
| upsell_engine API | ✅ 100% |
| onboarding_engine API | ✅ 100% |
| tutorial_engine API | ✅ 100% |
| Frontend /pricing | ✅ 100% |
| Premium navigation | ✅ 100% |

**Backend: 18/18 tests passed (100%)**
**Frontend: All UI components working**

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
- [ ] Résoudre échecs anciens (iteration_1.json)
- [ ] Migration complète modules `/modules` → `/ui`
- [ ] Unification templates email

---

## API Endpoints P3

| Endpoint | Description |
|----------|-------------|
| `/api/v1/payments/` | Info payment engine |
| `/api/v1/payments/packages` | Liste 4 packages |
| `/api/v1/payments/checkout/session` | Créer session Stripe |
| `/api/v1/payments/checkout/status/{id}` | Status paiement |
| `/api/v1/freemium/` | Info freemium |
| `/api/v1/freemium/subscription/{user}` | Abonnement utilisateur |
| `/api/v1/freemium/check-access` | Vérifier accès feature |
| `/api/v1/freemium/tiers/compare` | Comparaison tiers |
| `/api/v1/upsell/` | Info upsell |
| `/api/v1/upsell/trigger` | Déclencher upsell |
| `/api/v1/upsell/campaigns` | Liste campagnes |
| `/api/v1/onboarding/` | Info onboarding |
| `/api/v1/onboarding/status/{user}` | Status parcours |
| `/api/v1/tutorials/` | Info tutoriels |
| `/api/v1/tutorials/list` | Liste tutoriels |
| `/api/v1/tutorials/tip/daily` | Tip du jour |

---

## URLs

- **Preview**: https://apex-huntiq.preview.emergentagent.com
- **Pricing**: https://apex-huntiq.preview.emergentagent.com/pricing
- **API Status**: https://apex-huntiq.preview.emergentagent.com/api/modules/status
