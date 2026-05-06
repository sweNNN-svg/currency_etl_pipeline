import json

import pandas as pd


def read_json_to_df(file_path):
    """JSON dosyasını okur ve DataFrame döner."""
    with open(file_path, encoding="utf-8-sig") as f:
        return pd.read_json(f)


def save_df_to_csv(df, file_path):
    """DataFrame'i CSV olarak kaydeder."""
    df.to_csv(file_path, encoding="utf-8", index=True)
