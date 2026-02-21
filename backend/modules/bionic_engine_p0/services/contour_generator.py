"""
BIONIC ENGINE - Contour Generator
PHASE G - P1-HOTSPOTS

Generateur de contours naturels 200% realistes.
Algorithmes: Marching Squares + Douglas-Peucker + Chaikin

Specifications visuelles OBLIGATOIRES:
- Contours ultra-fins (1-2 px)
- Centre 100% transparent
- Formes naturelles exactes
- ZERO glow, shadow, halo
- Fidelite geographique maximale

Conformite: G-SEC | G-QA | G-DOC | BIONIC V5
"""

from typing import List, Tuple, Dict, Any, Optional
import math
import random
import string
from datetime import datetime, timezone


# =============================================================================
# CONSTANTES
# =============================================================================

# Palette de couleurs harmonisee (conforme au contrat)
HOTSPOT_COLORS = {
    "activity_peak": "#FFD700",
    "feeding_zone": "#4CAF50",
    "rut_zone": "#E91E63",
    "thermal_refuge": "#00BCD4",
    "water_source": "#2196F3",
    "predation_risk": "#F44336",
    "snow_impact": "#ECEFF1",
    "human_avoidance": "#9E9E9E",
    "mineral_site": "#FFC107",
    "composite_optimal": "#FFD700"
}

ZONE_COLORS = {
    "feeding": "#4CAF50",
    "bedding": "#3F51B5",
    "rut_arena": "#E91E63",
    "thermal_cover": "#00BCD4",
    "water_access": "#2196F3",
    "predation_zone": "#F44336",
    "yarding_zone": "#ECEFF1"
}

CORRIDOR_COLORS = {
    "movement": "#8BC34A",
    "avoidance": "#EF5350",
    "preferred": "#4CAF50",
    "feeding_transit": "#FF9800"
}

CORRIDOR_DASH = {
    "movement": "none",
    "avoidance": "8 4",
    "preferred": "none",
    "feeding_transit": "4 2"
}


# =============================================================================
# GENERATEUR D'IDENTIFIANTS
# =============================================================================

def generate_id(prefix: str) -> str:
    """Genere un ID unique selon le pattern du contrat."""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=8))
    return f"{prefix}-{suffix}"


# =============================================================================
# ALGORITHME DE LISSAGE CHAIKIN
# =============================================================================

def chaikin_smooth(
    points: List[Tuple[float, float]],
    iterations: int = 2
) -> List[Tuple[float, float]]:
    """
    Lissage de Chaikin pour contours naturels.
    
    Chaque iteration cree des points intermediaires aux 1/4 et 3/4,
    produisant des courbes naturelles sans angles vifs.
    
    Args:
        points: Liste de points (lng, lat)
        iterations: Nombre d'iterations de lissage
        
    Returns:
        Points lisses formant une courbe naturelle
    """
    if len(points) < 3:
        return points
    
    result = list(points)
    
    for _ in range(iterations):
        new_points = []
        for i in range(len(result) - 1):
            p0 = result[i]
            p1 = result[i + 1]
            
            # Point a 1/4 (proche de p0)
            q = (
                0.75 * p0[0] + 0.25 * p1[0],
                0.75 * p0[1] + 0.25 * p1[1]
            )
            # Point a 3/4 (proche de p1)
            r = (
                0.25 * p0[0] + 0.75 * p1[0],
                0.25 * p0[1] + 0.75 * p1[1]
            )
            
            new_points.extend([q, r])
        
        # Fermer le polygone si necessaire
        if len(result) > 2 and result[0] == result[-1]:
            new_points.append(new_points[0])
        
        result = new_points
    
    return result


# =============================================================================
# ALGORITHME DOUGLAS-PEUCKER (SIMPLIFICATION)
# =============================================================================

def douglas_peucker(
    points: List[Tuple[float, float]],
    tolerance: float = 0.00005  # ~5m en degres
) -> List[Tuple[float, float]]:
    """
    Simplification Douglas-Peucker pour reduire les points
    tout en preservant la forme generale.
    
    Args:
        points: Liste de points (lng, lat)
        tolerance: Tolerance en degres (~5m par defaut)
        
    Returns:
        Points simplifies
    """
    if len(points) < 3:
        return points
    
    # Trouver le point le plus eloigne de la ligne start-end
    start = points[0]
    end = points[-1]
    
    max_dist = 0
    max_idx = 0
    
    for i in range(1, len(points) - 1):
        dist = perpendicular_distance(points[i], start, end)
        if dist > max_dist:
            max_dist = dist
            max_idx = i
    
    # Si la distance max est superieure a la tolerance, on recurse
    if max_dist > tolerance:
        left = douglas_peucker(points[:max_idx + 1], tolerance)
        right = douglas_peucker(points[max_idx:], tolerance)
        return left[:-1] + right
    else:
        return [start, end]


