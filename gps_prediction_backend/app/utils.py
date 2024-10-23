import math

def calculate_distance(point_a, point_b):
    """
    Calculate the Haversine distance between two latitude/longitude points.
    """
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = math.radians(point_a[0]), math.radians(point_a[1])
    lat2, lon2 = math.radians(point_b[0]), math.radians(point_b[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in kilometers
    return distance

def calculate_speed(distance, time_in_hours):
    """
    Calculate speed given distance and time.
    """
    if time_in_hours == 0:
        return 0
    return distance / time_in_hours

def select_calculation_mode(mode, point_a, point_b, time_elapsed):
    """
    Selects the calculation to be performed based on the mode type.
    """
    if mode == 'distance':
        return calculate_distance(point_a, point_b)
    elif mode == 'speed':
        distance = calculate_distance(point_a, point_b)
        return calculate_speed(distance, time_elapsed)
    else:
        raise ValueError("Invalid mode selected.")
