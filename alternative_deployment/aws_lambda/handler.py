import joblib
from marshmallow import Schema, fields, ValidationError
import json

# Load the model when the lambda function starts
model = joblib.load('model.joblib')

# Define a Marshmallow schema for input validation
class PredictionInputSchema(Schema):
    store = fields.Integer(required=True)
    item = fields.Integer(required=True)
    date = fields.Date(required=True, format='%Y-%m-%d')

# Initialize the schema
input_schema = PredictionInputSchema()

def predict_sales(input_data):
    # Use the model to make a prediction
    predicted_sales = model.predict(input_data)
    # Return the prediction
    return predicted_sales[0]

def lambda_handler(event, context):
    try:
        # parse JSON
        data = json.loads(event['body'])
   
        # Validate input
        data = input_schema.load(data)
        
        store = data['store']
        item = data['item']
        date = data['date']
        
        # Extract year, month, day from date
        year = date.year
        month = date.month
        day = date.day
        
        # Prepare input data in the required format
        input_data = [[store, item, month, day, year]]
        
        # Get prediction
        predicted_sales = predict_sales(input_data)
        
        # Return prediction with a 200 OK status
        return {
            'statusCode': 200,
            'body': json.dumps({'predicted_sales': predicted_sales})
        }

    except ValidationError as err:
        return {
            'statusCode': 400,
            'body': json.dumps(err.messages)
        }
    except Exception as err:
        # Log the error
        print(f"Unexpected error: {err}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An unexpected error occurred'})
        } 