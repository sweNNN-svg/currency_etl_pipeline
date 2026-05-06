import os
from pathlib import Path

from dotenv import load_dotenv

# .env dosyasındaki verileri yükle
load_dotenv()

# --- Dizin Yapılandırması (K-4 ve O-4 Çözümü) ---
# Bu dosyanın bulunduğu yer: scripts/utils/config.py
# 1. .parent (utils) -> 2. .parent (scripts) -> 3. .parent (root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Veri dosyaları için merkezi bir klasör (Container'lar arası volume paylaşımı için)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # Klasör yoksa otomatik oluştur

# --- API Bilgileri ---
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
API_BASE_URL = "https://v6.exchangerate-api.com/v6"

# --- Veritabanı Bilgileri ---
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
}

# --- Dosya Yolları (Mutlak Yol Yapısı) ---
# Artık script nereden çalışırsa çalışsın dosyalar hep /data altında bulunur.
RAW_DATA_JSON = str(DATA_DIR / "currency.json")
RAW_DATA_CSV = str(DATA_DIR / "currency_raw.csv")
FINAL_DATA_CSV = str(DATA_DIR / "currency_final.csv")

# --- İş Kuralları ---
DEFAULT_BASE_CURRENCY = "TRY"
HTTP_TIMEOUT = 10  # Claude (7) bulgusunu merkezi hale getirdik
