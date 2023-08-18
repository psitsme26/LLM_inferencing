from locust import HttpUser, task, constant, between
import pandas as pd


class MyUser(HttpUser):
    wait_time = between(1, 1)  # Wait time for requests
    host = 'http://0.0.0.0:8000'

    @task
    def send_post_request(self):
        data = pd.read_csv('test.csv')
        sub_data = data.head(1000)
        sample = sub_data.sample(n=1)
        article_id = sample[['id']].values[0][0]
        ground_truth = sample[['highlights']].values[0][0]
        prompt = sample[['article']].values[0][0]
        max_length = 1024
        model_name = 'BART'
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

        payload = {
            "article_id": article_id,
            "prompt": prompt,
            "max_length": max_length,
            "model_name": model_name,
            "ground_truth": ground_truth
        }

        response = self.client.post("/generate/", json=payload, headers=headers)
        #print("Response:", response.json())
        print(f"Response status code: {response.status_code}")
        res = response.json()

        with open('api_response_scenario1.txt', 'a+') as file:
            file.write('---------- \n' + str(res) + '\n ---------------')

