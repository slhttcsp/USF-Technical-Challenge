import joblib
import os
import json
import lightgbm as lgb
from marshmallow import Schema, fields, ValidationError

# Define validation schema
class PredictionInputSchema(Schema):
    store = fields.Integer(required=True)
    item = fields.Integer(required=True) 
    date = fields.Date(required=True, format='%Y-%m-%d')

# Initialize schema
input_schema = PredictionInputSchema()

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, 'model.joblib'))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        # Parse JSON
        data = json.loads(request_body)
        
        # Validate input
        try:
            data = input_schema.load(data)
        except ValidationError as err:
            raise ValueError(f"Invalid input data: {err.messages}")
            
        # Extract features
        store = data['store']
        item = data['item']
        date = data['date']
        
        # Extract year, month, day from date
        year = date.year
        month = date.month
        day = date.day
        
        # Prepare input data in required format
        input_data = [[store, item, month, day, year]]
        
        return input_data
        
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    try:
        prediction = model.predict(input_data)
        return prediction
    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")

def output_fn(prediction, content_type):
    try:
        return json.dumps({'predicted_sales': prediction.tolist()})
    except Exception as e:
        raise ValueError(f"Failed to serialize prediction: {str(e)}")