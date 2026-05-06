import json

import requests


def fetch_currency_data(api_key, base_currency="USD"):
    """API'den döviz verisini çeker."""
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_data_to_file(data, file_path):
    """Gelen veriyi belirtilen dosya yoluna kaydeder."""
    # BURASI DÜZELDİ: Sabit isim yerine 'file_path' değişkenini kullanıyoruz.
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)


def main():
    # Bu bilgileri ileride bir .env dosyasından okumak daha pro-racon olur.
    api_key = "YOUR-API-KEY"
    currency_to_fetch = "TRY"

    # Dosya ismini de dinamik yaptık
    target_file = f"currency_{currency_to_fetch}.json"

    try:
        data = fetch_currency_data(api_key, currency_to_fetch)
        save_data_to_file(data, target_file)
        print(f"Başarılı: {currency_to_fetch} verisi {target_file} dosyasına yazıldı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")


if __name__ == "__main__":
    main()
