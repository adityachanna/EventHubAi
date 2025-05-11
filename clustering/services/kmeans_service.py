from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import re

# --- User-Agent Parsing ---
def parse_user_agent(user_agent_string):
    """Rudimentary parsing of User-Agent string to get OS and device type."""
    device_type = "desktop" # Default
    os_type = "unknown"

    if user_agent_string:
        ua = user_agent_string.lower()
        if "iphone" in ua or "android" in ua or "mobile" in ua:
            device_type = "mobile"
        elif "ipad" in ua or "tablet" in ua:
            device_type = "tablet"
        
        if "windows" in ua:
            os_type = "windows"
        elif "mac os x" in ua or "macos" in ua:
            os_type = "macos"
        elif "linux" in ua:
            os_type = "linux"
        elif "android" in ua:
            os_type = "android"
        elif "iphone" in ua or "ipad" in ua:
            os_type = "ios"
            
    # Convert to numerical representations for clustering
    device_type_map = {"desktop": 0, "mobile": 1, "tablet": 2}
    os_type_map = {"windows": 0, "macos": 1, "linux": 2, "android": 3, "ios": 4, "unknown": 5}
    
    return device_type_map.get(device_type, 0), os_type_map.get(os_type, 5)

# --- Synthetic Data Generation ---
def generate_synthetic_data(n_samples_per_profile=150):
    """
    Generates synthetic data for K-means clustering based on geographic profiles
    and returns the data along with ideal geographic centers for each tier.
    """
    data = []
    np.random.seed(42) # for reproducibility

    # Define ideal geographic centers based on generation parameters
    ideal_centers = {
        "HIGH_USA": [37.5, -95.0],    # Approx. center of USA data generation
        "HIGH_EUROPE": [52.5, 15.0],  # Approx. center of Europe data generation
        "MID_ASIA": [30.0, 95.0],     # Approx. center of Asia data generation
        "LOW_AFRICA": [0.0, 17.5]     # Approx. center of Africa data generation
    }

    # Profile 1: High Price Tier (USA & Europe)
    # USA-like part
    for _ in range(n_samples_per_profile // 2):
        lat = np.random.uniform(25, 50)     # USA Latitude
        lon = np.random.uniform(-125, -65)  # USA Longitude
        device_type = np.random.choice([0, 1, 2]) # desktop, mobile, tablet
        os_type = np.random.choice([0, 1, 4])    # Windows, macOS, iOS
        pixel_ratio = np.random.choice([1.0, 1.5, 2.0, 2.5])
        data.append([lat, lon, device_type, os_type, pixel_ratio])
    # Europe-like part
    for _ in range(n_samples_per_profile - (n_samples_per_profile // 2)):
        lat = np.random.uniform(35, 70)     # Europe Latitude
        lon = np.random.uniform(-10, 40)    # Europe Longitude
        device_type = np.random.choice([0, 1, 2]) # desktop, mobile, tablet
        os_type = np.random.choice([0, 1, 3, 4]) # Windows, macOS, Android, iOS
        pixel_ratio = np.random.choice([1.5, 2.0, 2.5, 3.0])
        data.append([lat, lon, device_type, os_type, pixel_ratio])

    # Profile 2: Middle Price Tier (Asia)
    for _ in range(n_samples_per_profile):
        lat = np.random.uniform(0, 60)      # Asia Latitude
        lon = np.random.uniform(60, 130)    # Asia Longitude
        device_type = np.random.choice([1, 2]) # Mostly Mobile/Tablet
        os_type = np.random.choice([3, 4, 5])   # Android, iOS, Unknown
        pixel_ratio = np.random.choice([1.0, 1.5, 2.0, 2.5])
        data.append([lat, lon, device_type, os_type, pixel_ratio])

    # Profile 3: Low Price Tier (Africa)
    for _ in range(n_samples_per_profile):
        lat = np.random.uniform(-35, 35)    # Africa Latitude
        lon = np.random.uniform(-20, 55)    # Africa Longitude
        device_type = 1                     # Mostly Mobile
        os_type = np.random.choice([3, 5])    # Android, Unknown
        pixel_ratio = np.random.choice([1.0, 1.5])
        data.append([lat, lon, device_type, os_type, pixel_ratio])
    
    return np.array(data), ideal_centers

# --- Model Training & Tier Mapping ---
N_CLUSTERS = 3
X_synthetic_data, IDEAL_GEO_CENTERS = generate_synthetic_data(n_samples_per_profile=150)

SCALER = StandardScaler()
X_scaled_synthetic = SCALER.fit_transform(X_synthetic_data)

KMEANS_MODEL = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
KMEANS_MODEL.fit(X_scaled_synthetic)

# Global map for cluster index to price adjustment factor
CLUSTER_ADJUSTMENT_FACTORS = {}

def _determine_and_set_cluster_adjustments():
    global CLUSTER_ADJUSTMENT_FACTORS
    actual_centroids_scaled = KMEANS_MODEL.cluster_centers_
    actual_centroids_unscaled = SCALER.inverse_transform(actual_centroids_scaled)

    tier_price_adjustments = {
        "HIGH_USA": 1.10,
        "HIGH_EUROPE": 1.10,
        "MID_ASIA": 1.00,
        "LOW_AFRICA": 0.90
    }
    
    temp_cluster_map = {} # Store provisional assignments

    for i, actual_centroid_data in enumerate(actual_centroids_unscaled):
        actual_centroid_geo = np.array([actual_centroid_data[0], actual_centroid_data[1]]) # Lat, Lon
        
        min_dist = float('inf')
        best_tier_name = None
        
        for tier_name, ideal_center_coords in IDEAL_GEO_CENTERS.items():
            dist = np.linalg.norm(actual_centroid_geo - np.array(ideal_center_coords))
            if dist < min_dist:
                min_dist = dist
                best_tier_name = tier_name
        
        if best_tier_name:
            temp_cluster_map[i] = tier_price_adjustments[best_tier_name]
        else:
            # This case should ideally not be reached if IDEAL_GEO_CENTERS is populated
            temp_cluster_map[i] = 0.90

    # Ensure all N_CLUSTERS have an assignment, even if some map to the same tier (which is expected)
    CLUSTER_ADJUSTMENT_FACTORS = temp_cluster_map

_determine_and_set_cluster_adjustments() # Initialize the mapping on script load

def get_user_cluster(latitude, longitude, user_agent_string, device_pixel_ratio_str: str = None):
    """Determines the user's cluster based on their data using the trained model."""
    device_numeric, os_numeric = parse_user_agent(user_agent_string)

    lat = latitude if latitude is not None else 0.0 
    lon = longitude if longitude is not None else 0.0
    
    pixel_ratio = 1.0 # Default device pixel ratio
    if device_pixel_ratio_str:
        try:
            val = float(device_pixel_ratio_str)
            if val > 0:
                 pixel_ratio = val
        except ValueError:
            pixel_ratio = 1.0 # Fallback to default if conversion fails

    # Features: latitude, longitude, device_type_numeric, os_type_numeric, pixel_ratio
    user_features = np.array([[lat, lon, device_numeric, os_numeric, pixel_ratio]])

    scaled_user_features = SCALER.transform(user_features)
    cluster_label = KMEANS_MODEL.predict(scaled_user_features)[0]
    return int(cluster_label)

# --- Price Adjustment Logic ---
def adjust_price_based_on_cluster(base_price, cluster_label):
    """Adjusts the base price based on the assigned cluster label."""
    adjustment_factor = CLUSTER_ADJUSTMENT_FACTORS.get(cluster_label, 1.0) # Default to base price if label not in map
    adjusted_price = base_price * adjustment_factor
    return round(adjusted_price, 2)

# --- Main Service Functions ---
def get_dynamically_adjusted_price(
    base_price: float, 
    latitude: float = None, 
    longitude: float = None, 
    user_agent_string: str = None,
    device_pixel_ratio: str = None
):
    user_agent_string = user_agent_string or ""
    cluster_label = get_user_cluster(latitude, longitude, user_agent_string, device_pixel_ratio)
    adjusted_price = adjust_price_based_on_cluster(base_price, cluster_label)
    return adjusted_price, cluster_label

def cluster_data(data, n_clusters):
    """Cluster data using KMeans algorithm"""
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    return kmeans.labels_.tolist()
