import requests
import os

def get_data(event, context):
    api_key = os.getenv("API_KEY")
    symbol = "BTC"

    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&market=USD&apikey={api_key}"

    response = requests.get(endpoint)

    if response.status_code == 200:
        response_json = response.json()

        time_series = response_json.get("Time Series (Daily)", {})
        if not time_series:
            return None

        latest_date = sorted(time_series.keys())[-1]
        latest_data = time_series[latest_date]

        open_price = latest_data["1. open"]
        high_price = latest_data["2. high"]
        low_price = latest_data["3. low"]
        close_price = latest_data["4. close"]
        volume = latest_data["5. volume"]

        data = [latest_date, open_price, high_price, low_price, close_price, volume]
        return data