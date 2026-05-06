from scripts.utils.config import RAW_DATA_CSV, RAW_DATA_JSON
from scripts.utils.io_handler import read_json_to_df, save_df_to_csv


def convert_json_to_csv():
    # Artık 'currency.json' yerine merkezden gelen sabiti kullanıyoruz
    df = read_json_to_df(RAW_DATA_JSON)
    save_df_to_csv(df, RAW_DATA_CSV)


if __name__ == "__main__":
    convert_json_to_csv()
