import logging

import psycopg2
from database import DatabaseAdapter
from psycopg2.extras import execute_values

# Claude A09: İsimlendirilmiş logger
logger = logging.getLogger("currency_etl.postgres_adapter")


class PostgresAdapter(DatabaseAdapter):
    def __init__(self, db_config):
        """Bağlantı bilgilerini dışarıdan (config.py üzerinden) alır."""
        self.db_config = db_config

    def connect(self):
        """Veritabanı bağlantısını kurar."""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            logger.error(f"Veritabanı bağlantı hatası: {e}")
            raise

    def upsert_data(self, df, table_name):
        """
        Claude Ölçeklenebilirlik Çözümü: Idempotency.
        Veriyi insert ederken çakışma (conflict) olursa günceller.
        Böylece DAG tekrar çalıştığında 'UniqueViolation' hatası almazsın.
        """
        conn = self.connect()
        cur = conn.cursor()

        # DataFrame'i liste formatına çeviriyoruz
        values = [tuple(x) for x in df.to_numpy()]
        cols = ",".join(list(df.columns))

        # UPSERT Sorgusu: base_currency ve target_currency üzerinden çakışma kontrolü yapar
        query = f"""
            INSERT INTO {table_name} ({cols})
            VALUES %s
            ON CONFLICT (base_currency, target_currency)
            DO UPDATE SET
                rate = EXCLUDED.rate,
                last_updated = EXCLUDED.last_updated;
        """

        try:
            execute_values(cur, query, values)
            conn.commit()
            logger.info(
                f"'{table_name}' tablosuna {len(df)} satır başarıyla UPSERT edildi."
            )
        except Exception as e:
            conn.rollback()
            logger.error(f"Upsert hatası ({table_name}): {e}")
            raise
        finally:
            cur.close()
            conn.close()

    def log_metadata(self, base_currency, status_code, record_count):
        """
        Claude 'Ölü Şema' Çözümü:
        api_metadata tablosunu her çekim sonrası doldurur.
        """
        conn = self.connect()
        cur = conn.cursor()
        query = """
            INSERT INTO api_metadata (fetch_date, base_currency, status_code, record_count)
            VALUES (CURRENT_TIMESTAMP, %s, %s, %s)
        """
        try:
            cur.execute(query, (base_currency, status_code, record_count))
            conn.commit()
            logger.info("Metadata loglama başarılı.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Metadata loglama hatası: {e}")
        finally:
            cur.close()
            conn.close()
