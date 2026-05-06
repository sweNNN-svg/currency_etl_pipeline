import os

from dotenv import load_dotenv

# .env dosyasındaki verileri yükle
load_dotenv()

# API Bilgileri
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

# Veritabanı Bilgileri
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dosya Yolları (Artık sadece buradan değişecek)
RAW_DATA_JSON = "currency.json"
RAW_DATA_CSV = "currency.csv"
PROCESSED_DATA_CSV = "currency-v2.csv"
FINAL_DATA_CSV = "currency-v3.csv"

# API Ayarları
DEFAULT_BASE_CURRENCY = "TRY"
