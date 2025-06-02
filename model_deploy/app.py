from flask import Flask, request, jsonify, Response
import joblib
from marshmallow import Schema, fields, ValidationError
import json
from pyinstrument import Profiler

app = Flask(__name__)


# Load the model when the application starts
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

@app.route('/predict', methods=['POST'])
def predict():
    # Check if profiling is requested
    profile = request.args.get('performance', 'false').lower() == 'true'
    profiler = None
    if profile:
        profiler = Profiler()
        profiler.start()

    try:
        # parse JSON
        data = request.get_json()
        
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
        response = jsonify({'predicted_sales': predicted_sales}), 200

    except ValidationError as err:
        response = jsonify(err.messages), 400
    except Exception as err:
        # Log the error
        app.logger.error(f"Unexpected error: {err}")
        response = jsonify({'error': 'An unexpected error occurred'}), 500
    finally:
        if profile:
            profiler.stop()
            html_output = profiler.output_html()
            return Response(html_output, mimetype='text/html')

    return response

@app.route('/status', methods=['GET'])
def status():
    #check if the API is healthy
    return jsonify({'status': 'Healthy'}), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True) 