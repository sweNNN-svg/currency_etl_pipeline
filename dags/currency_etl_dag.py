from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.convert import convert_json_to_csv as convert_stage

# scripts artık bir paket olduğu için doğrudan temiz importlar
from scripts.main import main as fetch_stage
from scripts.postgres_adapter import PostgresAdapter
from scripts.transform import main as transform_stage
from scripts.utils.config import DB_CONFIG, FINAL_DATA_CSV


def load_stage():
    """
    Claude Ölçeklenebilirlik Çözümü:
    CSV'yi okur ve veritabanına UPSERT (Idempotent) olarak basar.
    """
    # Veriyi Pandas ile okuyoruz (Validasyon için ilk adım)
    df = pd.read_csv(FINAL_DATA_CSV)

    # Adapter'ı başlat ve UPSERT operasyonunu çağır
    adapter = PostgresAdapter(DB_CONFIG)
    adapter.upsert_data(df, table_name="exchange_rates")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # Claude A08: start_date'i daha mantıklı bir geçmişe çekiyoruz
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries": 2,  # Claude: Daha dirençli bir pipeline için retry sayısı artırıldı
    "retry_delay": timedelta(minutes=5),
    # Claude: Task asılı kalmasın diye timeout (Ölçeklenebilirlik maddesi)
    "execution_timeout": timedelta(minutes=10),
}

with DAG(
    "currency_etl_pipeline",
    default_args=default_args,
    description="Professional Currency ETL Pipeline with Upsert & Scalability",
    schedule_interval="@daily",  # Daha standart bir tanım
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
