# Bangalore House Price Prediction

A machine learning web application that predicts house prices in Bangalore based on location, area, number of bedrooms, and bathrooms.

## Project Overview

This project combines machine learning with a web interface to provide real-time house price predictions. The application uses a trained regression model to estimate property values based on multiple input parameters.

## Features

- Real-time house price prediction
- Location-based valuation
- Web-based user interface
- RESTful API endpoints
- CORS-enabled for cross-origin requests

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript (Vanilla)

### Backend

- Python 3
- Flask
- Flask-CORS
- scikit-learn (for ML model)
- pandas
- numpy

### Data Science

- Jupyter Notebook
- pandas
- scikit-learn
- matplotlib
- scipy

## Project Structure

```
bhk/
├── client/
│   ├── index.html          # Frontend UI
│   ├── app.js              # Client-side logic
│   └── app.css             # Styling
├── server/
│   ├── app.py              # Flask application
│   ├── requirements.txt     # Backend dependencies
│   ├── util/
│   │   └── util.py         # Utility functions
│   └── artifacts/
│       └── columns.json     # Model metadata
├── model/
│   ├── bhp.ipynb           # Model training notebook
│   ├── requirements.txt     # Data science dependencies
│   └── csv/
│       └── bengaluru_house_prices.csv  # Training dataset
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Backend Setup

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

The frontend is a static web application and requires no installation. Open `client/index.html` in a web browser.

## Usage

### Running the Server

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Start the Flask server:

   ```bash
   python app.py
   ```

3. The server will run on `http://localhost:5000`

### Accessing the Application

1. Open `client/index.html` in a web browser
2. Enter the following details:
   - Area in square feet
   - Number of bedrooms
   - Number of bathrooms
   - Property location
3. Click predict to get the estimated price

## API Endpoints

### GET `/api/get-location-names`

Returns a list of available locations for prediction.

**Response:**

```json
{
  "locations": ["Location1", "Location2", ...]
}
```

### POST `/api/predict-home-price`

Predicts house price based on input parameters.

**Parameters:**

- `total_sqft`: Area in square feet (float)
- `location`: Property location (string)
- `bhk`: Number of bedrooms (integer)
- `bath`: Number of bathrooms (integer)

**Response:**

```json
{
  "estimated_price": 5000000
}
```

## Model Training

The machine learning model is trained using the data in `model/bhp.ipynb`. The training process includes:

- Data loading and preprocessing
- Feature engineering
- Model training using scikit-learn
- Model serialization for inference

To retrain the model:

1. Navigate to the model directory
2. Open `bhp.ipynb` in Jupyter Notebook
3. Run all cells to train and save the model

## Dependencies

### Backend Requirements

See `server/requirements.txt` for detailed versions.

### Model Requirements

See `model/requirements.txt` for data science libraries.

## Configuration

The application uses the following configuration:

- Model artifacts stored in `server/artifacts/`
- Location metadata stored in `columns.json`
- CORS enabled for all routes
