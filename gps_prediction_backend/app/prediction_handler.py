import time
import math
from app.google_api_handler import GoogleAPIHandler  # Adjust the import path as necessary

class PredictionHandler:
    def __init__(self):
        self.route_points = []
        self.start_time = None
        self.initial_location = None
        self.google_api_handler = GoogleAPIHandler()  # Create an instance of the GoogleAPIHandler

    def start_prediction(self, route_points):
        self.route_points = route_points
        self.start_time = time.time()  # Set the start time
        self.initial_location = route_points[0]  # Starting point
        return self.initial_location

    def predict_next_location(self, elapsed_time):
        if not self.route_points:
            return None

        # Calculate which point to predict based on elapsed time
        total_points = len(self.route_points)
        index = int(elapsed_time / 5)  # Since prediction is every 5 seconds

        if index < total_points:
            return self.route_points[index]  # Return the predicted location
        else:
            return self.route_points[-1]  # Return the last point if elapsed time exceeds

    def reset(self, origin, destination):
        """
        Reset the prediction handler by fetching new route points
        from the Google API based on the new origin and destination.
        """
        # Call the Google API to get new directions
        directions_data = self.google_api_handler.get_directions(origin, destination)
        self.route_points = self.google_api_handler.get_polyline_points(directions_data)  # Get new route points
        self.start_time = time.time()  # Reset start time
        self.initial_location = self.route_points[0] if self.route_points else None  # Reset initial location
