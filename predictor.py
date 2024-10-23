
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google_api_handler import GoogleAPIHandler
import polyline
import math

app = FastAPI()
handler = GoogleAPIHandler()

class Location(BaseModel):
    from_lat: float
    from_lng: float
    to_lat: float
    to_lng: float

class PredictionInput(BaseModel):
    elapsed_time: int  
    polyline: str      

@app.post("/get_route_data/")
async def get_route_data(location: Location):
    try:
        origin = f"{location.from_lat},{location.from_lng}"
        destination = f"{location.to_lat},{location.to_lng}"
        
        
        directions_data = handler.get_directions(origin, destination)
        
        
        travel_time = directions_data['routes'][0]['legs'][0]['duration']['value']  
        polyline_points = directions_data['routes'][0]['overview_polyline']['points']
        
        
        decoded_points = polyline.decode(polyline_points)

        return {
            "travel_time": travel_time,
            "polyline": decoded_points
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/")
async def predict(prediction_input: PredictionInput):
    average_speed = 40  
    distance_per_second = average_speed / 3600  
    distance_traveled = distance_per_second * prediction_input.elapsed_time  

    polyline_points = polyline.decode(prediction_input.polyline)
    
    total_distance = 0.0
    for i in range(len(polyline_points) - 1):
        segment_start = polyline_points[i]
        segment_end = polyline_points[i + 1]
        segment_distance = haversine(segment_start, segment_end)
        
        if total_distance + segment_distance >= distance_traveled:
            
            remaining_distance = distance_traveled - total_distance
            ratio = remaining_distance / segment_distance
            
            new_lat = segment_start[0] + ratio * (segment_end[0] - segment_start[0])
            new_lng = segment_start[1] + ratio * (segment_end[1] - segment_start[1])
            
            return {
                "predicted_location": (new_lat, new_lng),
                "distance_traveled": distance_traveled
            }
        
        total_distance += segment_distance

    
    return {
        "predicted_location": polyline_points[-1],
        "distance_traveled": total_distance
    }

def haversine(coord1, coord2):
    R = 6371  
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c  
