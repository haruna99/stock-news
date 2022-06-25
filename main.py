import requests
import datetime as dt
from twilio.rest import Client
import os

account_sid = os.environ.get("TWILIO_ID")
auth_token = os.environ.get("TWILIO_API_KEY")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_URL = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")

stock_parameters = {
    "apikey": STOCK_API_KEY,
    "symbol": STOCK,
    "function": "TIME_SERIES_DAILY"
}

response = requests.get(url=STOCK_API_URL, params=stock_parameters)
response.raise_for_status()
data = response.json()
stock_data = data["Time Series (Daily)"]

today = dt.date.today()
yesterday = str(today - dt.timedelta(days=1))
day_before = str(today - dt.timedelta(days=2))

yesterday_stock = float(stock_data[yesterday]["4. close"])
day_before_stock = float(stock_data[day_before]["4. close"])
percentage_change = round((yesterday_stock - day_before_stock)/yesterday_stock * 100, 2)
if abs(percentage_change) > 0:
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url=NEWS_API_URL, params=news_parameters)
    response.raise_for_status()
    data = response.json()
    news = data["articles"][:3]
    if percentage_change < 5:
        change = f"TSLA: 🔺{percentage_change}%"
    if percentage_change < -5:
        change = f"TSLA: 🔻{abs(percentage_change)}%"
    for new in news:
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body=f"{change}\nHeadline: {new['title']}\n Brief: {new['description']}",
                from_='+19855318330',
                to='+14053343782'
            )
