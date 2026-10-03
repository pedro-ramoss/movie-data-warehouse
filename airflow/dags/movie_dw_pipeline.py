import os
import subprocess
from datetime import datetime, timezone
from airflow.sdk import dag, task

PROJECT_ROOT = "/home/pedro/movie-data-warehouse"
PYTHON = f"{PROJECT_ROOT}/.venv/bin/python"
DBT = f"{PROJECT_ROOT}/.venv/bin/dbt"

@dag(
    dag_id="movie_dw_pipeline",
    schedule=None,
    start_date=datetime(2026, 10, 3, tzinfo=timezone.utc),
    catchup=False,
    tags=["movie_dw"]
)
def movie_dw_pipeline():

    @task
    def extract_tmdb():
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        subprocess.run([PYTHON, "-m", "movie_dw.extract"], cwd=PROJECT_ROOT, env=env, check=True)

    @task
    def load_staging():
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        subprocess.run([PYTHON, "-m", "movie_dw.load_staging"], cwd=PROJECT_ROOT, env=env, check=True)

    @task
    def dbt_run():
        subprocess.run([DBT, "run"], cwd=f"{PROJECT_ROOT}/movie_dw_dbt", check=True)

    @task
    def dbt_test():
        subprocess.run([DBT, "test"], cwd=f"{PROJECT_ROOT}/movie_dw_dbt", check=True)

    extract = extract_tmdb()
    staging = load_staging()
    run = dbt_run()
    test = dbt_test()

    extract >> staging >> run >> test

movie_dw_pipeline()

