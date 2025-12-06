import json
import pickle
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

# Get the directory where this file is located
__current_dir = os.path.dirname(os.path.abspath(__file__))
# Parent directory (server/)
__server_dir = os.path.dirname(__current_dir)
# Artifacts directory
__artifacts_dir = os.path.join(__server_dir, "artifacts")

def _ensure_artifacts_loaded() -> None:
    if __model is None or __data_columns is None:
        raise RuntimeError("Artifacts not loaded. Call load_saved_artifacts first.")

def get_location_names():
    return __locations or []

def get_estimated_price(location, sqft, bhk, bath):
    _ensure_artifacts_loaded()

    try:
        sqft_val = float(sqft)
        bhk_val = float(bhk)
        bath_val = float(bath)
    except (TypeError, ValueError) as exc:
        raise ValueError("sqft, bhk, and bath must be numeric.") from exc

    safe_location = (location or "").strip().lower()
    loc_index = __data_columns.index(safe_location) if safe_location in __data_columns else -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft_val
    x[1] = bath_val
    x[2] = bhk_val

    if loc_index >= 0:
        x[loc_index] = 1

    try:
        prediction = __model.predict([x])[0]
    except Exception as exc:
        raise RuntimeError(f"Model prediction failed: {exc}") from exc

    return round(prediction, 2)

def load_saved_artifacts():
    print("Loading artifacts...")
    global __locations
    global __data_columns
    global __model

    columns_path = os.path.join(__artifacts_dir, "columns.json")
    model_path = os.path.join(__artifacts_dir, "bhp_model.pickle")

    try:
        with open(columns_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            __data_columns = data.get("data_columns", [])
            __locations = __data_columns[3:]
            print(f"Loaded {len(__locations)} locations")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"columns.json not found at {columns_path}") from exc
    except (KeyError, json.JSONDecodeError) as exc:
        raise RuntimeError("Invalid columns.json format.") from exc
    except Exception as exc:
        raise

    try:
        with open(model_path, "rb") as f:
            __model = pickle.load(f)
            print("Model loaded successfully")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"bhp_model.pickle not found at {model_path}") from exc
    except Exception as exc:
        raise RuntimeError(f"Loading model failed: {exc}") from exc

    print("Loading the artifacts is done.")