from utils.io_handler import read_json_to_df, save_df_to_csv


def convert_json_to_csv(input_path="currency.json", output_path="currency.csv"):
    # 1. Veriyi Oku (I/O utils'den geliyor)
    df = read_json_to_df(input_path)

    # 2. Varsa Dönüşüm/Temizlik İşlemleri Burada Yapılır
    # (Şimdilik doğrudan yazıyoruz ama yerimiz hazır)

    # 3. Veriyi Yaz (I/O utils'den geliyor)
    save_df_to_csv(df, output_path)


if __name__ == "__main__":
    convert_json_to_csv()
