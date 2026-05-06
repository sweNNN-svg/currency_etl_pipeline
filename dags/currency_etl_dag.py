from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.convert import convert_json_to_csv as convert_stage

# GÜNCELLEME: Artık sys.path.append('...') gibi çirkinliklere gerek yok!
# scripts artık bir paket olduğu için doğrudan import yapıyoruz.
from scripts.main import main as fetch_stage

# GÜNCELLEME: Load aşaması için yeni adapter yapısını kullanıyoruz
from scripts.postgres_adapter import PostgresAdapter
from scripts.transform import main as transform_stage
from scripts.utils.config import DB_CONFIG, RAW_DATA_CSV


def load_stage():
    """Yeni adapter yapısını kullanan profesyonel load aşaması."""
    adapter = PostgresAdapter(DB_CONFIG)
    # Claude'un 'validasyon' uyarısı için kolon isimlerini belirtiyoruz (A03)
    target_columns = ["base_currency", "target_currency", "rate", "last_updated"]

    adapter.load_csv_to_table(
        file_path=RAW_DATA_CSV, table_name="exchange_rates", columns=target_columns
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "currency_etl_pipeline",
    default_args=default_args,
    description="Professional Currency ETL Pipeline with Clean Architecture",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    fetch_task = PythonOperator(
        task_id="fetch_currency_data",
        python_callable=fetch_stage,
    )

    convert_task = PythonOperator(
        task_id="convert_json_to_csv",
        python_callable=convert_stage,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_stage,
    )

    load_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_stage,
    )

    # Akış: Çek -> Çevir -> İşle -> Yükle
    fetch_task >> convert_task >> transform_task >> load_task
