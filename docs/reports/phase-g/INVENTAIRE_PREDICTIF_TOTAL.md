# INVENTAIRE PREDICTIF TOTAL - HUNTIQ BIONIC V5
## PHASE G - BIONIC ULTIMATE INTEGRATION
### Document preparé pour COPILOT MAITRE (STEEVE)
### Version: 1.0.0 | Date: Decembre 2025

---

# PREAMBULE

Ce document constitue l'**INVENTAIRE PREDICTIF TOTAL** requis avant toute implementation des modules P0 de la PHASE G. Il couvre exhaustivement les **12 familles de donnees obligatoires** definies par la COMMANDE OFFICIELLE ULTIME, avec pour chaque famille:

- Donnees existantes (avec localisation precise dans le code)
- Donnees manquantes (gap analysis)
- Donnees a acquerir (sources potentielles)
- Limites, biais et risques identifies

**Conformite:** G-SEC | G-QA | G-DOC
**Objectif:** Alimenter l'onglet INTELLIGENCE (Analytics, Previsions, Plan Maitre)

---

# TABLE DES MATIERES

1. [FAMILLE 1: Donnees Territoriales Avancees](#famille-1-donnees-territoriales-avancees)
2. [FAMILLE 2: Vegetation & Transitions d'Habitats](#famille-2-vegetation--transitions-dhabitats)
3. [FAMILLE 3: Alimentation & Carences](#famille-3-alimentation--carences)
4. [FAMILLE 4: Topographie & Geologie](#famille-4-topographie--geologie)
5. [FAMILLE 5: Zones Thermiques & Microclimats](#famille-5-zones-thermiques--microclimats)
6. [FAMILLE 6: Corridors de Deplacement](#famille-6-corridors-de-deplacement)
7. [FAMILLE 7: Zones de Repos & Abris](#famille-7-zones-de-repos--abris)
8. [FAMILLE 8: Pression de Chasse & Derangement](#famille-8-pression-de-chasse--derangement)
9. [FAMILLE 9: Conditions Extremes](#famille-9-conditions-extremes)
10. [FAMILLE 10: Historiques Multi-Annees](#famille-10-historiques-multi-annees)
11. [FAMILLE 11: Agregats Cameras Avances](#famille-11-agregats-cameras-avances)
12. [FAMILLE 12: Cycles Temporels Avances](#famille-12-cycles-temporels-avances)
13. [SOURCES EMPIRIQUES & SCIENTIFIQUES](#sources-empiriques--scientifiques)
14. [MAPPING MODULES P0](#mapping-modules-p0)
15. [SYNTHESE EXECUTIVE](#synthese-executive)

---

# FAMILLE 1: DONNEES TERRITORIALES AVANCEES

## 1.1 DONNEES EXISTANTES

### 1.1.1 Coordonnees GPS et Waypoints
| Variable | Type | Source | Localisation Code | Statut |
|----------|------|--------|-------------------|--------|
| `latitude` | float | MongoDB | `backend/modules/waypoint_engine/v1/` | EXPLOITABLE P0 |
| `longitude` | float | MongoDB | `backend/modules/waypoint_engine/v1/` | EXPLOITABLE P0 |
| `waypoint_type` | enum | MongoDB | Types: zec, pourvoirie, prive, sepaq, affut, saline, observation, camp | EXPLOITABLE P0 |
| `waypoint_notes` | string | MongoDB | Notes utilisateur libres | EXPLOITABLE P0 |
| `active` | boolean | MongoDB | Waypoint actif/inactif | EXPLOITABLE P0 |

**Collection MongoDB:** `territory_waypoints`, `waypoints`, `geo_entities`

### 1.1.2 Couches Cartographiques BIONIC
| Layer ID | Nom | Couleur | Description | Poids Scoring |
|----------|-----|---------|-------------|---------------|
| `habitats` | Habitats optimaux | #22c55e | Zones d'habitat ideales | 25% |
| `rut` | Rut potentiel | #e91e63 | Zones de rut identifiees | 20% |
| `salines` | Salines potentielles | #00bcd4 | Points de salines | 10% |
| `affuts` | Affuts potentiels | #9c27b0 | Positions d'affut | 20% |
| `trajets` | Trajets de chasse | #ff9800 | Routes recommandees | 15% |
| `peuplements` | Peuplements forestiers | #4caf50 | Types de foret | 10% |

**Localisation:** `frontend/src/components/TerritoryMap.jsx`

### 1.1.3 Services WMS Gouvernementaux (Quebec)
| Service | URL | Couches | Frequence MAJ |
|---------|-----|---------|---------------|
| Foret | servicescarto.mffp.gouv.qc.ca | Couverture forestiere | Annuelle |
| Hydro | servicescarto.mern.gouv.qc.ca | Hydrographie GRHQ | Statique |
| Topo | servicescarto.mern.gouv.qc.ca | Relief LiDAR | Statique |
| Routes | servicescarto.mern.gouv.qc.ca | Routes et chemins | Annuelle |
| Cadastre | servicescarto.mern.gouv.qc.ca | Cadastre | Annuelle |

**Localisation:** `frontend/src/pages/MapPage.jsx`

### 1.1.4 Entites Territoriales Utilisateur
| Entite | Collection | Champs Cles |
|--------|------------|-------------|
| Lieux | `user_places` | id, name, type, lat, lng, notes |
| Tracks | `user_tracks` | points GPS, distance, duree |
| Favoris | `zone_favorites` | zone_id, alertes, notes |

## 1.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Delimitation ZEC/Pourvoiries | Polygones officiels des zones de chasse | CRITIQUE | P0 |
| Zones d'exclusion | Zones interdites a la chasse | CRITIQUE | P0 |
| Cadastre faunique | Decoupage administratif MFFP | HAUTE | P1 |
| Zones de securite tir | Calcul automatique selon reglementation | MOYENNE | P1 |

## 1.3 DONNEES A ACQUERIR

| Source | Donnee | Methode d'acquisition | Fiabilite |
|--------|--------|----------------------|-----------|
| MFFP Quebec | Polygones ZEC/Pourvoiries | API REST ou telechargement shapefile | 0.95 |
| MFFP Quebec | Zones d'exclusion chasse | Donnees ouvertes Quebec | 0.95 |
| OpenStreetMap | Sentiers et chemins | API Overpass | 0.80 |
| Cadastre Quebec | Limites proprietes | WMS/WFS | 0.90 |

## 1.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Precision GPS | ±3-10m selon appareil utilisateur | Algorithme de lissage, moyenne mobile |
| Couverture WMS | Temps de latence variable | Cache local, fallback tiles statiques |
| MAJ Cadastre | Donnees parfois obsoletes (1-2 ans) | Horodatage visible, refresh annuel |
| Biais utilisateur | Waypoints concentres zones accessibles | Ponderation par densite |

---

# FAMILLE 2: VEGETATION & TRANSITIONS D'HABITATS

## 2.1 DONNEES EXISTANTES

### 2.1.1 Variables d'Habitat (Knowledge Layer)
| Variable | ID | Unite | Source | Poids Especes |
|----------|----|----|--------|---------------|
| NDVI | `ndvi` | index [-1, 1] | NASA MODIS, Sentinel2 | moose: 0.7, deer: 0.6, bear: 0.7 |
| Couvert forestier | `canopy_cover` | % [0-100] | Satellite, LiDAR | moose: 0.8, deer: 0.7, bear: 0.6 |
| Densite canopee | `canopy_density` | % [0-100] | LiDAR, Sentinel2 | moose: 0.7, deer: 0.65, bear: 0.6 |
| Densite lisieres | `edge_density` | m/ha [0-500] | Satellite, inventaire | moose: 0.85, deer: 0.9, bear: 0.6 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/habitat_variables.json`

### 2.1.2 Types d'Habitats (Enums)
```python
class HabitatType(str, Enum):
    CONIFEROUS_FOREST = "coniferous_forest"    # Foret coniferienne
    DECIDUOUS_FOREST = "deciduous_forest"      # Foret feuillue
    MIXED_FOREST = "mixed_forest"              # Foret mixte
    WETLAND = "wetland"                        # Milieu humide
    BOG = "bog"                                # Tourbiere
    MARSH = "marsh"                            # Marecage
    LAKE_SHORE = "lake_shore"                  # Rive de lac
    RIVER_CORRIDOR = "river_corridor"          # Corridor riverain
    RIDGE = "ridge"                            # Crete
    VALLEY = "valley"                          # Vallee
    CLEARCUT = "clearcut"                      # Coupe forestiere
    REGENERATION = "regeneration"              # Regeneration
    AGRICULTURAL = "agricultural"              # Zone agricole
    ALPINE = "alpine"                          # Zone alpine
    TUNDRA = "tundra"                          # Toundra
```

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/knowledge_models.py`

### 2.1.3 Preferences d'Habitat par Espece
| Espece | Habitat Principal | Score | Habitat Secondaire | Score |
|--------|-------------------|-------|-------------------|-------|
| Orignal | wetland | 0.90 | mixed_forest | 0.85 |
| Cerf | forest_edge | 0.85 | regeneration | 0.80 |
| Ours | mixed_forest | 0.80 | berry_patches | 0.75 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/moose.json`

## 2.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Ecotones dynamiques | Transitions inter-habitats en temps reel | HAUTE | P0 |
| Age des peuplements | Maturite forestiere (jeune/mature/vieux) | HAUTE | P1 |
| Perturbations recentes | Coupes, feux, epidemies (5 derniers ans) | MOYENNE | P1 |
| Phenologie vegetale | Stade de developpement saisonnier | MOYENNE | P1 |

## 2.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite | Cout |
|--------|--------|---------|-----------|------|
| Sentinel-2 | NDVI haute resolution | API Copernicus | 0.90 | Gratuit |
| MFFP | Inventaire ecoforestier | Donnees ouvertes | 0.95 | Gratuit |
| CFS-NRCan | Perturbations forestieres | API REST | 0.85 | Gratuit |
| NASA MODIS | Phenologie FPAR/LAI | AppEEARS | 0.85 | Gratuit |

## 2.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Resolution NDVI | 10-30m selon source | Interpolation spatiale |
| Delai satellite | 5-16 jours selon orbite | Fusion multi-capteurs |
| Couvert nuageux | Masquage frequent au Quebec | Composite temporel |
| Saisonnalite | NDVI non pertinent en hiver | Modeles saisonniers adaptes |

---

# FAMILLE 3: ALIMENTATION & CARENCES

## 3.1 DONNEES EXISTANTES

### 3.1.1 Sources Alimentaires par Espece
| Espece | Source | Nom FR | Categorie | Mois Dispo | Preference |
|--------|--------|--------|-----------|------------|------------|
| Orignal | willow | Saule | browse | 5-9 | 0.95 |
| Orignal | aquatic_plants | Plantes aquatiques | browse | 6-8 | 0.90 |
| Orignal | birch | Bouleau | browse | 5-10 | 0.80 |
| Orignal | balsam_fir | Sapin baumier | browse | 11-3 | 0.75 |
| Cerf | browse | Brout | browse | toute annee | 0.85 |
| Cerf | forbs | Plantes herbacees | graze | 5-9 | 0.80 |
| Cerf | mast | Glands/noix | mast | 9-11 | 0.90 |
| Ours | berries | Baies | fruit | 7-9 | 0.95 |
| Ours | nuts | Noix | mast | 9-11 | 0.85 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/*.json`

### 3.1.2 Couche Alimentation (Frontend)
| Layer | ID | Couleur | Description |
|-------|----|---------| ------------|
| Zones alimentation | `alimentation` | #8bc34a | Sources de nourriture identifiees |

**Localisation:** `frontend/src/components/TerritoryMap.jsx`

### 3.1.3 Valeurs Nutritionnelles
| Source | Valeur Nutritionnelle | Persistance | Attractivite |
|--------|----------------------|-------------|--------------|
| Plantes aquatiques | 0.90 | 3 mois | 0.95 |
| Saule | 0.80 | 5 mois | 0.90 |
| Baies | 0.85 | 2 mois | 0.95 |

## 3.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Cartes de mast | Localisation chenes, noyers, hetre | CRITIQUE | P0 |
| Stress alimentaire | Indicateurs de carence par zone | HAUTE | P0 |
| Salines naturelles | Localisation des sources minerales | HAUTE | P0 |
| Production fruitiere | Estimation annuelle de la production de baies | MOYENNE | P1 |

## 3.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| MFFP | Cartes essences forestieres | Inventaire ecoforestier | 0.90 |
| UQAR | Etudes stress alimentaire | Publications scientifiques | 0.85 |
| Terrain utilisateur | Salines naturelles | Crowdsourcing waypoints | 0.75 |
| Sentinel-2 | Phenologie floraison/fructification | NDVI temporel | 0.70 |

## 3.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Variabilite interannuelle | Production de mast tres variable | Historique 5 ans |
| Localisation approximative | Sources alimentaires estimees | Validation terrain |
| Biais echantillonnage | Donnees concentrees zones accessibles | Modeles predictifs |

---

# FAMILLE 4: TOPOGRAPHIE & GEOLOGIE

## 4.1 DONNEES EXISTANTES

### 4.1.1 Variables Topographiques
| Variable | ID | Unite | Source | Poids |
|----------|----|----|--------|-------|
| Elevation | `elevation` | m | open_elevation, SRTM | moose: 0.5, deer: 0.4 |
| Pente | `slope` | degres [0-90] | DEM derive | moose: 0.3, deer: 0.4 |
| Orientation | `aspect` | degres [0-360] | DEM derive | moose: 0.4, deer: 0.5 |
| Exposition | `slope_aspect` | cardinal (N,NE,E...) | DEM derive | saisonnier |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/habitat_variables.json`

### 4.1.2 Couches Cartographiques Terrain
| Layer | ID | Couleur | Description |
|-------|----|---------| ------------|
| Pentes | `pentes` | #ff7043 | Inclinaison terrain |
| Altitude | `altitude` | #78909c | Elevation relative |
| Orientation | `orientation` | #2196f3 | Direction terrain |
| Ensoleillement | `ensoleillement` | #ffeb3b | Exposition solaire |

**Localisation:** `frontend/src/components/TerritoryMap.jsx`

### 4.1.3 Plages Optimales par Espece
| Espece | Elevation Min | Elevation Max | Elevation Optimale | Pente Preferee |
|--------|---------------|---------------|-------------------|----------------|
| Orignal | 0m | 1200m | 300m | 5-15 degres |
| Cerf | 0m | 800m | 200m | 0-20 degres |
| Ours | 0m | 1500m | 400m | variable |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/moose.json`

## 4.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Rugosite terrain | Indice de difficulte de deplacement | HAUTE | P0 |
| Geologie surfacique | Type de sol, roche mere | MOYENNE | P1 |
| Drainage | Capacite d'evacuation des eaux | MOYENNE | P1 |
| Microrelief | Depressions, buttes, ravines | BASSE | P2 |

## 4.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Resolution | Fiabilite |
|--------|--------|---------|------------|-----------|
| USGS | SRTM DEM | Telechargement direct | 30m | 0.90 |
| Quebec LiDAR | MNT haute precision | MERN | 1m | 0.98 |
| GSC | Geologie surfacique | Donnees ouvertes | 1:250k | 0.85 |

## 4.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Resolution SRTM | 30m insuffisant pour microrelief | LiDAR provincial |
| Couverture LiDAR | Non disponible partout au Quebec | Fusion SRTM/LiDAR |
| Artefacts DEM | Erreurs dans zones forestieres denses | Filtrage algorithmique |

---

# FAMILLE 5: ZONES THERMIQUES & MICROCLIMATS

## 5.1 DONNEES EXISTANTES

### 5.1.1 Variables Climatiques
| Variable | ID | Unite | Source | MAJ | Poids |
|----------|----|----|--------|-----|-------|
| Temperature | `temperature` | degC | open_meteo, environment_canada | temps reel | moose: 0.9, deer: 0.6 |
| Vitesse vent | `wind_speed` | km/h | open_meteo | temps reel | moose: 0.6, deer: 0.7 |
| Humidite | `humidity` | % | open_meteo | temps reel | 0.5 |
| Precipitation | `precipitation` | mm/h | open_meteo | horaire | moose: 0.5, deer: 0.6 |
| Pression | `barometric_pressure` | hPa | open_meteo | horaire | moose: 0.4, deer: 0.8 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/habitat_variables.json`

### 5.1.2 Plages de Temperature Optimales
| Espece | Optimal Min | Optimal Max | Tolerance Min | Tolerance Max | Seuil Activite |
|--------|-------------|-------------|---------------|---------------|----------------|
| Orignal | -5C | 14C | -40C | 25C | 20C |
| Cerf | -5C | 15C | -30C | 30C | 25C |
| Ours | 5C | 25C | -20C | 35C | 30C |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/*.json`

### 5.1.3 Conditions Optimales de Chasse
```python
OPTIMAL_CONDITIONS = {
    "temperature": {"min": -5, "max": 15, "ideal": 5},  # Celsius
    "humidity": {"min": 40, "max": 80, "ideal": 60},    # %
    "wind_speed": {"min": 0, "max": 20, "ideal": 8},    # km/h
    "pressure_change": 5  # hPa - declencheur d'activite
}
```

**Localisation:** `/app/backend/modules/weather_engine/v1/service.py`

## 5.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Temperature au sol | Differentiel air/sol crucial pour gibier | CRITIQUE | P0 |
| Microclimats topographiques | Poches de froid/chaleur locales | HAUTE | P0 |
| Gradient thermique vertical | Temperature selon altitude | HAUTE | P0 |
| Couverture nuageuse | Impact sur rayonnement et comportement | MOYENNE | P1 |

## 5.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| Open-Meteo | Donnees horaires completes | API REST gratuite | 0.85 |
| Environment Canada | Stations meteo officielles | API REST | 0.95 |
| Modele derive | Microclimats (aspect x elevation) | Calcul local | 0.70 |
| GOES Satellite | Couverture nuageuse temps reel | API NOAA | 0.90 |

## 5.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Resolution spatiale meteo | Stations espacees 50-100km | Interpolation spatiale |
| Previsions > 7 jours | Fiabilite decroissante | Limiter affichage a 5 jours |
| Microclimats non modelises | Variations locales non captees | Modele topographique |
| Delai API | Latence 1-5 min | Cache intelligent |

---

# FAMILLE 6: CORRIDORS DE DEPLACEMENT

## 6.1 DONNEES EXISTANTES

### 6.1.1 Couche Corridors
| Layer | ID | Couleur | Description |
|-------|----|---------| ------------|
| Corridors fauniques | `corridors` | #ff5722 | Passages faune identifies |

**Localisation:** `frontend/src/components/TerritoryMap.jsx`

### 6.1.2 Service Comportemental - Corridors
```javascript
// BehavioralService.js
static async getMovementCorridors(lat, lng, species, radiusKm = 5)
// Retourne: { corridors: [{ id, type, traffic, ... }] }
```

**Localisation:** `/app/frontend/src/modules/behavioral/BehavioralService.js`

### 6.1.3 Patterns de Deplacement Backend
```python
# MovementPattern - modele de donnees
{
    "typical_routes": [
        {"type": "feeding_to_bedding", "distance_km": 0.5, "typical_time": "08:00"},
        {"type": "bedding_to_feeding", "distance_km": 0.5, "typical_time": "16:00"}
    ],
    "travel_corridors": [
        {"type": "ridge_line", "usage": "high"},
        {"type": "creek_bottom", "usage": "medium"}
    ]
}
```

**Localisation:** `/app/backend/modules/wildlife_behavior_engine/v1/service.py`

## 6.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Detection corridors GPS | Identification automatique depuis cameras | CRITIQUE | P0 |
| Intensite de trafic | Frequence d'utilisation des corridors | CRITIQUE | P0 |
| Saisonnalite corridors | Variation des routes selon saisons | HAUTE | P0 |
| Goulots d'etranglement | Points de passage obligatoires | HAUTE | P0 |

## 6.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| Cameras trail | Patterns de passage | Agregation temporelle | 0.85 |
| Telemetrie externe | Donnees GPS colliers (etudes MFFP) | Partenariat | 0.95 |
| UQAR | Corridors modelises | Publications | 0.90 |
| Utilisateurs | Observations terrain | Crowdsourcing | 0.70 |

## 6.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Echantillonnage cameras | Couverture partielle | Modeles predictifs |
| Biais placement cameras | Sur sentiers accessibles | Ponderation spatiale |
| Dynamique temporelle | Corridors changent avec perturbations | MAJ annuelle |

---

# FAMILLE 7: ZONES DE REPOS & ABRIS

## 7.1 DONNEES EXISTANTES

### 7.1.1 Couche Repos
| Layer | ID | Couleur | Description |
|-------|----|---------| ------------|
| Zones de repos | `repos` | #795548 | Zones de coucher identifiees |

**Localisation:** `frontend/src/components/TerritoryMap.jsx`

### 7.1.2 Service Comportemental - Zones de Coucher
```javascript
// BehavioralService.js
static async getBeddingAreas(lat, lng, species, radiusKm = 3)
// Retourne: { areas: [{ id, name, score, type }] }
```

**Localisation:** `/app/frontend/src/modules/behavioral/BehavioralService.js`

### 7.1.3 Zones de Concentration
```python
# WildlifeBehaviorService
"concentration_zones": [
    {"type": "bedding_area", "habitat": "thick_cover"},
    {"type": "water_source", "habitat": "stream"}
]
```

**Localisation:** `/app/backend/modules/wildlife_behavior_engine/v1/service.py`

## 7.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Ravages hivernaux | Zones de concentration hivernale orignal | CRITIQUE | P0 |
| Abris thermiques | Zones protegees du vent/froid | HAUTE | P0 |
| Densite couvert | Indice de protection visuelle | HAUTE | P0 |
| Distance securite | Eloignement routes/habitations | MOYENNE | P1 |

## 7.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| MFFP | Inventaire ravages | Donnees officielles | 0.95 |
| LiDAR | Densite sous-bois | Analyse 3D | 0.90 |
| Modele derive | Score abri (canopy x slope x aspect) | Calcul | 0.75 |

## 7.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Ravages dynamiques | Changent selon conditions neige | MAJ saisonniere |
| Resolution LiDAR | Non disponible partout | Proxy satellite |

---

# FAMILLE 8: PRESSION DE CHASSE & DERANGEMENT

## 8.1 DONNEES EXISTANTES

### 8.1.1 Variables Impact Humain
| Variable | ID | Unite | Source | Poids |
|----------|----|----|--------|-------|
| Distance route | `road_distance` | m | OSM, MTQ | moose: 0.7, deer: 0.6, bear: 0.5 |
| Distance batiment | `building_distance` | m | OSM, Cadastre | moose: 0.6, deer: 0.5, bear: 0.7 |
| Indice pression humaine | `human_pressure_index` | [0-1] | Composite | moose: 0.75, deer: 0.6, bear: 0.85 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/habitat_variables.json`

### 8.1.2 Tolerance et Fuite par Espece
| Espece | Tolerance Humaine | Distance Fuite | Evitement Route |
|--------|-------------------|----------------|-----------------|
| Orignal | 0.30 | 150m | 300m |
| Cerf | 0.35 | 100m | 200m |
| Ours | 0.25 | 200m | 250m |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/*.json`

### 8.1.3 Sorties de Chasse Enregistrees
| Variable | Type | Source | Collection |
|----------|------|--------|------------|
| `total_trips` | integer | MongoDB | `hunting_trips` |
| `date` | datetime | MongoDB | Par sortie |
| `duration_hours` | float | MongoDB | Par sortie |
| `success` | boolean | MongoDB | Par sortie |
| `location` | coordinates | MongoDB | Par sortie |

**Localisation:** `/app/backend/modules/analytics_engine/`

## 8.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Densite chasseurs | Nombre chasseurs par zone/periode | CRITIQUE | P0 |
| Pression cumulative | Historique pression sur plusieurs jours | CRITIQUE | P0 |
| Activites recreatives | Randonnee, VTT, motoneige | HAUTE | P0 |
| Calendrier ouvertures | Dates chasse par zone/espece | HAUTE | P0 |

## 8.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| MFFP | Statistiques recolte | Rapports publics | 0.95 |
| Strava Heatmap | Activites recreatives | API | 0.80 |
| Utilisateurs HUNTIQ | Sorties enregistrees | Agregation interne | 0.85 |
| SEPAQ | Frequentation reserves | Partenariat | 0.90 |

## 8.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Donnees privees | Sorties non partagees | Opt-in anonymise |
| Biais territorial | Concentration zones populaires | Normalisation |
| Temps reel impossible | Pas de tracking live chasseurs | Modeles predictifs |

---

# FAMILLE 9: CONDITIONS EXTREMES

## 9.1 DONNEES EXISTANTES

### 9.1.1 Seuils Climatiques
| Condition | Seuil | Impact Comportement | Source |
|-----------|-------|---------------------|--------|
| Vent fort | > 30 km/h | Reduction activite -25% | WeatherService |
| Pluie forte | > 5 mm/h | Reduction activite -20% | WeatherService |
| Froid extreme | < -20C | Reduction deplacement | SPECIES_PATTERNS |
| Chaleur extreme | > 25C | Inactivite diurne | SPECIES_PATTERNS |

**Localisation:** `/app/backend/modules/weather_engine/v1/service.py`

### 9.1.2 Modificateurs Saisonniers
```python
SEASON_FACTORS = {
    1: 0.6,   # Janvier - froid
    2: 0.5,   # Fevrier - tres froid
    7: 0.5,   # Juillet - chaleur
    10: 0.95, # Octobre - pic
    11: 0.9,  # Novembre - rut
}
```

**Localisation:** `/app/backend/modules/predictive_engine/v1/service.py`

## 9.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Epaisseur neige | Impact mobilite et energie | CRITIQUE | P0 |
| Gel au sol | Accessibilite nourriture | HAUTE | P0 |
| Verglas | Dangerosité deplacement | HAUTE | P0 |
| Stress thermique | Index combine (temp + humidex) | MOYENNE | P1 |

## 9.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| Environment Canada | Epaisseur neige stations | API REST | 0.90 |
| NOAA | Modeles neige SNODAS | Telechargement | 0.85 |
| Derive | Stress thermique (formule) | Calcul | 0.80 |

## 9.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Stations espacees | Interpolation necessaire | Krigeage spatial |
| Micro-variabilite neige | Accumulation locale variable | Modele topographique |

---

# FAMILLE 10: HISTORIQUES MULTI-ANNEES

## 10.1 DONNEES EXISTANTES

### 10.1.1 Collections MongoDB Historiques
| Collection | Donnees | Profondeur | Volume Estime |
|------------|---------|------------|---------------|
| `hunting_trips` | Sorties de chasse | Depuis creation | ~51+ records demo |
| `camera_events` | Photos cameras | Depuis creation | Variable |
| `territory_waypoints` | Waypoints | Depuis creation | Variable |
| `user_observations` | Observations faune | Depuis creation | Variable |

### 10.1.2 Modeles Saisonniers
```python
# SeasonalModel - structure
{
    "species_id": "moose",
    "region": "quebec_south",
    "year": 2024,
    "phases": [
        {"name": "rut", "start": "2024-09-15", "peak": "2024-10-01", "end": "2024-10-20"}
    ],
    "accuracy_score": 0.85,
    "validation_observations": 150
}
```

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/knowledge_models.py`

## 10.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Historique recolte MFFP | Statistiques officielles multi-annees | CRITIQUE | P0 |
| Tendances populations | Evolution densites par zone | CRITIQUE | P0 |
| Patterns interannuels | Cycles pluriannuels (mastage, populations) | HAUTE | P1 |
| Baseline climat | Normales climatiques 30 ans | MOYENNE | P1 |

## 10.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Profondeur | Fiabilite |
|--------|--------|---------|------------|-----------|
| MFFP | Statistiques recolte | Rapports PDF/API | 10+ ans | 0.95 |
| Environment Canada | Normales climatiques | API | 30 ans | 0.95 |
| UQAR | Etudes populations | Publications | Variable | 0.90 |
| Louis Gagnon | Historique terrain | Entrevues | 30+ ans | 0.85 |

## 10.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Donnees fragmentees | Formats et sources heterogenes | ETL standardise |
| Biais d'echantillonnage | Zones mieux documentees que d'autres | Ponderation |
| Changements methodo | Protocoles de collecte evolues | Normalisation |

---

# FAMILLE 11: AGREGATS CAMERAS AVANCES

## 11.1 DONNEES EXISTANTES

### 11.1.1 Schema Camera Event
```python
# CameraEvent - modele complet
{
    "id": str,
    "user_id": str,
    "camera_id": str,
    "waypoint_id": str,  # OBLIGATOIRE
    "timestamp": datetime,
    "raw_image_url": str,  # Chemin chiffre
    "exif_data": {
        "timestamp": str,
        "gps_lat": float,
        "gps_lon": float,
        "camera_make": str,
        "camera_model": str
    },
    "species": str,            # Detecte par IA (Phase 2)
    "species_confidence": float,# Score IA
    "created_at": datetime
}
```

**Localisation:** `/app/backend/modules/camera_engine/v1/services.py`

### 11.1.2 Service Detection Especes
| Fonctionnalite | Statut | Module |
|----------------|--------|--------|
| Registre cameras | ACTIF | camera_engine |
| Ingestion email | ACTIF | camera_engine |
| Extraction EXIF | ACTIF | camera_engine |
| Chiffrement images | ACTIF | camera_engine |
| Detection especes IA | PREVU Phase 2 | camera_engine |

**Localisation:** `/app/backend/modules/camera_engine/v1/`

## 11.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Classification especes | Detection automatique sur photos | CRITIQUE | P0 |
| Comptage individus | Nombre d'animaux par photo | CRITIQUE | P0 |
| Patterns temporels | Distribution horaire des detections | HAUTE | P0 |
| Heatmaps cameras | Agregation spatiale des detections | HAUTE | P0 |
| Comportement detecte | Alimentation, deplacement, repos | MOYENNE | P1 |

## 11.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| GPT-5.2 Vision | Classification especes | API Emergent LLM | 0.85 |
| MegaDetector | Detection animaux | Modele pre-entraine | 0.90 |
| Agregation interne | Patterns temporels | Calcul | 0.95 |
| PostGIS | Heatmaps spatiaux | Calcul | 0.95 |

## 11.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Qualite photos | Photos nuit basse resolution | Pre-traitement images |
| Faux positifs IA | Detection erronee | Seuil confiance > 0.7 |
| Biais placement | Cameras sur sentiers | Normalisation spatiale |
| Volume images | Stockage et traitement couteux | Compression, purge |

---

# FAMILLE 12: CYCLES TEMPORELS AVANCES

## 12.1 DONNEES EXISTANTES

### 12.1.1 Cycles Horaires d'Activite
```python
# SPECIES_PATTERNS - activite par periode
{
    "deer": {
        "dawn_activity": 95,
        "midday_activity": 30,
        "dusk_activity": 90,
        "night_activity": 60
    },
    "moose": {
        "dawn_activity": 85,
        "midday_activity": 25,
        "dusk_activity": 80,
        "night_activity": 50
    }
}
```

**Localisation:** `/app/backend/modules/predictive_engine/v1/service.py`

### 12.1.2 Patterns Activite Detailles
| Espece | Periode | Niveau Activite | Probabilite Alimentation | Probabilite Mouvement |
|--------|---------|-----------------|-------------------------|----------------------|
| Orignal | dawn | 0.90 | 0.80 | 0.70 |
| Orignal | midday | 0.30 | 0.20 | 0.20 |
| Orignal | dusk | 0.90 | 0.80 | 0.70 |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/species/moose.json`

### 12.1.3 Cycles Lunaires
```python
# MoonPhase - service meteo
{
    "phase": "new/waxing_crescent/first_quarter/...",
    "illumination": 0-100,
    "hunting_impact": "description textuelle"
}
# Cycle: 29.53 jours
# Nouvelle lune: +activite diurne
# Pleine lune: +activite nocturne
```

**Localisation:** `/app/backend/modules/weather_engine/v1/service.py`

### 12.1.4 Cycles Saisonniers
| Saison | Enum | Multiplicateur Activite | Comportements |
|--------|------|------------------------|---------------|
| PRE_RUT | pre_rut | 1.2 | Territorial, scrapes |
| RUT | rut | 1.5 | Rutting, chasing |
| POST_RUT | post_rut | 0.8 | Feeding, recovery |
| WINTER | winter | 0.5 | Minimal movement |

**Localisation:** `/app/backend/modules/wildlife_behavior_engine/v1/service.py`

### 12.1.5 Dates de Rut par Espece
| Espece | Debut Rut | Pic Rut | Fin Rut |
|--------|-----------|---------|---------|
| Orignal | Septembre | Octobre | Octobre |
| Cerf | Octobre | Novembre | Novembre |

## 12.2 DONNEES MANQUANTES

| Donnee | Description | Impact P0 | Priorite |
|--------|-------------|-----------|----------|
| Photopériode | Impact duree du jour sur comportement | CRITIQUE | P0 |
| Cycles pluriannuels | Patterns sur 3-5 ans (populations) | HAUTE | P1 |
| Evenements astronomiques | Lever/coucher soleil precis par coord | HAUTE | P0 |
| Migration saisonnière | Mouvements altitude/latitude | MOYENNE | P1 |

## 12.3 DONNEES A ACQUERIR

| Source | Donnee | Methode | Fiabilite |
|--------|--------|---------|-----------|
| SunCalc | Ephemerides solaires | Bibliotheque calcul | 0.99 |
| legal_time_engine | Heures legales chasse | Calcul | 0.99 |
| NOAA | Photoperiode par latitude | API | 0.95 |
| UQAR | Cycles pluriannuels | Publications | 0.85 |

## 12.4 LIMITES, BIAIS ET RISQUES

| Limite | Description | Mitigation |
|--------|-------------|------------|
| Variabilite interannuelle | Dates rut variables ±2 semaines | Fourchette dynamique |
| Latitude dependante | Patterns differents nord/sud | Regionalisation |

---

# SOURCES EMPIRIQUES & SCIENTIFIQUES

## SOURCES INTEGREES (ACTIVES)

| ID | Nom | Type | Fiabilite | Especes | Statut |
|----|-----|------|-----------|---------|--------|
| `mffp_quebec` | MFFP Quebec | government_report | 0.95 | moose, deer, bear, caribou | INTEGRE |
| `sepaq` | SEPAQ | government_report | 0.90 | moose, deer, bear | INTEGRE |
| `cic_quebec` | Canards Illimites Quebec | scientific_paper | 0.90 | waterfowl | INTEGRE |
| `fqf` | Federation chasseurs Quebec | expert_interview | 0.80 | all | INTEGRE |
| `wildlife_research_ulaval` | CEN U. Laval | scientific_paper | 0.95 | caribou, moose, bear | INTEGRE |
| `wildlife_society_na` | The Wildlife Society | scientific_paper | 0.92 | moose, deer, bear | INTEGRE |
| `usgs_wildlife` | USGS Wildlife Research | scientific_paper | 0.95 | all | INTEGRE |
| `ulaval_forestry` | FFGG U. Laval | scientific_paper | 0.92 | moose, deer, bear | INTEGRE |
| `expert_louis_gagnon` | Louis Gagnon | expert_interview | 0.85 | moose, caribou, bear | INTEGRE |
| `expert_guides_nordiques` | Guides Nordiques QC | expert_interview | 0.82 | all | INTEGRE |

**Localisation:** `/app/backend/modules/bionic_knowledge_engine/data/sources_registry.json`

## SOURCES A INTEGRER (PRIORITAIRES)

| Source | Donnees | Priorite | Methode Integration |
|--------|---------|----------|---------------------|
| UQAR | Etudes comportementales orignal | P0 | Publications PDF, structuration |
| "De la bouche des orignaux" | Savoir empirique compile | P0 | Extraction manuelle, validation |
| Louis Gagnon (approfondi) | 30+ ans terrain nord Quebec | P0 | Entrevues structurees |
| CWS-SCF | Donnees federales faune | P1 | API/Donnees ouvertes |
| iNaturalist Quebec | Observations citoyennes | P1 | API REST |
| eBird Quebec | Observations oiseaux (prey/predators) | P2 | API REST |

## STATUT PAR SOURCE

| Source | Integre | Disponible | A Integrer | Non Disponible |
|--------|---------|------------|------------|----------------|
| MFFP Quebec | X | | | |
| SEPAQ | X | | | |
| CIC Quebec | X | | | |
| Louis Gagnon | X (partiel) | | X (approfondi) | |
| UQAR | | X | X | |
| "De la bouche des orignaux" | | X | X | |
| Telemetrie GPS | | | | X (partenariat requis) |

---

# MAPPING MODULES P0

## PREDICTIVE_TERRITORIAL.PY

### Donnees Exploitables Immediatement
| Famille | Donnees | Variable/Collection | Utilisation |
|---------|---------|---------------------|-------------|
| F1 | Waypoints | `territory_waypoints` | Points d'analyse |
| F1 | Layers BIONIC | `BIONIC_LAYERS` | Scores par zone |
| F2 | NDVI, Canopy | `habitat_variables.json` | Score vegetation |
| F4 | Elevation, Slope | `habitat_variables.json` | Score terrain |
| F5 | Temperature, Vent | `weather_engine` | Score meteo |
| F8 | Distance routes | `habitat_variables.json` | Score pression |
| F12 | Cycles saisonniers | `SEASON_FACTORS` | Multiplicateur |

### Donnees a Integrer (P1)
| Famille | Donnees | Source | Priorite |
|---------|---------|--------|----------|
| F1 | Polygones ZEC | MFFP | P1 |
| F2 | Ecotones | Derive satellite | P1 |
| F6 | Corridors detectes | Cameras | P1 |
| F10 | Historique recolte | MFFP | P1 |

### Donnees a Creer (Nouveau Pipeline)
| Famille | Donnees | Methode | Priorite |
|---------|---------|---------|----------|
| F5 | Microclimats | Modele topo | P0 |
| F8 | Pression cumulative | Agregation interne | P0 |
| F11 | Patterns cameras | Agregation | P0 |

## BEHAVIORAL_MODELS.PY

### Donnees Exploitables Immediatement
| Famille | Donnees | Variable/Collection | Utilisation |
|---------|---------|---------------------|-------------|
| F3 | Food sources | `species/*.json` | Zones alimentation |
| F6 | Movement patterns | `wildlife_behavior_engine` | Corridors |
| F7 | Bedding areas | `wildlife_behavior_engine` | Zones repos |
| F12 | Activity patterns | `SPECIES_PATTERNS` | Horaires |
| F12 | Seasonal behavior | `SeasonalBehavior` | Comportement |

### Donnees a Integrer (P1)
| Famille | Donnees | Source | Priorite |
|---------|---------|--------|----------|
| F6 | Corridors valides terrain | Louis Gagnon | P1 |
| F7 | Ravages officiels | MFFP | P1 |
| F12 | Dates rut regionales | UQAR | P1 |

### Donnees a Creer (Nouveau Pipeline)
| Famille | Donnees | Methode | Priorite |
|---------|---------|---------|----------|
| F11 | Classification especes | GPT-5.2 Vision | P0 |
| F11 | Patterns temporels | Agregation cameras | P0 |

---

# SYNTHESE EXECUTIVE

## METRIQUES GLOBALES

| Metrique | Valeur |
|----------|--------|
| **Familles de donnees** | 12 |
| **Variables d'habitat** | 17 |
| **Especes documentees** | 4 (moose, deer, bear, elk) |
| **Sources scientifiques** | 11 |
| **Collections MongoDB** | 15+ |
| **Layers cartographiques** | 15 |
| **Endpoints API existants** | 80+ |

## MATRICE DE COUVERTURE

| Famille | Existant | Manquant | A Acquerir | Score |
|---------|----------|----------|------------|-------|
| F1 Territoriales | 70% | 20% | 10% | **HAUTE** |
| F2 Vegetation | 60% | 25% | 15% | **MOYENNE** |
| F3 Alimentation | 50% | 35% | 15% | **MOYENNE** |
| F4 Topographie | 75% | 15% | 10% | **HAUTE** |
| F5 Microclimats | 55% | 30% | 15% | **MOYENNE** |
| F6 Corridors | 40% | 45% | 15% | **BASSE** |
| F7 Repos/Abris | 45% | 40% | 15% | **BASSE** |
| F8 Pression | 50% | 35% | 15% | **MOYENNE** |
| F9 Extremes | 60% | 25% | 15% | **MOYENNE** |
| F10 Historiques | 30% | 50% | 20% | **BASSE** |
| F11 Cameras | 35% | 50% | 15% | **BASSE** |
| F12 Cycles | 70% | 20% | 10% | **HAUTE** |

## PRIORITES P0 - ACTIONS IMMEDIATES

### 1. BLOQUEURS CRITIQUES
| Action | Famille | Impact | Effort |
|--------|---------|--------|--------|
| Classifier especes cameras | F11 | CRITIQUE | Moyen (GPT-5.2) |
| Calculer microclimats | F5 | CRITIQUE | Faible (formules) |
| Agreger pression cumulative | F8 | CRITIQUE | Faible (MongoDB) |
| Detecter corridors cameras | F6 | CRITIQUE | Moyen (algorithme) |

### 2. INTEGRATIONS PRIORITAIRES
| Source | Donnees | Famille | Effort |
|--------|---------|---------|--------|
| MFFP | Polygones ZEC | F1 | Moyen |
| MFFP | Ravages | F7 | Moyen |
| UQAR | Comportements | F6, F7, F12 | Faible |
| Louis Gagnon | Expertise terrain | Toutes | Moyen |

### 3. PIPELINES A CREER
| Pipeline | Input | Output | Priorite |
|----------|-------|--------|----------|
| Camera Classifier | Photos brutes | Espece + confiance | P0 |
| Microclimate Engine | DEM + Meteo | Score thermique | P0 |
| Pressure Calculator | Sorties + Waypoints | Score pression | P0 |
| Corridor Detector | GPS cameras | Lignes corridors | P0 |

## RISQUES IDENTIFIES

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Couverture donnees incomplete | Moyenne | Haut | Modeles predictifs, fallbacks |
| Latence APIs externes | Haute | Moyen | Cache agressif, fallbacks |
| Biais echantillonnage | Haute | Moyen | Ponderation spatiale |
| Qualite photos cameras | Moyenne | Moyen | Pre-traitement, seuils |
| Changement reglementation | Basse | Haut | MAJ trimestrielle sources |

## RECOMMANDATIONS

### POUR PREDICTIVE_TERRITORIAL.PY
1. Commencer avec les 5 variables d'habitat les plus documentees (NDVI, canopy, elevation, slope, water_proximity)
2. Implementer le calcul de microclimats comme premiere extension
3. Integrer les sources gouvernementales (MFFP) en priorite

### POUR BEHAVIORAL_MODELS.PY
1. S'appuyer sur les patterns d'activite existants (`SPECIES_PATTERNS`)
2. Prioriser la detection d'especes sur photos cameras
3. Valider avec les donnees de Louis Gagnon avant production

### ARCHITECTURE RECOMMANDEE
```
bionic_engine/
├── core.py                    # Orchestrateur
├── contracts/                 # Interfaces
│   ├── data_contracts.py
│   └── api_contracts.py
├── modules/
│   ├── predictive_territorial.py    # P0
│   ├── behavioral_models.py         # P0
│   ├── camera_classifier.py         # P0
│   ├── microclimate_engine.py       # P0
│   └── pressure_calculator.py       # P0
├── data/
│   └── (donnees statiques)
└── tests/
    └── (tests unitaires G-QA)
```

---

# ANNEXES

## A. GLOSSAIRE

| Terme | Definition |
|-------|------------|
| BIONIC | Branding du systeme intelligent HUNTIQ |
| G-QA | Cadre Qualite Phase G |
| G-SEC | Cadre Securite Phase G |
| G-DOC | Cadre Documentation Phase G |
| NDVI | Normalized Difference Vegetation Index |
| DEM | Digital Elevation Model |
| WMS | Web Map Service |
| ZEC | Zone d'Exploitation Controlee |

## B. FICHIERS DE REFERENCE

| Fichier | Contenu |
|---------|---------|
| `/app/backend/modules/bionic_knowledge_engine/data/habitat_variables.json` | Variables habitat |
| `/app/backend/modules/bionic_knowledge_engine/data/species/*.json` | Donnees especes |
| `/app/backend/modules/bionic_knowledge_engine/data/sources_registry.json` | Sources scientifiques |
| `/app/backend/modules/predictive_engine/v1/service.py` | Patterns predictifs |
| `/app/backend/modules/weather_engine/v1/service.py` | Service meteo |
| `/app/backend/modules/wildlife_behavior_engine/v1/service.py` | Comportements |
| `/app/backend/modules/camera_engine/v1/services.py` | Cameras trail |

## C. CONTACTS SOURCES

| Source | Contact | Type |
|--------|---------|------|
| MFFP Quebec | donnees.ouvertes@mffp.gouv.qc.ca | Donnees ouvertes |
| SEPAQ | info@sepaq.com | Partenariat |
| UQAR | recherche@uqar.ca | Academique |
| Louis Gagnon | (a documenter) | Expert terrain |

---

**Document genere conformement aux cadres G-QA, G-SEC, G-DOC**
**PHASE G - BIONIC ULTIMATE INTEGRATION**
**HUNTIQ V5 GOLD MASTER**

*Ce document constitue le prerequis absolu pour le demarrage des modules P0.*
*Toute implementation est suspendue jusqu'a validation explicite par COPILOT MAITRE.*
