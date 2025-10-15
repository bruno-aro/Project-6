import requests
import os

def get_data(event, context):
    api_key = os.getenv("API_KEY")
    symbol = "BTC"
    market = "EUR"

    endpoint = (
        f"https://www.alphavantage.co/query"
        f"?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={api_key}"
    )

    response = requests.get(endpoint)

    if response.status_code != 200:
        return None

    response_json = response.json()

    # Handle rate limits / errors gracefully
    time_series = response_json.get("Time Series (Digital Currency Daily)", {})
    if not time_series:
        return None

    latest_date = sorted(time_series.keys())[-1]
    latest_data = time_series[latest_date]

    open_price  = latest_data.get("1a. open (USD)")
    high_price  = latest_data.get("2a. high (USD)")
    low_price   = latest_data.get("3a. low (USD)")
    close_price = latest_data.get("4a. close (USD)")
    volume      = latest_data.get("5. volume")

    return [latest_date, open_price, high_price, low_price, close_price, volume]