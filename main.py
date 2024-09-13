import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+12513195842"
VERIFIED_NUMBER = "+9108910398654"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "GRMU4HSKH0FJ0PZU"
NEWS_API_KEY = "f0839cb9ad664f5b967411019796f3c3"
TWILIO_SID = "AC5de4ab1dee02b8e133956ae33b4e76d9"
TWILIO_AUTH_TOKEN = "5aa72ecb441ca585fbce48a85dd7f963"

#yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#Find the difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "+"
else:
    up_down = "-"

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

#If difference percentage is greater than 3 then print("Get News").
if abs(diff_percent) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    #extrating first 3 articles
    three_articles = articles[:3]
    print(three_articles)

    #Creating a new list of the first 3 articles' headline and description using list comprehension.
    formatted_articles = [(f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. "
                           f"\nBrief: {article['description']}") for article in three_articles]
    print(formatted_articles)
    #Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    #Sending message for each articles
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