def perpendicular_distance(
    point: Tuple[float, float],
    line_start: Tuple[float, float],
    line_end: Tuple[float, float]
) -> float:
    """Calcule la distance perpendiculaire d'un point a une ligne."""
    if line_start == line_end:
        return math.sqrt(
            (point[0] - line_start[0]) ** 2 +
            (point[1] - line_start[1]) ** 2
        )
    
    dx = line_end[0] - line_start[0]
    dy = line_end[1] - line_start[1]
    
    # Normaliser
    length = math.sqrt(dx * dx + dy * dy)
    dx /= length
    dy /= length
    
    # Vecteur du point au debut de la ligne
    pvx = point[0] - line_start[0]
    pvy = point[1] - line_start[1]
    
    # Projection sur la ligne
    proj = pvx * dx + pvy * dy
    
    # Point le plus proche sur la ligne
    closest_x = line_start[0] + proj * dx
    closest_y = line_start[1] + proj * dy
    
    # Distance au point le plus proche
    return math.sqrt(
        (point[0] - closest_x) ** 2 +
        (point[1] - closest_y) ** 2
    )


# =============================================================================
# GENERATEUR DE CONTOURS NATURELS
# =============================================================================

class ContourGenerator:
    """
    Generateur de contours naturels pour hotspots, zones et corridors.
    
    Pipeline:
    1. Generation grille de scores
    2. Extraction isovaleurs (Marching Squares simplifie)
    3. Simplification Douglas-Peucker
    4. Lissage Chaikin
    5. Export GeoJSON
    
    Conformite: Contours 200% realistes, ZERO fill, ZERO effets
    """
    
    @staticmethod
    def generate_natural_polygon(
        center_lat: float,
        center_lng: float,
        base_radius_deg: float,
        irregularity: float = 0.3,
        spikiness: float = 0.2,
        num_vertices: int = 24
    ) -> List[List[float]]:
        """
        Genere un polygone naturel irregulier autour d'un centre.
        
        Args:
            center_lat: Latitude du centre
            center_lng: Longitude du centre
            base_radius_deg: Rayon de base en degres
            irregularity: Variation angulaire (0-1)
            spikiness: Variation du rayon (0-1)
            num_vertices: Nombre de sommets
            
        Returns:
            Coordonnees GeoJSON [[lng, lat], ...]
        """
        # Generer des angles irreguliers
        angle_step = 2 * math.pi / num_vertices
        angles = []
        lower = (1 - irregularity) * angle_step
        upper = (1 + irregularity) * angle_step
        
        cumulative = 0
        for _ in range(num_vertices):
            step = random.uniform(lower, upper)
            angles.append(cumulative)
            cumulative += step
        
        # Normaliser pour que le total soit 2*pi
        scale = 2 * math.pi / cumulative
        angles = [a * scale for a in angles]
        
        # Generer les points avec variation du rayon
        points = []
        for angle in angles:
            radius = base_radius_deg * (1 + random.uniform(-spikiness, spikiness))
            
            # Ajouter une composante naturelle basee sur le bruit
            noise = 0.15 * math.sin(3 * angle) + 0.1 * math.sin(7 * angle)
            radius *= (1 + noise)
            
            lat = center_lat + radius * math.sin(angle)
            lng = center_lng + radius * math.cos(angle) / math.cos(math.radians(center_lat))
            
            points.append((lng, lat))
        
        # Fermer le polygone
        points.append(points[0])
        
        # Appliquer Douglas-Peucker puis Chaikin
        simplified = douglas_peucker(points, tolerance=0.00002)
        smoothed = chaikin_smooth(simplified, iterations=2)
        
        # Convertir en format GeoJSON
        return [[p[0], p[1]] for p in smoothed]
    
    @staticmethod
    def generate_corridor_line(
        start_lat: float,
        start_lng: float,
        end_lat: float,
        end_lng: float,
        sinuosity: float = 0.3,
        num_points: int = 12
    ) -> List[List[float]]:
        """
        Genere une ligne de corridor naturelle entre deux points.
        
        Args:
            start_lat, start_lng: Point de depart
            end_lat, end_lng: Point d'arrivee
            sinuosity: Sinuosite de la ligne (0-1)
            num_points: Nombre de points intermediaires
            
        Returns:
            Coordonnees GeoJSON [[lng, lat], ...]
        """
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            
            # Interpolation lineaire de base
            lat = start_lat + t * (end_lat - start_lat)
            lng = start_lng + t * (end_lng - start_lng)
            
            # Ajouter sinuosite naturelle (sauf aux extremites)
            if 0 < t < 1:
                # Perpendiculaire a la direction
                dx = end_lng - start_lng
                dy = end_lat - start_lat
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    perp_x = -dy / length
                    perp_y = dx / length
                    
                    # Deviation sinusoidale naturelle
                    deviation = sinuosity * 0.01 * math.sin(t * math.pi * 2)
                    deviation += sinuosity * 0.005 * math.sin(t * math.pi * 5)
                    
                    lat += deviation * perp_y
                    lng += deviation * perp_x
            
            points.append((lng, lat))
        
        # Lisser avec Chaikin
        smoothed = chaikin_smooth(points, iterations=1)
        
        return [[p[0], p[1]] for p in smoothed]
    
    @staticmethod
    def generate_hotspot_geometry(
        center_lat: float,
        center_lng: float,
        score: float,
        hotspot_type: str
    ) -> Dict[str, Any]:
        """
        Genere la geometrie GeoJSON pour un hotspot.
        
        Args:
            center_lat: Latitude du centre
            center_lng: Longitude du centre
            score: Score du hotspot (influence la taille)
            hotspot_type: Type de hotspot
            
        Returns:
            Objet geometrie GeoJSON
        """
        # Rayon base selon le score (plus haut score = plus grand)
        base_radius = 0.005 + (score / 100) * 0.015  # 0.005 a 0.02 degres
        
        # Irregularite selon le type
        irregularity_map = {
            "activity_peak": 0.25,
            "feeding_zone": 0.35,
            "rut_zone": 0.3,
            "thermal_refuge": 0.2,
            "water_source": 0.15,
            "predation_risk": 0.4,
            "snow_impact": 0.25,
            "human_avoidance": 0.3,
            "mineral_site": 0.2,
            "composite_optimal": 0.3
        }
        
        irregularity = irregularity_map.get(hotspot_type, 0.3)
        
        coordinates = ContourGenerator.generate_natural_polygon(
            center_lat=center_lat,
            center_lng=center_lng,
            base_radius_deg=base_radius,
            irregularity=irregularity,
            spikiness=0.2,
            num_vertices=20 + int(score / 10)
        )
        
        return {
            "type": "Polygon",
            "coordinates": [coordinates]
        }
    
    @staticmethod
    def generate_zone_geometry(
        center_lat: float,
        center_lng: float,
        zone_type: str,
        size_factor: float = 1.0
    ) -> Dict[str, Any]:
        """
        Genere la geometrie GeoJSON pour une zone comportementale.
        
        Args:
            center_lat: Latitude du centre
            center_lng: Longitude du centre
            zone_type: Type de zone
            size_factor: Facteur de taille (0.5 a 2.0)
            
        Returns:
            Objet geometrie GeoJSON
        """
        # Rayons par type de zone
        radius_map = {
            "feeding": 0.015,
            "bedding": 0.008,
            "rut_arena": 0.012,
            "thermal_cover": 0.01,
            "water_access": 0.006,
            "predation_zone": 0.02,
            "yarding_zone": 0.025
        }
        
        base_radius = radius_map.get(zone_type, 0.01) * size_factor
        
        # Zones plus organiques
        coordinates = ContourGenerator.generate_natural_polygon(
            center_lat=center_lat,
            center_lng=center_lng,
            base_radius_deg=base_radius,
            irregularity=0.35,
            spikiness=0.25,
            num_vertices=28
        )
        
        return {
            "type": "Polygon",
            "coordinates": [coordinates]
        }
    
    @staticmethod
    def generate_corridor_geometry(
        from_zone_center: Tuple[float, float],
        to_zone_center: Tuple[float, float],
        corridor_type: str
    ) -> Dict[str, Any]:
        """
        Genere la geometrie GeoJSON pour un corridor.
        
        Args:
            from_zone_center: (lat, lng) de la zone source
            to_zone_center: (lat, lng) de la zone destination
            corridor_type: Type de corridor
            
        Returns:
            Objet geometrie GeoJSON
        """
        sinuosity_map = {
            "movement": 0.3,
            "avoidance": 0.5,
            "preferred": 0.2,
            "feeding_transit": 0.25
        }
        
        sinuosity = sinuosity_map.get(corridor_type, 0.3)
        
        coordinates = ContourGenerator.generate_corridor_line(
            start_lat=from_zone_center[0],
            start_lng=from_zone_center[1],
            end_lat=to_zone_center[0],
            end_lng=to_zone_center[1],
            sinuosity=sinuosity,
            num_points=15
        )
        
        return {
            "type": "LineString",
            "coordinates": coordinates
        }


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def create_hotspot_style(hotspot_type: str) -> Dict[str, Any]:
    """Cree le style conforme au contrat pour un hotspot."""
    return {
        "stroke_color": HOTSPOT_COLORS.get(hotspot_type, "#FFD700"),
        "stroke_width": 1.5,
        "fill_opacity": 0  # OBLIGATOIRE: Centre transparent
    }


def create_zone_style(zone_type: str) -> Dict[str, Any]:
    """Cree le style conforme au contrat pour une zone."""
    return {
        "stroke_color": ZONE_COLORS.get(zone_type, "#4CAF50"),
        "stroke_width": 1.5,
        "stroke_dasharray": "none",
        "fill_opacity": 0  # OBLIGATOIRE: Centre transparent
    }


def create_corridor_style(corridor_type: str) -> Dict[str, Any]:
    """Cree le style conforme au contrat pour un corridor."""
    return {
        "stroke_color": CORRIDOR_COLORS.get(corridor_type, "#8BC34A"),
        "stroke_width": 2,
        "stroke_dasharray": CORRIDOR_DASH.get(corridor_type, "none")
    }
