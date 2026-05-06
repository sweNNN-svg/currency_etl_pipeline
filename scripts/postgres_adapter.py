import logging

import psycopg2
from database import DatabaseAdapter

# Logger kurulumu
logger = logging.getLogger(__name__)


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

    def load_csv_to_table(self, file_path, table_name, columns):
        """CSV dosyasındaki verileri belirtilen tabloya yükler."""
        conn = self.connect()
        cur = conn.cursor()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                next(f)  # Header satırını atla
                cur.copy_from(f, table_name, sep=",", columns=columns)
            conn.commit()
            logger.info(f"Veri başarıyla '{table_name}' tablosuna yüklendi.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Tabloya veri yükleme hatası ({table_name}): {e}")
            raise
        finally:
            cur.close()
            conn.close()

    def log_metadata(self, base_currency, status_code, record_count):
        """
        Claude'un bahsettiği 'api_metadata' tablosunu dolduran metod.
        Her API çekiminin güncesini tutar.
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
            logger.info("API çekim metadatası veritabanına kaydedildi.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Metadata loglama hatası: {e}")
        finally:
            cur.close()
            conn.close()
