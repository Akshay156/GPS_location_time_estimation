# mock_main.py

from mock_google_api_handler import MockGoogleAPIHandler
from mock_algorithm_operations_handler import MockAlgorithmOperationsHandler
from mock_ui_handler import MockUIHandler

def main():
    # Initialize the mock Google API handler
    google_api_handler = MockGoogleAPIHandler()

    # Fetch route data from the mock handler
    origin = 'HSR Layout, Bangalore, Karnataka'
    destination = 'ITI Layout, Bangalore, Karnataka'
    route_data = google_api_handler.get_route(origin, destination)
    
    # Get polyline points for the route
    polyline_points = google_api_handler.get_polyline_points(route_data)
    
    # Initialize the algorithm handler with polyline points
    algo_handler = MockAlgorithmOperationsHandler(polyline_points)

    # Calculate the ETA (in minutes)
    eta = google_api_handler.get_eta(origin, destination)
    print(f"Estimated Time of Arrival: {eta:.2f} minutes")

    # Simulate driver's progress (e.g., after 5 minutes)
    elapsed_time = 5  # minutes
    estimated_driver_location = algo_handler.estimate_driver_position(elapsed_time, eta)

    # Calculate how much of the route is covered
    covered_percentage = algo_handler.get_covered_percentage(estimated_driver_location)
    print(f"Driver has covered: {covered_percentage:.2f}% of the route")

    # Initialize UI handler and draw route on the map
    ui_handler = MockUIHandler(polyline_points[0], polyline_points[-1], polyline_points)
    ui_handler.draw_route()

    # Add driver's estimated position to the map
    ui_handler.add_driver_marker(estimated_driver_location)

    # Save and display the map
    ui_handler.display_map()

if __name__ == '__main__':
    main()
