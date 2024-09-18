import requests
import configparser

class GoogleAPIHandler:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_url = self.config['API']['url']
        self.api_key = self.config['API']['api_key']
    
    def get_route(self, origins, destinations):
        params = {
            'origins': origins,
            'destinations': destinations,
            'key': self.api_key
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")
    
    def get_eta(self, origins, destinations):
        route_data = self.get_route(origins, destinations)
        if route_data['status'] == 'OK':
            duration = route_data['rows'][0]['elements'][0]['duration']['value']  # in seconds
            return duration / 60  # Convert to minutes
        else:
            raise Exception(f"Error in API response: {route_data['status']}")
