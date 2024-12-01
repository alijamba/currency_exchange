import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ExchangeRates')

# ECB URL
ECB_URL = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"


def fetch_ecb_exchange_rates():
    """Fetch exchange rates from the ECB website."""
    response = requests.get(ECB_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", class_="forextable")

    rates = {}
    rows = table.find_all("tr")[1:]  # Skip the header
    for row in rows:
        cols = row.find_all("td")
        currency = cols[0].text.strip()
        rate = float(cols[2].text.strip())  # Assuming the rate is in the third column
        rates[currency] = rate
    return rates


def fetch_previous_rates():
    """Fetch exchange rates from the previous day stored in DynamoDB."""
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    response = table.query(
        KeyConditionExpression=Key('date').eq(yesterday)
    )
    return {item['currency']: float(item['rate']) for item in response['Items']}


def lambda_handler(event, context):
    try:
        # Fetch current exchange rates from ECB
        current_rates = fetch_ecb_exchange_rates()

        # Fetch previous day's rates from DynamoDB
        previous_rates = fetch_previous_rates()

        # Get today's date
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # Save current rates and calculate changes
        with table.batch_writer() as batch:
            for currency, rate in current_rates.items():
                change = rate - previous_rates.get(currency, 0)
                batch.put_item({
                    "currency": currency,
                    "date": today,
                    "rate": Decimal(str(rate)),
                    "change": Decimal(str(change))
                })

        # If the request is for an API call, return the data
        if event.get('httpMethod') == 'GET':
            # Query today's rates
            response = table.query(
                KeyConditionExpression=Key('date').eq(today)
            )
            data = [
                {
                    "currency": item['currency'],
                    "rate": float(item['rate']),
                    "change": float(item['change'])
                }
                for item in response['Items']
            ]
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "date": today,
                    "exchange_rates": data
                }
            }

        # If this is not a GET request, return success for the processing
        return {"statusCode": 200, "message": "Exchange rates processed successfully."}
    except Exception as e:
        return {"statusCode": 500, "error": str(e)}

