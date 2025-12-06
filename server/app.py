from flask import Flask, jsonify, request
from flask_cors import CORS
import util.util as util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load artifacts when the app starts (works with both dev and production servers)
print("Starting flask server....")
try:
    util.load_saved_artifacts()
    print("[SUCCESS] Artifacts loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load artifacts: {e}")
    raise

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
    app.run()