import logging
import os

import requests
from utils.config import API_KEY, DEFAULT_BASE_CURRENCY, RAW_DATA_JSON

# GÜNCELLEME: Root logger yerine isimlendirilmiş logger (A09)
logger = logging.getLogger("currency_etl.main")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def fetch_currency_data(api_key, base_currency):
    """API'den döviz kurlarını çeker."""
    # GÜNCELLEME: URL'i f-string ile daha güvenli ve okunaklı hale getirdik
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"

    try:
        # GÜNCELLEME: Timeout eklendi (A02). 10 saniye içinde cevap gelmezse hata verir.
        response = requests.get(url, timeout=10)

        # GÜNCELLEME: 200 OK dışındaki hataları yakalamak için (A09)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        logger.error("API isteği zaman aşımına uğradı (Timeout).")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP Hatası oluştu: {err}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Beklenmedik bir bağlantı hatası oluştu: {e}")

    return None


def main():
    if not API_KEY:
        logger.error("API Key bulunamadı! Lütfen .env dosyasını kontrol edin.")
        return

    logger.info(f"{DEFAULT_BASE_CURRENCY} için veri çekme işlemi başlıyor...")
    data = fetch_currency_data(API_KEY, DEFAULT_BASE_CURRENCY)

    if data:
        # Veriyi kaydetme ve diğer işlemler...
        logger.info("Veri başarıyla çekildi ve işlenmeye hazır.")
