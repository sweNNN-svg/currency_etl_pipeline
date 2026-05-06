import json
import logging
import sys
from pathlib import Path

# O-1 Çözümü: Script'in ana dizini sys.path'e eklenerek import hataları önlenir
current_dir = Path(__file__).resolve().parent
if str(current_dir.parent) not in sys.path:
    sys.path.append(str(current_dir.parent))

import requests

from scripts.utils.config import (
    API_BASE_URL,
    API_KEY,
    DEFAULT_BASE_CURRENCY,
    HTTP_TIMEOUT,
    RAW_DATA_JSON,
)

# A09: İsimlendirilmiş logger
logger = logging.getLogger("currency_etl.main")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def fetch_currency_data(api_key, base_currency):
    """API'den döviz kurlarını çeker."""
    # URL yapısı config'den gelen base_url ile daha profesyonel hale getirildi
    url = f"{API_BASE_URL}/{api_key}/latest/{base_currency}"

    try:
        # A02: Timeout config üzerinden yönetiliyor
        response = requests.get(url, timeout=HTTP_TIMEOUT)

        # A09: HTTP hatalarını (4xx, 5xx) yakalamak için
        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        logger.error("API isteği zaman aşımına uğradı.")
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP Hatası: {err}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Bağlantı hatası: {e}")

    return None


def main():
    if not API_KEY:
        logger.error("API Key bulunamadı! .env dosyasını kontrol edin.")
        return False

    logger.info(f"{DEFAULT_BASE_CURRENCY} için veri çekme işlemi başlıyor...")
    data = fetch_currency_data(API_KEY, DEFAULT_BASE_CURRENCY)

    if data:
        # K-1 Çözümü: Veri gerçekten diske yazılıyor
        try:
            with open(RAW_DATA_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            logger.info(
                f"Veri başarıyla çekildi ve {RAW_DATA_JSON} dosyasına kaydedildi."
            )
            return True
        except IOError as e:
            logger.error(f"Dosya yazma hatası: {e}")
            return False

    return False


if __name__ == "__main__":
    main()
