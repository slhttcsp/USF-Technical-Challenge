import sagemaker
from sagemaker.model import Model
from sagemaker import get_execution_role
import logging

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()

# Get the execution role
role = get_execution_role()

# model path in S3
model_s3_path = 's3://bucket-name/model/model.joblib'

# Create a SageMaker Model
model = Model(
    model_data=model_s3_path,
    role=role,
    entry_point='inference.py',  
    image_uri='docker image',  
    sagemaker_session=sagemaker_session
)

def deploy_model():
    try:
        # Deploy the model to an endpoint
        predictor = model.deploy(
            instance_type='ml.m5.large',
            endpoint_name='sales-prediction-endpoint'
        )

        print(f"Model deployed at endpoint: {predictor.endpoint_name}")

        # Example of invoking the endpoint
        import boto3
        import json

        # Initialize SageMaker runtime client
        runtime = boto3.client('sagemaker-runtime')

        #  input data
        sample_data = {
            'store': 1,
            'item': 1,
            'date': '2013-01-01'
        }

        # Convert data to JSON string
        payload = json.dumps(sample_data)

        # Invoke endpoint
        response = runtime.invoke_endpoint(
            EndpointName='sales-prediction-endpoint',
            ContentType='application/json',
            Body=payload
        )

        # Parse response
        result = json.loads(response['Body'].read().decode())
        print(f"Predicted sales: {result['predicted_sales']}")
    except Exception as e:
        logging.error(f"Failed to deploy model: {e}")
        raise
