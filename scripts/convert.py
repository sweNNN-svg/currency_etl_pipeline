import pandas as pd

with open('currency.json', encoding='utf-8-sig') as f_input:
    df = pd.read_json(f_input)

df.to_csv('currency.csv', encoding='utf-8', index=True)