import pandas as pd
import json

# JSON dosyasını oku
def load_json_file(filepath: str) -> dict:
    # Verilen path'deki JSON dosyasını okur ve Python dict olarak döner.
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

# JSON verisini normalize et (json.normalize)
def normalize_currency_data(data):
    # RAW JSON'dan pandas DataFrame oluşturur.
    df = pd.json_normalize(data)
    return df

# Sütun isimlerini düzelt
def adjust_column_names(df):
    df.columns = df.columns.str.replace('conversion_rates.', '', regex=False)
    return df

# DataFrame'i melt ile long formata çevir
def melt_currency_rates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.melt(ignore_index=False).reset_index()
    return df

# Ek metadata ekle
def add_metadata_columns(df: pd.DataFrame, base_currency: str, last_updated: str):
    df.rename(columns={'variable':'target_currency'}, inplace=True)
    df.rename(columns={'index':'base_currency'}, inplace=True)
    df.rename(columns={'value':'rate'}, inplace=True)
    df['last_updated'] = last_updated
    return df

# type dönüşümleri
def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    df['base_currency'] = df['base_currency'].astype(str)  # Önce sütunu string'e çevir
    df.loc[df['base_currency'] == '0', 'base_currency'] = 'TRY'  # Sonra değişikliği yap
    df['last_updated'] = pd.to_datetime(df['last_updated'], utc=True)
    return df

# 3 Harfli olmayan currency kodlarını filtrele / daha iyi bir yönetim varsa yapabilirsin
def filter_currency_codes(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['target_currency'].str.len() == 3]

# CSV'ye yazdırma
def write_csv(df: pd.DataFrame):
    df.to_csv('currency-v3.csv', encoding='utf-8', index=False)
    
    
def main():
    data = load_json_file("currency.json")
    df = normalize_currency_data(data)
    df = adjust_column_names(df)
    df = melt_currency_rates(df)

    base_currency = data['base_code']
    last_updated = data['time_last_update_utc']

    df = add_metadata_columns(df, base_currency, last_updated)
    df = convert_types(df)
    df = filter_currency_codes(df)

    write_csv(df)
    print(df.head(10))

if __name__ == "__main__":
    main()