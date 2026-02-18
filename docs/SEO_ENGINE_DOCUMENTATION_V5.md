# DOCUMENTATION COMPLÈTE - MODULE SEO ENGINE V5-ULTIME
## HUNTIQ / BIONIC - Plateforme de Chasse Intelligente

---

**Version:** 1.0.0  
**Architecture:** LEGO V5 - Module Isolé  
**Date de documentation:** Décembre 2025  
**Statut:** Module ACTIF (non verrouillé)

---

## TABLE DES MATIÈRES

1. [Vue d'Ensemble](#1-vue-densemble)
2. [Architecture et Structure des Fichiers](#2-architecture-et-structure-des-fichiers)
3. [Endpoints API Complets](#3-endpoints-api-complets)
4. [Fonctionnalités Actives](#4-fonctionnalités-actives)
5. [Logique Métier Détaillée](#5-logique-métier-détaillée)
6. [Automatisations en Place](#6-automatisations-en-place)
7. [Règles SEO Existantes](#7-règles-seo-existantes)
8. [Dépendances Internes](#8-dépendances-internes)
9. [Intégrations Actuelles](#9-intégrations-actuelles)
10. [Indicateurs de Performance (KPIs)](#10-indicateurs-de-performance-kpis)
11. [Paramètres et Configurations](#11-paramètres-et-configurations)
12. [Schémas de Données (MongoDB)](#12-schémas-de-données-mongodb)
13. [Annexes Techniques](#13-annexes-techniques)

---

## 1. VUE D'ENSEMBLE

### 1.1 Description du Module

Le **SEO Engine** est un module premium de la plateforme HUNTIQ/BIONIC dédié à l'optimisation du référencement naturel. Il implémente une stratégie SEO complète basée sur :

- **Architecture de clusters thématiques** (espèces, régions, saisons, techniques, équipement)
- **Hiérarchie de pages** (Piliers → Satellites → Opportunités)
- **Données structurées JSON-LD** pour les Rich Snippets
- **Intégration avec le Knowledge Layer** pour enrichir le contenu avec des données comportementales du gibier
- **Génération de contenu assistée par IA** (GPT-4o via Emergent LLM Key)

### 1.2 Objectif Stratégique

> **Cible : +300% de trafic organique** via une stratégie de contenu premium.

### 1.3 Prefix API

```
/api/v1/bionic/seo
```

---

## 2. ARCHITECTURE ET STRUCTURE DES FICHIERS

### 2.1 Arborescence du Module

```
/app/backend/modules/seo_engine/
├── __init__.py                 # Exports du module
├── seo_router.py               # Routes API FastAPI (41 endpoints)
├── seo_service.py              # Service orchestrateur principal
├── seo_models.py               # Modèles Pydantic (15 modèles)
├── seo_clusters.py             # Gestion des clusters SEO (9 clusters de base)
├── seo_pages.py                # Gestion des pages (6 templates)
├── seo_jsonld.py               # Schémas JSON-LD (6 types)
├── seo_analytics.py            # Analytics et KPIs
├── seo_automation.py           # Règles d'automatisation (5 règles)
├── seo_generation.py           # Génération de structure de contenu
├── seo_content_generator.py    # Génération de contenu via LLM
└── data/                       # Répertoires de stockage (vides)
    ├── clusters/
    ├── jsonld/
    └── pages/
```

### 2.2 Composants et Responsabilités

| Fichier | Classe Principale | Responsabilité |
|---------|------------------|----------------|
| `seo_router.py` | - | Définition des 41 endpoints API |
| `seo_service.py` | `SEOService` | Orchestration des composants |
| `seo_models.py` | Multiples | Définition des structures de données |
| `seo_clusters.py` | `SEOClustersManager` | CRUD et gestion des clusters |
| `seo_pages.py` | `SEOPagesManager` | CRUD pages, templates, maillage interne |
| `seo_jsonld.py` | `SEOJsonLDManager` | Génération et validation JSON-LD |
| `seo_analytics.py` | `SEOAnalyticsManager` | Métriques, KPIs, reporting |
| `seo_automation.py` | `SEOAutomationManager` | Règles automatiques, alertes, calendrier |
| `seo_generation.py` | `SEOGenerationManager` | Outlines, meta tags, scoring |
| `seo_content_generator.py` | `SEOContentGenerator` | Génération IA via Emergent LLM |

---

## 3. ENDPOINTS API COMPLETS

### 3.1 Module Info
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Information sur le SEO Engine |

### 3.2 Dashboard
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/dashboard` | Dashboard complet du SEO Engine |

### 3.3 Clusters (8 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/clusters` | Liste des clusters SEO | `cluster_type`, `is_active`, `limit` |
| GET | `/clusters/stats` | Statistiques des clusters | - |
| GET | `/clusters/hierarchy` | Hiérarchie des clusters | - |
| GET | `/clusters/{cluster_id}` | Détail d'un cluster | `cluster_id` |
| POST | `/clusters` | Créer un cluster | `cluster_data` (body) |
| PUT | `/clusters/{cluster_id}` | Mettre à jour un cluster | `cluster_id`, `updates` (body) |
| DELETE | `/clusters/{cluster_id}` | Supprimer un cluster | `cluster_id` |

### 3.4 Pages (10 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/pages` | Liste des pages SEO | `cluster_id`, `page_type`, `status`, `limit` |
| GET | `/pages/stats` | Statistiques des pages | - |
| GET | `/pages/templates` | Templates de pages disponibles | - |
| GET | `/pages/{page_id}` | Détail d'une page | `page_id` |
| POST | `/pages` | Créer une page | `page_data` (body) |
| PUT | `/pages/{page_id}` | Mettre à jour une page | `page_id`, `updates` (body) |
| POST | `/pages/{page_id}/publish` | Publier une page | `page_id` |
| DELETE | `/pages/{page_id}` | Supprimer une page | `page_id` |
| GET | `/pages/{page_id}/internal-links` | Suggestions de liens internes | `page_id` |
| GET | `/pages/{page_id}/optimize` | Recommandations d'optimisation | `page_id` |

### 3.5 JSON-LD (8 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/jsonld` | Liste des schémas JSON-LD | `page_id`, `schema_type`, `limit` |
| GET | `/jsonld/stats` | Statistiques des schémas | - |
| POST | `/jsonld/generate/article` | Générer un schéma Article | `page_data` (body) |
| POST | `/jsonld/generate/howto` | Générer un schéma HowTo | `page_data`, `steps` (body) |
| POST | `/jsonld/generate/faq` | Générer un schéma FAQPage | `questions` (body) |
| POST | `/jsonld/generate/breadcrumb` | Générer un schéma BreadcrumbList | `breadcrumbs` (body) |
| POST | `/jsonld/save` | Sauvegarder un schéma | `page_id`, `schema_type`, `schema_data` |
| POST | `/jsonld/validate` | Valider un schéma JSON-LD | `schema_data` (body) |

### 3.6 Analytics (6 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/analytics/dashboard` | Dashboard analytics SEO | - |
| GET | `/analytics/top-pages` | Pages les plus performantes | `metric`, `limit` |
| GET | `/analytics/top-clusters` | Clusters les plus performants | `limit` |
| GET | `/analytics/traffic-trend` | Tendance du trafic | `days` |
| GET | `/analytics/opportunities` | Opportunités d'optimisation | - |
| GET | `/analytics/report` | Rapport SEO | `period` |

### 3.7 Automation (8 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| GET | `/automation/rules` | Règles d'automatisation | - |
| PUT | `/automation/rules/{rule_id}/toggle` | Activer/désactiver une règle | `rule_id`, `is_active` |
| GET | `/automation/suggestions` | Suggestions de contenu | - |
| GET | `/automation/calendar` | Calendrier de contenu | - |
| GET | `/automation/tasks` | Tâches planifiées | `status` |
| POST | `/automation/tasks` | Planifier une tâche | `task_data` (body) |
| GET | `/automation/alerts` | Alertes SEO | `is_read`, `limit` |
| PUT | `/automation/alerts/{alert_id}/read` | Marquer une alerte comme lue | `alert_id` |

### 3.8 Génération de Contenu (6 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| POST | `/generate/outline` | Générer un outline de page | `cluster_id`, `page_type`, `target_keyword`, `knowledge_data` |
| POST | `/generate/meta-tags` | Générer des meta tags optimisés | `title`, `keyword`, `content_summary` |
| POST | `/generate/seo-score` | Calculer le score SEO | `page_data` (body) |
| POST | `/generate/viral-capsule` | Générer une capsule virale | `topic`, `species_id`, `knowledge_data` |
| POST | `/generate/pillar-content` | Générer le contenu d'une page pilier via IA | `species_id`, `keyword`, `knowledge_data` |
| GET | `/generate/pillar-content/history` | Historique des contenus générés | `limit` |

### 3.9 Workflow (2 endpoints)
| Méthode | Endpoint | Description | Paramètres |
|---------|----------|-------------|------------|
| POST | `/workflow/create-content` | Workflow complet de création de contenu | `cluster_id`, `page_type`, `target_keyword`, `knowledge_data` |
| POST | `/workflow/enrich-with-knowledge` | Enrichir une page avec le Knowledge Layer | `page_id`, `species_id`, `knowledge_api_response` |

### 3.10 Reports (1 endpoint)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/reports/full` | Rapport SEO complet |

---

## 4. FONCTIONNALITÉS ACTIVES

### 4.1 Gestion des Clusters SEO

#### 4.1.1 Clusters de Base (9 pré-configurés)

| ID Cluster | Nom | Type | Mot-clé Principal | Volume Recherche |
|------------|-----|------|-------------------|-----------------|
| `cluster_moose` | Chasse à l'Orignal | species | "chasse orignal québec" | 12,100 |
| `cluster_deer` | Chasse au Cerf de Virginie | species | "chasse chevreuil québec" | 9,900 |
| `cluster_bear` | Chasse à l'Ours Noir | species | "chasse ours noir québec" | 6,600 |
| `cluster_laurentides` | Chasse dans les Laurentides | region | "chasse laurentides" | 3,300 |
| `cluster_abitibi` | Chasse en Abitibi | region | "chasse abitibi" | 2,700 |
| `cluster_rut_season` | Chasse pendant le Rut | season | "chasse pendant le rut" | 8,100 |
| `cluster_calling` | Techniques d'Appel | technique | "techniques appel chasse" | 4,400 |
| `cluster_scouting` | Repérage et Pistage | technique | "conseils repérage chasse" | 2,900 |
| `cluster_equipment` | Équipement de Chasse | equipment | "liste équipement chasse" | 5,400 |

#### 4.1.2 Attributs d'un Cluster

- **Identifiant unique** (`id`)
- **Noms bilingues** (`name`, `name_fr`)
- **Type de cluster** (species, region, season, technique, equipment, territory, behavior, weather)
- **Mot-clé principal** avec métriques (volume, difficulté, CPC, intention)
- **Mots-clés secondaires** (liste)
- **Mots-clés longue traîne** (liste)
- **Pages associées** (pillar_page_id, satellite_page_ids, opportunity_page_ids)
- **Hiérarchie** (parent_cluster_id, sub_cluster_ids)
- **Liens Knowledge Layer** (species_ids, region_ids, season_tags)
- **Métriques** (total_pages, total_traffic, avg_position)

### 4.2 Gestion des Pages SEO

#### 4.2.1 Types de Pages

| Type | Description | Objectif | Word Count Cible |
|------|-------------|----------|-----------------|
| **pillar** | Page pilier (guide complet) | Autorité thématique | 2,000-3,500+ |
| **satellite** | Page satellite (sous-sujet) | Support du pilier | 800-1,200 |
| **opportunity** | Page opportunité (longue traîne) | Capture trafic niché | 400-700 |
| **viral** | Capsule virale | Partage social | Variable |
| **interactive** | Guide interactif | Engagement | Variable |
| **tool** | Outil/widget | Conversion | Variable |
| **landing** | Landing page | Acquisition | Variable |

#### 4.2.2 Templates de Pages Disponibles

**Templates Piliers (3):**
- `tpl_species_guide` - Guide Complet Chasse par Espèce (3,400 mots)
- `tpl_region_guide` - Guide Chasse par Région (2,600 mots)
- `tpl_technique_guide` - Guide Technique de Chasse (2,000 mots)

**Templates Satellites (2):**
- `tpl_species_behavior` - Article Comportement Espèce (1,000 mots)
- `tpl_seasonal_tips` - Conseils Chasse Saisonniers (1,100 mots)

**Templates Opportunités (2):**
- `tpl_specific_question` - Réponse Question Spécifique (650 mots)
- `tpl_location_specific` - Guide Lieu Spécifique (700 mots)

#### 4.2.3 Structure d'une Page

```
- Métadonnées: id, cluster_id, page_type, status, slug, url_path
- Titres: title, title_fr, h1, h2_list
- SEO: meta_description, primary_keyword, secondary_keywords, keyword_density, seo_score
- Maillage: internal_links_out, internal_links_in
- JSON-LD: jsonld_types, jsonld_data
- Ciblage: target_audience, target_regions, target_seasons, target_species
- Knowledge Layer: knowledge_rules_applied, knowledge_data_used
- Performance: impressions, clicks, ctr, avg_position, conversions
- Métadonnées: author, created_at, updated_at, published_at, scheduled_at
```

### 4.3 Schémas JSON-LD

#### 4.3.1 Types Supportés

| Type | Usage | Recommandé Pour |
|------|-------|-----------------|
| `Article` | Articles et guides | Toutes les pages de contenu |
| `HowTo` | Tutoriels étape par étape | Guides techniques |
| `FAQPage` | Questions/réponses | Pages avec FAQ |
| `LocalBusiness` | Pourvoiries, ZECs | Pages régionales |
| `BreadcrumbList` | Fil d'Ariane | Toutes les pages |
| `VideoObject` | Vidéos intégrées | Pages avec média vidéo |

#### 4.3.2 Génération Automatique

Le système génère automatiquement les schémas JSON-LD basés sur :
- Le type de page
- Les données structurées (titre, description, date, etc.)
- Les étapes pour HowTo
- Les questions/réponses pour FAQ

#### 4.3.3 Validation des Schémas

Validation automatique incluant :
- Présence de `@context` et `@type`
- Champs requis selon le type de schéma
- Avertissements et erreurs reportés

### 4.4 Génération de Contenu IA

#### 4.4.1 Intégration LLM

- **Provider:** OpenAI via Emergent LLM Key
- **Modèle:** GPT-4o
- **Bibliothèque:** `emergentintegrations.llm.chat`

#### 4.4.2 Génération de Pages Piliers

Le générateur IA crée du contenu complet incluant :
- Structure optimisée (10 sections)
- Intégration des données Knowledge Layer
- Minimum 3,500 mots
- FAQ avec 8 questions
- Optimisation mot-clé naturelle

#### 4.4.3 Structure du Prompt IA

Le prompt inclut automatiquement :
- Données comportementales de l'espèce (température, activité, habitat, alimentation)
- Information sur le rut
- Phase saisonnière actuelle
- Structure SEO requise
- Consignes de tonalité et style

### 4.5 Maillage Interne Intelligent

#### 4.5.1 Calcul Automatique des Liens

Le système suggère des liens internes basés sur :
- Appartenance au même cluster
- Espèces cibles communes
- Régions cibles communes
- Type de contenu (contextuel, navigation, lié, CTA)

#### 4.5.2 Priorités de Liens

| Priorité | Critère |
|----------|---------|
| 3 (haute) | Même cluster |
| 2 (moyenne) | Même espèce/région |
| 1 (basse) | Contenu connexe |

---

## 5. LOGIQUE MÉTIER DÉTAILLÉE

### 5.1 Workflow de Création de Contenu

```
1. SEOService.create_content_workflow()
   ├── 2. SEOGenerationManager.generate_page_outline()
   │   ├── Génération structure selon type (pillar/satellite/opportunity)
   │   ├── Suggestions de liens internes
   │   └── Recommandations JSON-LD
   ├── 3. SEOPagesManager.create_page()
   │   └── Création page en statut "draft"
   └── 4. SEOGenerationManager.calculate_seo_score()
       └── Score initial de la page
```

### 5.2 Enrichissement Knowledge Layer

```
1. SEOService.enrich_with_knowledge()
   ├── Récupération page existante
   ├── Extraction données Knowledge Layer
   │   ├── Données espèce (species)
   │   ├── Règles applicables (applied_rules)
   │   └── Phase saisonnière (seasonal_phase)
   └── Mise à jour page avec données enrichies
```

### 5.3 Optimisation de Page

```
1. SEOService.optimize_page()
   ├── Calcul score SEO actuel
   ├── Suggestions liens internes
   ├── Recommandations JSON-LD
   └── Checklist d'optimisation
       ├── Titre optimisé
       ├── Meta description
       ├── Liens internes (≥3)
       ├── Schémas JSON-LD
       └── Word count (≥800)
```

### 5.4 Score SEO - Algorithme de Calcul

```python
Score initial: 100 points

Déductions:
- Titre manquant: -15
- Titre < 30 caractères: -5
- Titre > 60 caractères: -5
- Meta description manquante: -10
- Meta description trop courte/longue: -5
- Mot-clé absent du titre: -10
- H1 manquant: -10
- H1 sans mot-clé: -5
- < 3 H2: -5
- Word count insuffisant: -15
- Word count marginal: -5
- < 2 liens internes: -10
- Pas de JSON-LD: -10

Grades:
A: ≥90 | B: ≥80 | C: ≥70 | D: ≥60 | F: <60
```

### 5.5 Health Score Global

```python
Score initial: 100 points

Pénalités:
- Position moyenne > 20: -30
- Position moyenne > 10: -15
- CTR < 3%: -20
- CTR < 5%: -10
- Score SEO moyen < 60: -25
- Score SEO moyen < 80: -10
- Taux publication < 50%: -15
- Taux publication < 80%: -5

Résultat: max(0, min(100, score))
```

---

## 6. AUTOMATISATIONS EN PLACE

### 6.1 Règles d'Automatisation par Défaut

| ID | Nom | Déclencheur | Action | Configuration |
|----|-----|-------------|--------|---------------|
| `auto_internal_linking` | Maillage interne automatique | `page_created` | `suggest_links` | max: 5, min_relevance: 0.6 |
| `seo_score_alert` | Alerte score SEO | `page_updated` | `alert` | seuil: 60, type: warning |
| `publish_reminder` | Rappel de publication | `scheduled` | `notify` | délai: 7 jours, fréquence: daily |
| `seasonal_content` | Contenu saisonnier | `scheduled` | `suggest_content` | avance: 4 semaines |
| `keyword_tracking` | Suivi positions | `scheduled` | `track` | fréquence: weekly, alerte chute: 5 |

### 6.2 Suggestions de Contenu Saisonnières

Le système génère automatiquement des suggestions basées sur le mois en cours :

| Mois | Suggestions |
|------|-------------|
| Septembre | Guide pré-rut orignal, Techniques d'appel femelle |
| Octobre | Stratégies pic du rut orignal |
| Novembre | Chasse au cerf pendant le rut |

### 6.3 Système d'Alertes

#### Types d'Alertes
- Score SEO inférieur au seuil
- Pages en brouillon depuis trop longtemps
- Chute de position significative

#### Propriétés d'une Alerte
```
- id: Identifiant unique
- type: Type d'alerte
- message: Message descriptif
- page_id: Page concernée (optionnel)
- priority: low | medium | high
- is_read: État de lecture
- created_at: Date de création
```

### 6.4 Calendrier de Contenu

Le calendrier organise automatiquement :
- Pages planifiées pour publication
- Tâches SEO programmées
- Vue par date avec regroupement pages/tâches

---

## 7. RÈGLES SEO EXISTANTES

### 7.1 Règles de Titres

| Règle | Critère | Impact Score |
|-------|---------|--------------|
| Présence | Titre requis | -15 si absent |
| Longueur min | ≥ 30 caractères | -5 si non respecté |
| Longueur max | ≤ 60 caractères | -5 si dépassé |
| Mot-clé | Présence du mot-clé principal | -10 si absent |

### 7.2 Règles de Meta Description

| Règle | Critère | Impact Score |
|-------|---------|--------------|
| Présence | Meta description requise | -10 si absente |
| Longueur min | ≥ 120 caractères | -5 si non respecté |
| Longueur max | ≤ 160 caractères | -5 si dépassé |

### 7.3 Règles de Contenu

| Règle | Type Page | Word Count Min | Impact Score |
|-------|-----------|----------------|--------------|
| Pillar | pillar | 2,000 | -15 si insuffisant |
| Satellite | satellite | 800 | -15 si insuffisant |
| Opportunity | opportunity | 400 | -15 si insuffisant |

### 7.4 Règles de Structure

| Règle | Critère | Impact Score |
|-------|---------|--------------|
| H1 | Présence obligatoire | -10 si absent |
| H1 + keyword | Mot-clé dans H1 | -5 si absent |
| H2 | Minimum 3 sous-titres | -5 si insuffisant |

### 7.5 Règles de Maillage

| Règle | Critère | Impact Score |
|-------|---------|--------------|
| Liens sortants | Minimum 2 liens internes | -10 si insuffisant |
| Recommandation | Minimum 3 liens suggérés | Recommandation |

### 7.6 Règles JSON-LD

| Règle | Critère | Impact Score |
|-------|---------|--------------|
| Présence | Au moins 1 schéma | -10 si absent |
| @context | "https://schema.org" | Erreur validation |
| @type | Type valide requis | Erreur validation |

---

## 8. DÉPENDANCES INTERNES

### 8.1 Dépendances Intra-Module

```
seo_router.py
├── seo_service.py (SEOService)
├── seo_clusters.py (SEOClustersManager)
├── seo_pages.py (SEOPagesManager)
├── seo_jsonld.py (SEOJsonLDManager)
├── seo_analytics.py (SEOAnalyticsManager)
├── seo_automation.py (SEOAutomationManager)
├── seo_generation.py (SEOGenerationManager)
└── seo_content_generator.py (SEOContentGenerator)

seo_service.py
├── seo_clusters.py
├── seo_pages.py
├── seo_jsonld.py
├── seo_analytics.py
├── seo_automation.py
└── seo_generation.py
```

### 8.2 Dépendances Externes (Projet)

| Dépendance | Usage | Fichier Source |
|------------|-------|----------------|
| Motor (AsyncIOMotorClient) | Connexion MongoDB | `seo_router.py` |
| FastAPI (APIRouter) | Définition des routes | `seo_router.py` |
| Pydantic (BaseModel) | Validation des données | `seo_models.py` |
| emergentintegrations | Génération IA | `seo_content_generator.py` |

### 8.3 Intégration Knowledge Layer

Le SEO Engine est conçu pour s'intégrer avec le **Knowledge Layer** de BIONIC :

```
SEO Engine → Knowledge Layer
├── Données comportementales (species_info)
├── Phases saisonnières (seasonal_phase)
├── Règles applicables (applied_rules)
└── Sources alimentaires, habitats, etc.
```

**Note:** L'intégration est préparée dans le code mais dépend de l'API Knowledge Layer externe.

---

## 9. INTÉGRATIONS ACTUELLES

### 9.1 Base de Données MongoDB

#### Collections Utilisées

| Collection | Description |
|------------|-------------|
| `seo_clusters` | Clusters SEO personnalisés |
| `seo_pages` | Pages SEO |
| `seo_jsonld` | Schémas JSON-LD |
| `seo_alerts` | Alertes SEO |
| `seo_scheduled_tasks` | Tâches planifiées |
| `seo_automation_rules` | Règles d'automatisation personnalisées |
| `seo_generated_content` | Historique des contenus générés par IA |

#### Configuration Connexion

```python
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'bionic_db')
```

### 9.2 Emergent LLM Key (IA)

#### Configuration

```python
API_KEY = os.environ.get("EMERGENT_LLM_KEY")
MODEL_PROVIDER = "openai"
MODEL_NAME = "gpt-4o"
```

#### Usage

- Génération de pages piliers complètes
- Intégration automatique des données Knowledge Layer
- Fallback en cas d'indisponibilité (structure template uniquement)

### 9.3 Intégrations Préparées (Non Actives)

| Intégration | Statut | Description |
|-------------|--------|-------------|
| Google Search Console | **Préparé** | Import de métriques réelles (impressions, clicks, positions) |
| Knowledge Layer API | **Préparé** | Enrichissement contenu avec données comportementales |
| MFFP Quebec | **Référencé** | Source de données réglementaires |

---

## 10. INDICATEURS DE PERFORMANCE (KPIs)

### 10.1 KPIs Cibles Configurés

| Indicateur | Valeur Cible | Unité |
|------------|--------------|-------|
| Position moyenne | < 10 | Rang Google |
| CTR | > 5% | Pourcentage |
| Score SEO | > 80 | Points (0-100) |
| Taux d'indexation | > 95% | Pourcentage |
| Taux de conversion | > 2% | Pourcentage |

### 10.2 Métriques Dashboard

#### Vue d'Ensemble (Overview)
- Total impressions
- Total clicks
- CTR moyen
- Position moyenne
- Total conversions

#### Clusters
- Total clusters (base + custom)
- Clusters actifs
- Répartition par type

#### Pages
- Total pages
- Pages publiées
- Pages en brouillon
- Répartition par type

#### Schémas JSON-LD
- Total schémas
- Schémas valides
- Répartition par type

### 10.3 Opportunités d'Optimisation Détectées

Le système identifie automatiquement :

| Type | Critère | Priorité | Gain Potentiel |
|------|---------|----------|----------------|
| `low_ctr` | CTR < 3% avec > 100 impressions | High | +50% clicks |
| `low_seo_score` | Score < 60 (pages publiées) | Medium | Meilleur classement |
| `page_2_ranking` | Position 11-20 | High | +200% trafic |

### 10.4 Reporting

#### Types de Rapports
- `full` : Rapport SEO complet

#### Contenu du Rapport
1. Executive Summary (métriques clés)
2. Performance Analysis (analyse détaillée)
3. Top Performing Pages (top 5)
4. Top Performing Clusters (top 3)
5. Action Items (opportunités prioritaires)
6. Recommendations (4 recommandations automatiques)

---

## 11. PARAMÈTRES ET CONFIGURATIONS

### 11.1 Variables d'Environnement

| Variable | Usage | Fichier |
|----------|-------|---------|
| `MONGO_URL` | URL MongoDB | `seo_router.py` |
| `DB_NAME` | Nom de la base | `seo_router.py` |
| `EMERGENT_LLM_KEY` | Clé API LLM | `seo_content_generator.py` |

### 11.2 Limites par Défaut

| Paramètre | Valeur | Endpoint |
|-----------|--------|----------|
| Limit pages | 100 (max 500) | `/pages` |
| Limit clusters | 100 (max 500) | `/clusters` |
| Limit schemas | 100 (max 500) | `/jsonld` |
| Limit alerts | 50 (max 200) | `/automation/alerts` |
| Limit top pages | 10 (max 50) | `/analytics/top-pages` |
| Limit top clusters | 10 (max 50) | `/analytics/top-clusters` |
| Traffic trend days | 30 (max 90) | `/analytics/traffic-trend` |

### 11.3 Configuration JSON-LD Organisation

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "BIONIC - Chasse Bionic",
  "alternateName": "Bionic Hunt",
  "url": "https://chassebionic.com",
  "logo": "https://chassebionic.com/logo.png",
  "sameAs": [
    "https://facebook.com/chassebionic",
    "https://instagram.com/chassebionic",
    "https://youtube.com/chassebionic"
  ]
}
```

### 11.4 Configuration Génération IA

```python
SEOContentGenerator:
  api_key: EMERGENT_LLM_KEY
  model_provider: "openai"
  model_name: "gpt-4o"
  
Règles de génération:
  - Français québécois naturel
  - Structure H2/H3 claire
  - Minimum 3500 mots (piliers)
  - 8 questions FAQ
  - Références MFFP, SEPAQ
```

---

## 12. SCHÉMAS DE DONNÉES (MONGODB)

### 12.1 Collection `seo_pages`

```javascript
{
  id: String,                    // "page_xxxxxxxx"
  cluster_id: String,            // Référence cluster
  page_type: String,             // pillar|satellite|opportunity|viral|interactive|tool|landing
  status: String,                // draft|review|published|scheduled|archived
  
  // URL et Titres
  slug: String,
  url_path: String,
  title: String,
  title_fr: String,
  meta_description: String,
  meta_description_fr: String,
  
  // Contenu
  content_format: String,        // article|guide|checklist|infographic|video|quiz|calculator|map
  h1: String,
  h2_list: [String],
  word_count: Number,
  reading_time_min: Number,
  
  // SEO
  primary_keyword: String,
  secondary_keywords: [String],
  keyword_density: Number,
  seo_score: Number,             // 0-100
  
  // Maillage
  internal_links_out: [{
    target_page_id: String,
    anchor_text: String,
    anchor_text_fr: String,
    context: String,
    link_type: String,           // contextual|navigation|related|cta
    priority: Number
  }],
  internal_links_in: [String],   // Page IDs
  
  // JSON-LD
  jsonld_types: [String],        // Article|HowTo|FAQPage|etc.
  jsonld_data: Object,
  
  // Ciblage
  target_audience: String,       // beginner|intermediate|expert|guide|landowner|all
  target_regions: [String],
  target_seasons: [String],
  target_species: [String],
  
  // Knowledge Layer
  knowledge_rules_applied: [String],
  knowledge_data_used: Object,
  
  // Performance
  impressions: Number,
  clicks: Number,
  ctr: Number,
  avg_position: Number,
  conversions: Number,
  
  // Métadonnées
  author: String,
  created_at: ISODate,
  updated_at: ISODate,
  published_at: ISODate,
  scheduled_at: ISODate
}
```

### 12.2 Collection `seo_clusters`

```javascript
{
  id: String,                    // "cluster_xxxxxxxx"
  name: String,
  name_fr: String,
  cluster_type: String,          // species|region|season|technique|equipment|territory|behavior|weather
  description: String,
  description_fr: String,
  
  // Mots-clés
  primary_keyword: {
    keyword: String,
    keyword_fr: String,
    search_volume: Number,
    difficulty: Number,          // 0-1
    cpc: Number,
    intent: String,              // informational|transactional|navigational
    priority: Number,            // 1-5
    is_primary: Boolean
  },
  secondary_keywords: [Object],
  long_tail_keywords: [String],
  
  // Pages
  pillar_page_id: String,
  satellite_page_ids: [String],
  opportunity_page_ids: [String],
  
  // Hiérarchie
  parent_cluster_id: String,
  sub_cluster_ids: [String],
  
  // Métriques
  total_pages: Number,
  total_traffic: Number,
  avg_position: Number,
  
  // Knowledge Layer
  species_ids: [String],
  region_ids: [String],
  season_tags: [String],
  
  // Métadonnées
  created_at: ISODate,
  updated_at: ISODate,
  is_active: Boolean
}
```

### 12.3 Collection `seo_jsonld`

```javascript
{
  id: String,                    // "jsonld_xxxxxxxx"
  page_id: String,
  schema_type: String,           // Article|HowTo|FAQPage|LocalBusiness|BreadcrumbList|VideoObject
  schema_data: Object,           // Schéma JSON-LD complet
  is_valid: Boolean,
  validation_errors: [String],
  created_at: ISODate
}
```

### 12.4 Collection `seo_alerts`

```javascript
{
  id: String,                    // "alert_xxxxxxxx"
  type: String,                  // Type d'alerte
  message: String,
  page_id: String,               // Optionnel
  priority: String,              // low|medium|high
  is_read: Boolean,
  created_at: ISODate
}
```

### 12.5 Collection `seo_scheduled_tasks`

```javascript
{
  id: String,                    // "task_xxxxxxxx"
  type: String,                  // content_creation|optimization|etc.
  title: String,
  description: String,
  scheduled_at: ISODate,
  target_page_id: String,
  target_cluster_id: String,
  priority: String,              // low|medium|high
  status: String,                // pending|completed|cancelled
  created_at: ISODate
}
```

### 12.6 Collection `seo_generated_content`

```javascript
{
  type: String,                  // "pillar_generated"
  species_id: String,
  keyword: String,
  content: {
    title_fr: String,
    content_html: String,
    content_markdown: String,
    word_count: Number,
    h2_list: [String],
    faq_items: [{
      question: String,
      answer: String
    }],
    meta_description_fr: String,
    primary_keyword: String,
    reading_time_min: Number
  },
  metadata: {
    species_id: String,
    keyword: String,
    model_used: String,
    generated_at: ISODate,
    word_count: Number
  },
  status: String,                // draft|published
  created_at: ISODate
}
```

---

## 13. ANNEXES TECHNIQUES

### 13.1 Codes d'État des Pages

| Code | Signification |
|------|---------------|
| `draft` | Brouillon - En cours de rédaction |
| `review` | En révision - Prêt pour validation |
| `published` | Publié - En ligne |
| `scheduled` | Planifié - Publication programmée |
| `archived` | Archivé - Retiré de la publication |

### 13.2 Types de Clusters

| Type | Description | Exemple |
|------|-------------|---------|
| `species` | Par espèce de gibier | Orignal, Cerf, Ours |
| `region` | Par région géographique | Laurentides, Abitibi |
| `season` | Par saison de chasse | Rut, Pré-rut |
| `technique` | Par technique de chasse | Appel, Repérage |
| `equipment` | Par équipement | Armes, Optiques |
| `territory` | Par type de territoire | ZEC, Pourvoirie |
| `behavior` | Par comportement animal | Migration, Alimentation |
| `weather` | Par conditions météo | Neige, Pluie |

### 13.3 Grades SEO

| Grade | Score Min | Interprétation |
|-------|-----------|----------------|
| A | 90 | Excellent - Optimisation complète |
| B | 80 | Bon - Quelques améliorations possibles |
| C | 70 | Moyen - Optimisation nécessaire |
| D | 60 | Faible - Travail significatif requis |
| F | <60 | Critique - Refonte nécessaire |

### 13.4 Formats de Contenu

| Format | Usage |
|--------|-------|
| `article` | Articles standards |
| `guide` | Guides complets |
| `checklist` | Listes de vérification |
| `infographic` | Infographies |
| `video` | Contenu vidéo |
| `podcast` | Contenu audio |
| `quiz` | Quiz interactifs |
| `calculator` | Calculateurs |
| `map` | Cartes interactives |
| `comparison` | Tableaux comparatifs |

### 13.5 Intentions de Recherche

| Intention | Description | Exemple |
|-----------|-------------|---------|
| `informational` | Recherche d'information | "comment chasser l'orignal" |
| `transactional` | Intention d'achat | "acheter carabine chasse" |
| `navigational` | Navigation vers un site | "zec laurentides" |

---

## CONCLUSION

Le **SEO Engine V5-ULTIME** est un module complet et mature offrant :

✅ **41 endpoints API** couvrant tous les aspects du SEO  
✅ **9 clusters de base** pré-configurés pour le marché de la chasse au Québec  
✅ **7 templates de pages** pour différents types de contenu  
✅ **6 types de schémas JSON-LD** pour les données structurées  
✅ **5 règles d'automatisation** par défaut  
✅ **Génération de contenu IA** via GPT-4o  
✅ **Intégration préparée** avec le Knowledge Layer  
✅ **Analytics et reporting** complets  

**Statut actuel:** Module ACTIF, prêt pour utilisation et extension.

---

*Document généré le : Décembre 2025*  
*Version du module : 1.0.0*  
*Architecture : LEGO V5 - Isolé*
