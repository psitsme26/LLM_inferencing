from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between requests

    @task
    def test_endpoint(self):
        self.client.get("/")
