import folium

class UIHandler:
    def __init__(self, start_point, end_point):
        self.map = folium.Map(location=start_point, zoom_start=12)
        self.start_point = start_point
        self.end_point = end_point

    def draw_route(self):
        # Draw a line between start_point and end_point if needed
        folium.PolyLine([self.start_point, self.end_point], color='blue', weight=2.5, opacity=1).add_to(self.map)

    def add_driver_marker(self, driver_location):
        # Add a marker for the driver's current location
        folium.Marker(location=driver_location, icon=folium.Icon(color='green')).add_to(self.map)

    def display_map(self, map_name='route_map.html'):
        self.map.save(map_name)
        print(f"Map saved as {map_name}")
