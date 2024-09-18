class AlgorithmOperationsHandler:
    def __init__(self):
        pass

    def estimate_driver_position(self, elapsed_time, eta, start_point, end_point):
        # Here we are not estimating position based on polyline, but this function could be modified as needed
        progress_ratio = elapsed_time / eta
        # Assuming a linear path between start_point and end_point
        return [
            start_point[0] + progress_ratio * (end_point[0] - start_point[0]),
            start_point[1] + progress_ratio * (end_point[1] - start_point[1])
        ]

    def get_covered_percentage(self, estimated_driver_location, start_point, end_point):
        # Calculate distance covered based on the estimated position
        total_distance = self.calculate_distance(start_point, end_point)
        distance_covered = self.calculate_distance(start_point, estimated_driver_location)
        return (distance_covered / total_distance) * 100
    
    def calculate_distance(self, point1, point2):
        # Simple Euclidean distance calculation
        import math
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
