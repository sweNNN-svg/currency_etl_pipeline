import logging

import psycopg2
from scripts.database import DatabaseAdapter
from psycopg2 import sql
from psycopg2.extras import execute_values

# Claude A09: İsimlendirilmiş logger
logger = logging.getLogger("currency_etl.postgres_adapter")


class PostgresAdapter(DatabaseAdapter):
    def __init__(self, db_config):
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
        K-2: Constraint Mismatch Çözümü (last_updated eklendi)
        K-3: SQL Injection Çözümü (psycopg2.sql kullanıldı)
        """
        conn = self.connect()
        cur = conn.cursor()

        # DataFrame değerlerini listeye çeviriyoruz
        values = [tuple(x) for x in df.to_numpy()]

        # K-3: Kolon isimlerini ve tablo ismini sql.Identifier ile sarmalayarak
        # SQL Injection riskini tamamen ortadan kaldırıyoruz.
        columns = [sql.Identifier(col) for col in df.columns]

        # K-2: ON CONFLICT kısmını init.sql'deki UNIQUE constraint ile eşliyoruz.
        # init.sql'de UNIQUE(base_currency, target_currency, last_updated) vardı.
        query = sql.SQL("""
            INSERT INTO {table} ({cols})
            VALUES %s
            ON CONFLICT (base_currency, target_currency, last_updated)
            DO UPDATE SET
                rate = EXCLUDED.rate;
        """).format(table=sql.Identifier(table_name), cols=sql.SQL(",").join(columns))

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
        """api_metadata tablosunu doldurur."""
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
