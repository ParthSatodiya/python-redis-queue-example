import os
import redis
import requests
from redis import Redis
import rq

redis_conn_1 = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=1)

def add_dog_fact():
    resp = requests.get("https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1")
    if not resp.ok:
        raise Exception(resp.text)

    # resp_data
    # [
    #     {
    #         "fact": "Many foot disorders in dogs are caused by long toenails."
    #     }
    # ]
    redis_conn_1.lpush("dog_facts", resp.json()[0]["fact"])

def get_dog_facts_count():
    print("Total dog facts: ", redis_conn_1.llen("dog_facts"))

def add_cat_fact():
    resp = requests.get("https://catfact.ninja/facts?limit=1")
    if not resp.ok:
        raise Exception(resp.text)

    # resp_data
    # { 
    #     current_page": 1,
    #     "data": [
    #         {
    #         "fact": "A cat almost never meows at another cat, mostly just humans. Cats typically will spit, purr, and hiss at other cats.",
    #         "length": 116
    #         }
    #     ],
    #     "first_page_url": "https:\/\/catfact.ninja\/facts?page=1",
    #     ...
    # }

    redis_conn_1.lpush("cat_facts", resp.json()["data"][0]["fact"])

def get_cat_facts_count():
    print("Total caat facts: ", redis_conn_1.llen("cat_facts"))
