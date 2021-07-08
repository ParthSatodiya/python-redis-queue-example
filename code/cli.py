import os
import redis
from rq import Queue, Worker, job
from redis import Redis
import click
import tasks
from inspect import getmembers, isfunction

redis_conn = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
high_queue = Queue("high", connection=redis_conn)
medium_queue = Queue("medium", connection=redis_conn)
worker = Worker([high_queue, medium_queue], connection=redis_conn, name="mgmt_worker")

@click.group()
def cli():
    pass

@cli.command()
def enqueue(burst):
    click.echo(f"Queueing tasks...")
    high_queue.enqueue(tasks.add_dog_fact, args=(), kwargs={}, ttl=30, timeout="1m", job_id="add_dog_fact", retry=job.Retry(max=2))
    medium_queue.enqueue(tasks.add_cat_fact, args=(), kwargs={}, ttl=30, timeout="30", job_id="add_cat_fact")

@cli.command()
@click.option("--burst", default=False, is_flag=True, show_default=True, help="Start worker in burst mode")
def start_worker(burst):
    click.echo(f"Starting worker...")
    worker.work(burst=burst)

@cli.command()
def current_counts():
    print("Total dog facts: ", tasks.get_dog_facts_count())
    print("Total cat facts: ", tasks.get_cat_facts_count())

@cli.command()
@click.argument("function_name")
def run_one_off(function_name):
    task_functions = dict(getmembers(tasks, isfunction))
    task = task_functions.get(function_name, None)
    if task is None:
        raise Exception(f"No such function named {function_name}")
    task()

if __name__ == "__main__":
    cli()
    
