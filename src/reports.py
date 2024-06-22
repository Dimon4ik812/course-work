import requests
from dotenv import load_dotenv
import os
import json

load_dotenv(os.path.join("..", ".env"))
API_KEY = os.getenv("API_KEY")


def get_currency_rate_request():
    url = "https://api.apilayer.com/fixer/latest?symbols=EUR,USD&base=RUB"

    payload = {}


    response = requests.request("GET", url, headers={"apikey": API_KEY}, data=payload)

    status_code = response.status_code
    result = response.json()
    result['rates']['EUR'] = round(1 / result['rates']['EUR'], 2)
    result['rates']['USD'] = round(1 / result['rates']['USD'], 2)

    return result

with open('../user_settings.json', 'r') as file:
    user_choice = json.load(file)
load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
datetime_str = "30.06.2018"

companys = user_choice["user_stocks"]



def company(company, api_key_stocks):
    for com in company:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={com}&apikey={api_key_stocks}'
        # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={com}&apikey={api_key_stocks}'
        r = requests.get(url)
        # print(f'{r.status_code}')
        dates = r.json()
    return dates


if __name__ == '__main__':
    company = company(companys, api_key_stocks)
    print(company)