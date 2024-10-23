from flask import Flask, jsonify, request
from .google_api_handler import GoogleAPIHandler
from .prediction_handler import PredictionHandler
from .utils import select_calculation_mode

app = Flask(__name__)
google_api_handler = GoogleAPIHandler()
prediction_handler = PredictionHandler()

@app.route('/start_prediction', methods=['POST'])
def start_prediction():
    data = request.form
    origin = data.get('origin')
    destination = data.get('destination')

    # Get directions from Google API
    route_data = google_api_handler.get_directions(origin, destination)
    
    # Get polyline points from the route data
    polyline_points = google_api_handler.get_polyline_points(route_data)
    
    # Start prediction with the polyline points
    initial_location = prediction_handler.start_prediction(polyline_points)
    
    return jsonify({'initial_location': initial_location})

@app.route('/predict', methods=['GET'])
def predict():
    elapsed_time = request.args.get('elapsed_time', type=int)  # Elapsed time in seconds
    predicted_location = prediction_handler.predict_next_location(elapsed_time)
    
    return jsonify({'predicted_location': predicted_location})

@app.route('/reset', methods=['POST'])
def reset():
    prediction_handler.reset()
    return jsonify({'message': 'Prediction data reset successfully'})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    mode = data.get('mode')
    point_a = data.get('point_a')  # Expected as [lat, long]
    point_b = data.get('point_b')  # Expected as [lat, long]
    time_elapsed = data.get('time_elapsed')  # In hours for speed calculation

    result = select_calculation_mode(mode, point_a, point_b, time_elapsed)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
