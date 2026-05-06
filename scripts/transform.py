import json
import logging

import pandas as pd

from scripts.utils.config import FINAL_DATA_CSV, RAW_DATA_JSON

# İsimlendirilmiş Logger (Claude'un A09 uyarısı için)
logger = logging.getLogger("currency_etl.transform")


def normalize_currency_data(data):
    return pd.json_normalize(data)


def adjust_column_names(df):
    df.columns = df.columns.str.replace("conversion_rates.", "", regex=False)
    return df


def melt_currency_rates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.melt(ignore_index=False).reset_index()
    return df


def add_metadata_columns(df: pd.DataFrame, base_currency: str, last_updated: str):
    # 'variable' -> target_currency, 'value' -> rate
    df.rename(columns={"variable": "target_currency", "value": "rate"}, inplace=True)

    # Parametreden gelen temiz veriyi basıyoruz
    df["base_currency"] = base_currency
    df["last_updated"] = last_updated

    if "index" in df.columns:
        df.drop(columns=["index"], inplace=True)
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    df["last_updated"] = pd.to_datetime(df["last_updated"], utc=True)
    return df


def filter_currency_codes(df: pd.DataFrame) -> pd.DataFrame:
    # Sadece 3 harfli standart kodları tut (USD, TRY vb.)
    return df[df["target_currency"].str.len() == 3]


def main():
    logger.info("Transformasyon süreci başlıyor...")

    try:
        with open(RAW_DATA_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = normalize_currency_data(data)
        df = adjust_column_names(df)
        df = melt_currency_rates(df)

        base_currency = data["base_code"]
        last_updated = data["time_last_update_utc"]

        df = add_metadata_columns(df, base_currency, last_updated)
        df = convert_types(df)
        df = filter_currency_codes(df)

        # GÜNCELLEME: "currency-v3.csv" yerine Config'den gelen standart yol
        df.to_csv(FINAL_DATA_CSV, encoding="utf-8", index=False)

        logger.info(
            f"Transformasyon tamamlandı. Veri {FINAL_DATA_CSV} adresine yazıldı."
        )
        print(df.head(10))

    except Exception as e:
        logger.error(f"Transformasyon sırasında hata: {e}")
        raise


if __name__ == "__main__":
    main()
