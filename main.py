import argparse
import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

class ExchangeRateParser:
    @staticmethod
    def parse_exchange_rate(data):
        exchange_rate = {}
        for rate in data.get('exchangeRate', []):
            currency = rate.get('currency')
            if currency in ['EUR', 'USD']:
                exchange_rate[currency] = {
                    'sale': rate.get('saleRate'),
                    'purchase': rate.get('purchaseRate')
                }
        return exchange_rate

async def fetch_exchange_rates(api_url, days):
    exchange_rates = []
    async with aiohttp.ClientSession() as session:
        for day in range(1, days + 1):
            date = (datetime.today() - timedelta(days=day)).strftime('%d.%m.%Y')
            params = {
                'json': '',
                'date': date
            }
            async with session.get(api_url, params=params) as response:
                data = await response.text()
                data_dict = json.loads(data)
                exchange_rates.append({date: ExchangeRateParser.parse_exchange_rate(data_dict)})
    return exchange_rates

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch exchange rates for EUR and USD from PrivatBank API.")
    parser.add_argument("days", type=int, default=2, nargs="?", help="Number of days to fetch exchange rates for (up to 10 days). Default is 2.")
    args = parser.parse_args()

    if args.days > 10:
        print("Error: You can fetch exchange rates for up to 10 days only.")
        exit(1)

    api_url = "https://api.privatbank.ua/p24api/exchange_rates"
    loop = asyncio.get_event_loop()

    exchange_rates = loop.run_until_complete(fetch_exchange_rates(api_url, args.days))

    print(exchange_rates)
