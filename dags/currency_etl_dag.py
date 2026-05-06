import logging
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.convert import convert_json_to_csv as convert_stage

# Mutlak importlar (K-4 ve O-1 uyumluluğu için)
from scripts.main import main as fetch_stage
from scripts.postgres_adapter import PostgresAdapter
from scripts.transform import main as transform_stage
from scripts.utils.config import DB_CONFIG, DEFAULT_BASE_CURRENCY, FINAL_DATA_CSV

logger = logging.getLogger("airflow.task")


def load_stage():
    """
    Y-1 Çözümü: Veriyi yükler ve başarı durumunu metadata tablosuna kaydeder.
    """
    try:
        # Veriyi oku
        df = pd.read_csv(FINAL_DATA_CSV)
        adapter = PostgresAdapter(DB_CONFIG)

        # 1. Ana veriyi UPSERT et (K-2 uyumlu)
        adapter.upsert_data(df, table_name="exchange_rates")

        # 2. Y-1: Metadata kaydını oluştur (Audit Log)
        # API her zaman 200 dönerse buraya gelir, kayıt sayısı df uzunluğudur.
        adapter.log_metadata(
            base_currency=DEFAULT_BASE_CURRENCY, status_code=200, record_count=len(df)
        )

        logger.info(f"Load aşaması başarıyla tamamlandı. {len(df)} kayıt işlendi.")

    except Exception as e:
        logger.error(f"Load aşamasında kritik hata: {e}")
        raise


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # A08: start_date'i güncel tutuyoruz
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "retries": 3,  # Claude: Daha dirençli bir yapı için retry artırıldı
    "retry_delay": timedelta(minutes=5),
    # Ölçeklenebilirlik: Task asılı kalmasın diye timeout
    "execution_timeout": timedelta(minutes=15),
}

with DAG(
    "currency_etl_pipeline_v2",
    default_args=default_args,
    description="Professional ETL with Metadata Logging & Celery Consistency",
    schedule_interval="@daily",
    catchup=False,
    tags=["production", "currency"],
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

    # Pipeline Akışı
    fetch_task >> convert_task >> transform_task >> load_task
