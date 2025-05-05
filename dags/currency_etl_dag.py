import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.transform import main as transform_data
from scripts.main import fetch_currency_data
from scripts.convert import convert_json_to_csv
from scripts.load import load_data_to_postgres
import pendulum
from datetime import datetime, timedelta


default_args = {
    'owner': 'haci',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 5, 1, 0, 30, 0, tzinfo=pendulum.timezone("Europe/Istanbul")),
}

with DAG(
    dag_id='currency_etl',
    default_args=default_args,
    schedule_interval="0 * * * *",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="fetch_currency_data",
        python_callable=fetch_currency_data
    )

    t2 = PythonOperator(
        task_id="convert_json_to_csv",
        python_callable=convert_json_to_csv
    )

    t3 = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    t4 = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_data_to_postgres
    )

    t1 >> t2 >> t3 >> t4
