from locust import HttpUser, task, between, constant
from gevent.pool import Group
num_of_parallel_requests = 10
# class User(HttpUser):
#     wait_time = between(0.05, 0.1)
#     @task(1)
#     def test_api(self):
#         group = Group()
#         # // This will spawn the number of requests needed in parallel
#         for i in range(0, num_of_parallel_requests):
#              group.spawn(lambda:self.client.get(url))
#         # // Once they are ready they are hit in parallel
#         group.join()
#
# import time
# from locust import HttpUser, task, constant
import pandas as pd


class MyUser(HttpUser):
    wait_time = between(0.05, 0.1)  # Wait time for requests
    host = 'http://0.0.0.0:8000'

    @task
    def send_post_request(self):
        group = Group()
        for i in range(0, num_of_parallel_requests):

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
            group.spawn(lambda: self.client.post("/generate/", json=payload, headers=headers))
            #response = self.client.post("/generate/", json=payload, headers=headers)
            # print(f"Response status code: {response.status_code}")
            # res = response.json()
            #
            # with open('api_response_scenario1_new.txt', 'a+') as file:
            #     file.write('---------- \n' + str(res) + '\n ---------------')

            #time.sleep(10)  # Wait for 10 seconds between requests
