import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = os.environ.get("STOCK_API")
NEWS_API = os.environ.get("NEWS_API")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
MY_NUMBER = os.environ.get("MY_NUMBER")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

stock_parameters= {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
#list comprehension
yesterday_data = data_list[0]
yesterday_closing = yesterday_data["4. close"]
yesterday_closing = float(yesterday_closing)
day_before_yesterday = data_list[1]
day_before_yesterday_closing = day_before_yesterday["4. close"]
day_before_yesterday_closing = float(day_before_yesterday_closing)


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


percent_change = get_change(yesterday_closing, day_before_yesterday_closing)

news_parameters = {
    "q": COMPANY_NAME,
    "from": yesterday_data,
    "sortBy": "popularity",
    "apiKey": NEWS_API
}
volatile = False
if percent_change >= 5 or percent_change <= -5:
    volatile = True
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

if volatile:
    formatted_articles = [f"Headline: {article['title']}\nBrief: {article['description']}"
                          for article in three_articles]
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=article,
            from_=TWILIO_NUMBER,
            to=MY_NUMBER
            )

    print(message.status)
