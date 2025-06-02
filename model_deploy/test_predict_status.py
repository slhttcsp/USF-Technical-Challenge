import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_success(client):
    """
    Test the /predict endpoint with valid input data to ensure it returns
    a 200 status code and includes 'predicted_sales' in the response JSON.
    """
    response = client.post('/predict', json={
        'store': 1,
        'item': 1,
        'date': '2023-01-01'
    })
    assert response.status_code == 200
    assert 'predicted_sales' in response.get_json()


def test_predict_validation_error(client):
    """
    Test the /predict endpoint with invalid data types to ensure it returns
    a 400 status code.
    """
    response = client.post('/predict', json={
        'store': 'not-an-integer',
        'item': 1,
        'date': '2023-01-01'
    })
    assert response.status_code == 400

def test_predict_missing_field(client):
    """
    Test the /predict endpoint with missing fields to ensure it returns
    a 400 status code and an appropriate error message indicating the missing field.
    """
    response = client.post('/predict', json={
        'store': 1,
        'date': '2023-01-01'
    })
    assert response.status_code == 400
    assert 'item' in response.get_json()

def test_predict_unexpected_error(client, monkeypatch):
    """
    Test the /predict endpoint by mocking the predict functino 
    to simulate an unexpected error, ensuring it returns a 500 
    status code and an appropriate error message.
    """
    def mock_predict(input_data):
        raise Exception("Unexpected error")
    
    monkeypatch.setattr('app.predict_sales', mock_predict)
    
    response = client.post('/predict', json={
        'store': 1,
        'item': 1,
        'date': '2023-01-01'
    })
    assert response.status_code == 500
    assert response.get_json() == {'error': 'An unexpected error occurred'}
    
def test_status(client):
    """
    Test the /status endpoint to ensure it returns a 200 status code
    and the expected JSON response indicating the service is healthy.
    """
    response = client.get('/status')
    # Assert that the response status code is 200
    assert response.status_code == 200
    # Assert that the response JSON contains the expected status message
    assert response.get_json() == {'status': 'Healthy'}
    
#run above tests  
if __name__ == '__main__':
    pytest.main(['-v'])