import json
from locale import currency

import dictionary
import requests

# Where USD is the base currency you want to use
url = 'https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/TRY'

# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)

with open("currency.json", "w") as outfile:
    json.dump(data, outfile)