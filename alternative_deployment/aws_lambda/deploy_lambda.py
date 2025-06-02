import boto3

lambda_client = boto3.client('lambda')


def create_lambda_function():
    with open('zipped_lambda_code.zip', 'rb') as f:
        zipped_code = f.read()
    
    response = lambda_client.create_function(
                    FunctionName='lambda_function_name', 
                    Runtime='python3.11',
                    Role='arn:aws:iam::XXXXXX:role/lambda-admin-role',
                    Handler='handler.lambda_handler',
                    Code=dict(ZipFile=zipped_code),
                    Timeout=30,
                    MemorySize=1536,
                    Layers=['arn:aws:lambda:eu-west-2:XXXXXX:layer:quant:1']
                    )
        
create_lambda_function()
