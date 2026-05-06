import json
from locale import currency

import requests


def fetch_currency_data(api_url):
    # Making our request
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()


def save_data_to_file(data, file_path):
    with open("currency.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def main():
    # Where USD is the base currency you want to use
    url = "https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/TRY"
    try:
        data = fetch_currency_data(url)
        save_data_to_file(data, "currency.json")
        print("İşlem başarıyla tamamlandı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
