import requests
import json
import configparser
import polyline  # Ensure you have installed the polyline library using pip

class GoogleAPIHandler:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config['API']['api_key']
        
        # Define API URLs
        self.directions_url = 'https://maps.googleapis.com/maps/api/directions/json'
        self.distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        self.geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.maps_javascript_url = 'https://maps.googleapis.com/maps/api/js'
        self.roads_url = 'https://maps.googleapis.com/maps/api/roads/'
        self.routes_url = 'https://maps.googleapis.com/maps/api/route/json'
        self.route_optimization_url = 'https://maps.googleapis.com/maps/api/optimize/json'

    def save_to_file(self, filename, data, bytes=False):
        with open(filename, 'w' if not bytes else 'wb') as file:
            if bytes:
                file.write(data)
            else:    
                json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")

    def get_content(self, url, params, filename):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.content
            self.save_to_file(filename, data, bytes=True)
            return data
        else:
            raise Exception(f"Error fetching data from {url}: {response.status_code}")
        
    def call_api(self, url, params, filename):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.save_to_file(filename, data)
            return data
        else:
            raise Exception(f"Error fetching data from {url}: {response.status_code}")

    def get_directions(self, origin, destination):
        params = {
            'origin': origin,
            'destination': destination,
            'key': self.api_key
        }
        return self.call_api(self.directions_url, params, 'directions.json')

    def get_distance_matrix(self, origins, destinations):
        params = {
            'origins': origins,
            'destinations': destinations,
            'key': self.api_key
        }
        return self.call_api(self.distance_matrix_url, params, 'distance_matrix.json')

    def get_geocode(self, address):
        params = {
            'address': address,
            'key': self.api_key
        }
        return self.call_api(self.geocode_url, params, 'geocode.json')

    def get_maps_javascript(self):
        params = {
            'key': self.api_key
        }
        return self.get_content(self.maps_javascript_url, params, 'maps_javascript.json')

    def get_roads(self, path):
        params = {
            'path': path,
            'key': self.api_key
        }
        return self.get_content(self.roads_url, params, 'roads.json')

    def get_routes(self, origin, destination):
        params = {
            'origin': origin,
            'destination': destination,
            'key': self.api_key
        }
        return self.get_content(self.routes_url, params, 'routes.json')

    def get_route_optimization(self, waypoints):
        params = {
            'waypoints': waypoints,
            'key': self.api_key
        }
        return self.call_api(self.route_optimization_url, params, 'route_optimization.json')

    def get_polyline_points(self, route_data):
        steps = route_data['routes'][0]['legs'][0]['steps']
        route_points = []
        
        for step in steps:
            polyline_points = step['polyline']['points']
            decoded_points = polyline.decode(polyline_points)
            route_points.extend(decoded_points)
        
        self.save_to_file('polyline_points.json', route_points)
        return route_points

    def draw_polyline(self, polyline_points):
        # To draw polyline, normally you would use a map visualization library.
        # For now, we'll just save the polyline points to a JSON file.
        self.save_to_file('polyline_points.json', polyline_points)

    def get_time_between_points(self, origin, destination):
        params = {
            'origins': origin,
            'destinations': destination,
            'key': self.api_key
        }
        data = self.call_api(self.distance_matrix_url, params, 'distance_matrix.json')
        if data['status'] == 'OK':
            duration = data['rows'][0]['elements'][0]['duration']['value']  # in seconds
            return duration
        else:
            raise Exception(f"Error in API response: {data['status']}")

def main():
    handler = GoogleAPIHandler()

    # Example usage - replace with actual values
    directions_data = handler.get_directions('HSR Layout, Bangalore, Karnataka', 'ITI Layout, Bangalore, Karnataka')
    handler.get_polyline_points(directions_data)
    # distance_matrix_data = handler.get_distance_matrix('HSR Layout, Bangalore, Karnataka', 'ITI Layout, Bangalore, Karnataka')
    # handler.get_geocode('HSR Layout, Bangalore, Karnataka')
    # handler.get_maps_javascript()
                    # handler.get_roads('12.934533,77.626579|12.934534,77.626580')
                    # handler.get_routes('HSR Layout, Bangalore, Karnataka', 'ITI Layout, Bangalore, Karnataka')
    # handler.get_route_optimization('waypoint1|waypoint2|waypoint3')

    # Time taken between points
    # time_taken = handler.get_time_between_points('HSR Layout, Bangalore, Karnataka', 'ITI Layout, Bangalore, Karnataka')
    # print(f"Time taken: {time_taken / 60:.2f} minutes")

if __name__ == '__main__':
    main()
