import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dosya Yolları (Artık sadece buradan değişecek)
RAW_DATA_JSON = "currency.json"
RAW_DATA_CSV = "currency.csv"
PROCESSED_DATA_CSV = "currency-v2.csv"
FINAL_DATA_CSV = "currency-v3.csv"

# API Ayarları
DEFAULT_BASE_CURRENCY = "TRY"
