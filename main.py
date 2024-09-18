from handle_google_api import GoogleAPIHandler
from handle_algorithm_operations import AlgorithmOperationsHandler
from handle_ui import UIHandler
import configparser
import os

def main():
    # Initialize the Google API handler
    google_api_handler = GoogleAPIHandler()

    # Read start and destination from config
    config = configparser.ConfigParser()
    config.read('config.ini')
    driver_location = config['Locations']['driver_location']
    origin = config['Locations']['origin']
    destination = config['Locations']['destination']

    # Convert driver_location to tuple of floats
    start_point = tuple(map(float, driver_location.split(',')))

 

    # Fetch route data from Google Distance Matrix API
    route_data = google_api_handler.get_route(origin, destination)
    
    # Get ETA (in minutes)
    eta = google_api_handler.get_eta(origin, destination)
    print(f"Estimated Time of Arrival: {eta:.2f} minutes")

    # Simulate driver's progress (e.g., after 5 minutes)
    elapsed_time = 5  # minutes
    algo_handler = AlgorithmOperationsHandler()
    # Get latitude and longitude for the destination address
    end_point = google_api_handler.get_lat_long(destination)
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
