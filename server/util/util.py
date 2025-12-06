import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None


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

    try:
        with open("./artifacts/columns.json", "r", encoding="utf-8") as f:
            __data_columns = json.load(f)["data_columns"]
            __locations = __data_columns[3:]
    except FileNotFoundError as exc:
        raise FileNotFoundError("columns.json not found at ./artifacts/columns.json") from exc
    except (KeyError, json.JSONDecodeError) as exc:
        raise RuntimeError("Invalid columns.json format.") from exc

    try:
        with open("./artifacts/bhp_model.pickle", "rb") as f:
            __model = pickle.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError("bhp_model.pickle not found at ./artifacts/bhp_model.pickle") from exc
    except Exception as exc:
        raise RuntimeError(f"Loading model failed: {exc}") from exc

    print("Loading the artifacts is done.")