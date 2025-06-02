from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def predict(self):
        # Define the payload for the POST request
        payload = {
            "store": 1,
            "item": 1,
            "date": "2013-01-01"
        }
        # Send a POST request to the /predict endpoint
        self.client.post("/predict", json=payload)

    

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Simulate a wait time between requests 