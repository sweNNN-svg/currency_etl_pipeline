import logging

import psycopg2
from database import DatabaseAdapter

# create an instance of the logger
logger = logging.getLogger()

# logging set up
log_format = logging.Formatter("%(asctime)-15s %(levelname)-2s %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(log_format)

# add the handler
logger.addHandler(sh)
logger.setLevel(logging.INFO)


class PostgresAdapter(DatabaseAdapter):
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return psycopg2.connect(**self.db_config)

    def load_csv_to_table(self, file_path, table_name, columns):
        conn = self.connect()
        cur = conn.cursor()

        try:
            with open(file_path, "r") as f:
                next(f)  # Başlık satırını atla
                cur.copy_from(
                    f,
                    table_name,  # Değişken oldu
                    sep=",",
                    columns=columns,  # Değişken oldu
                )
            conn.commit()
            logger.info(f"Veri başarıyla {table_name} tablosuna yüklendi.")
        except Exception as e:
            conn.rollback()  # Hata olursa geri al (Best Practice!)
            logger.error(f"Yükleme hatası: {e}")
        finally:
            cur.close()
            conn.close()
