from flask import Flask, jsonify, request
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def health_check():
    return "Server is running..."

@app.route("/api/get-location-names")
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    }), 200
    
    return response

@app.route("/api/predict-home-price", methods=["POST"])
def predict_home_price():
    total_sqft = float(request.form["total_sqft"])
    location = request.form["location"]
    bhk = request.form["bhk"]
    bath = request.form["bath"]
    
    response = jsonify({
        "estimated_price" : util.get_estimated_price(location, total_sqft, bhk, bath)
    }), 200
    
    return response
    

if __name__ == "__main__":
    print("Starting flask server....")
    util.load_saved_artifacts()
    app.run()