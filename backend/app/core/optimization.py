"""
Optimization algorithms and utilities.
"""
import math
from typing import List, Dict


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula. Returns km."""
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def calculate_total_distance(route: List[Dict]) -> float:
    """Calculate total distance for a route."""
    total = 0.0
    for i in range(len(route) - 1):
        loc1 = route[i].get('location', {})
        loc2 = route[i + 1].get('location', {})
        if loc1 and loc2:
            total += haversine_distance(
                loc1.get('lat', 0), loc1.get('lng', 0),
                loc2.get('lat', 0), loc2.get('lng', 0)
            )
    return total


def nearest_neighbor_tsp(attractions: List[Dict], start_index: int = 0) -> List[Dict]:
    """Solve TSP using Nearest Neighbor heuristic."""
    if len(attractions) <= 1:
        return attractions
    unvisited = attractions.copy()
    route = []
    current = unvisited.pop(start_index)
    route.append(current)
    while unvisited:
        current_loc = current.get('location', {})
        if not current_loc:
            route.extend(unvisited)
            break
        current_lat = current_loc.get('lat', 0)
        current_lng = current_loc.get('lng', 0)
        min_distance = float('inf')
        nearest_idx = 0
        for i, attraction in enumerate(unvisited):
            attr_loc = attraction.get('location', {})
            if attr_loc:
                distance = haversine_distance(
                    current_lat, current_lng,
                    attr_loc.get('lat', 0), attr_loc.get('lng', 0)
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_idx = i
        current = unvisited.pop(nearest_idx)
        route.append(current)
    return route


def estimate_travel_time(distance_km: float, mode: str = "walking") -> int:
    """Estimate travel time. Returns minutes."""
    speeds = {"walking": 5, "driving": 30, "transit": 20, "bicycling": 15}
    speed = speeds.get(mode, 5)
    return int((distance_km / speed) * 60)
