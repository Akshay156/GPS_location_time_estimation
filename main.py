from handle_google_api import GoogleAPIHandler
from handle_algorithm_operations import AlgorithmOperationsHandler
from handle_ui import UIHandler

def main():
    # Initialize the Google API handler
    google_api_handler = GoogleAPIHandler()

    # Fetch route data from Google Distance Matrix API
    origins = 'HSR Layout, Bangalore, Karnataka'
    destinations = 'ITI Layout, Bangalore, Karnataka'
    route_data = google_api_handler.get_route(origins, destinations)
    
    # Get ETA (in minutes)
    eta = google_api_handler.get_eta(origins, destinations)
    print(f"Estimated Time of Arrival: {eta:.2f} minutes")

    # Simulate driver's progress (e.g., after 5 minutes)
    elapsed_time = 5  # minutes
    start_point = [12.934533, 77.626579]  # Example start point
    end_point = [12.934533, 77.626579]    # Example end point, adjust as needed
    algo_handler = AlgorithmOperationsHandler()
    estimated_driver_location = algo_handler.estimate_driver_position(elapsed_time, eta, start_point, end_point)

    # Calculate how much of the route is covered
    covered_percentage = algo_handler.get_covered_percentage(estimated_driver_location, start_point, end_point)
    print(f"Driver has covered: {covered_percentage:.2f}% of the route")

    # Initialize UI handler and draw route on the map
    ui_handler = UIHandler(start_point, end_point)
    ui_handler.draw_route()

    # Add driver's estimated position to the map
    ui_handler.add_driver_marker(estimated_driver_location)

    # Save and display the map
    ui_handler.display_map()

if __name__ == '__main__':
    main()
