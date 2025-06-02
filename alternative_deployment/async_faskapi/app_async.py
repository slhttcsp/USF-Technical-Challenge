from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import joblib
from datetime import date

app = FastAPI()

# Load the model when the application starts
model = joblib.load('model.joblib')

# Define a Pydantic model for input validation
class PredictionInput(BaseModel):
    store: int
    item: int
    date: date

def predict_sales(input_data):
    # Use the model to make a prediction
    predicted_sales = model.predict(input_data)
    # Return the prediction
    return predicted_sales[0]

@app.post('/predict')
async def predict(input_data: PredictionInput):
    try:
        store = input_data.store
        item = input_data.item
        date = input_data.date
        
        # Extract year, month, day from date
        year = date.year
        month = date.month
        day = date.day
        
        # Prepare input data in the required format
        input_data = [[store, item, month, day, year]]
        
        # Get prediction
        predicted_sales = predict_sales(input_data)
        
        # Return prediction with a 200 OK status
        return JSONResponse(content={'predicted_sales': predicted_sales}, status_code=200)

    except Exception as err:
        # Log the error
        app.logger.error(f"Unexpected error: {err}")
        return JSONResponse(
            content={'error': 'An unexpected error occurred'},
            status_code=500
        )

@app.get('/status')
async def status():
    # Check if the API is healthy
    return JSONResponse(content={'status': 'Healthy'}, status_code=200)

if __name__ == '__main__':
    app.run(debug=True) 