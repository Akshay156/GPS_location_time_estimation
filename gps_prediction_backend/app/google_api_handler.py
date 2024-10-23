import requests
import json
import configparser
import polyline
import os

class GoogleAPIHandler:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = None if self.config['API'].get('api_key', None) == 'None' else  self.config['API'].get('api_key')
        self.directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
        self.distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        self.example_response_path = os.path.join('data', 'sample_responses', 'example_response.json')

    def call_api(self, url, params):
        if self.api_key is None:
            print("API key is not provided, using example response.")
            return self.load_example_response()
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from {url}: {response.status_code}")

    def load_example_response(self):
        with open(self.example_response_path, 'r') as file:
            return json.load(file)

    def get_directions(self, origin, destination):
        params = {
            'origin': origin,
            'destination': destination,
            'key': self.api_key
        }
        return self.call_api(self.directions_url, params)

    def get_distance_matrix(self, origins, destinations):
        params = {
            'origins': origins,
            'destinations': destinations,
            'key': self.api_key
        }
        return self.call_api(self.distance_matrix_url, params)

    def get_polyline_points(self, route_data):
        polyline_points = route_data['routes'][0]['legs'][0]['steps'][0]['polyline']['points']
        print(f"Polyline points: {polyline_points}")  # Debugging line
        decoded_points = polyline.decode(polyline_points)
        return decoded_points
