import requests
import polyline
import configparser
import json
import os

class GoogleAPIHandler:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
        self.distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        self.geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.api_key = self.config['API']['api_key']
    
    def get_route(self, origins, destinations):
        # Check if direction.json exists
        if os.path.exists('direction.json'):
            with open('direction.json', 'r') as file:
                route_data = json.load(file)
        else:
            # File does not exist, make API call
            params = {
                'origin': origins,
                'destination': destinations,
                'key': self.api_key
            }
            response = requests.get(self.directions_url, params=params)
            if response.status_code == 200:
                route_data = response.json()
                # Save the response to direction.json
                with open('direction.json', 'w') as file:
                    json.dump(route_data, file, indent=4)
            else:
                raise Exception(f"Error fetching data: {response.status_code}")
        
        # Check if the route data is valid
        if route_data['status'] == 'OK':
            return self.get_polyline_points(route_data)
        else:
            raise Exception(f"Error in route data response: {route_data['status']}")
    
    def get_polyline_points(self, route_data):
        # Extract polyline points from route_data
        steps = route_data['routes'][0]['legs'][0]['steps']
        route_points = []
        for step in steps:
            polyline_points = step['polyline']['points']
            decoded_points = polyline.decode(polyline_points)
            route_points.extend(decoded_points)
        return route_points

    def get_eta(self, origins, destinations):
        params = {
            'origins': origins,
            'destinations': destinations,
            'key': self.api_key
        }
        response = requests.get(self.distance_matrix_url, params=params)
        if response.status_code == 200:
            route_data = response.json()
            if route_data['status'] == 'OK':
                duration = route_data['rows'][0]['elements'][0]['duration']['value']  # in seconds
                return duration / 60  # Convert to minutes
            else:
                raise Exception(f"Error in API response: {route_data['status']}")
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def get_lat_long(self, address):
        params = {
            'address': address,
            'key': self.api_key
        }
        response = requests.get(self.geocode_url, params=params)
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'OK':
                location = result['results'][0]['geometry']['location']
                return (location['lat'], location['lng'])
            else:
                raise Exception(f"Geocoding API error: {result['status']}")
        else:
            raise Exception(f"Error fetching geocode data: {response.status_code}")