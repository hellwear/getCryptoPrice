#! /usr/bin/python

from locale import currency
from pycoingecko import CoinGeckoAPI
from rich.console import Console
from rich.table import Table
import requests
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f')
args = parser.parse_args()

f = args.f

cg = CoinGeckoAPI()

price = cg.get_price(ids=['bitcoin', 'ethereum', 'the-open-network', 'tron', 'solana'], vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)

res_usd = requests.get('https://free.currconv.com/api/v7/convert?apiKey=cd2ff852330c08894153&q=USD_RUB&compact=ultra')
res_eur = requests.get('https://free.currconv.com/api/v7/convert?apiKey=cd2ff852330c08894153&q=EUR_RUB&compact=ultra')

usd_price = res_usd.text
eur_price = res_eur.text

procent_color = 'green'

def toFixed(numObj, digits):
    return f"{numObj:.{digits}f}"

if toFixed(price['bitcoin']['usd_24h_change'], 2)[0] == '-':
    procent_color = 'red'

if toFixed(price['ethereum']['usd_24h_change'], 2)[0] == '-':
    procent_color = 'red'

if toFixed(price['the-open-network']['usd_24h_change'], 2)[0] == '-':
    procent_color = 'red'

if toFixed(price['tron']['usd_24h_change'], 2)[0] == '-':
    procent_color = 'red'

if toFixed(price['solana']['usd_24h_change'], 2)[0] == '-':
    procent_color = 'red'

def getCurrency():

    # FIRST TABLE
    table_crypto = Table(title="Courses cryptocurrencies")
    
    table_crypto.add_column('Currencies', style='cyan', no_wrap=True)
    table_crypto.add_column('Price', style='green', no_wrap=True)
    table_crypto.add_column('Market cap', style='green', no_wrap=True)
    table_crypto.add_column('Volume 24H', style='green', no_wrap=True)
    table_crypto.add_column('Change 24H', style=procent_color, no_wrap=True)

    table_crypto.add_row('Bitcoin', str(toFixed(price['bitcoin']['usd'], 4)) + '$', str(toFixed(price['bitcoin']['usd_market_cap'], 2)) + '$', str(toFixed(price['bitcoin']['usd_24h_vol'], 2)) + '$', str(toFixed(price['bitcoin']['usd_24h_change'], 2)) + '%')
    table_crypto.add_row('Ethereum', str(toFixed(price['ethereum']['usd'], 4)) + '$', str(toFixed(price['ethereum']['usd_market_cap'], 2)) + '$', str(toFixed(price['ethereum']['usd_24h_vol'], 2)) + '$', str(toFixed(price['ethereum']['usd_24h_change'], 2)) + '%')
    table_crypto.add_row('Toncoin', str(toFixed(price['the-open-network']['usd'], 4)) + '$', str(toFixed(price['the-open-network']['usd_market_cap'], 2)) + '$', str(toFixed(price['the-open-network']['usd_24h_vol'], 2)) + '$', str(toFixed(price['the-open-network']['usd_24h_change'], 2)) + '%')
    table_crypto.add_row('Tron', str(toFixed(price['tron']['usd'], 4)) + '$', str(toFixed(price['tron']['usd_market_cap'], 2)) + '$', str(toFixed(price['tron']['usd_24h_vol'], 2)) + '$', str(toFixed(price['tron']['usd_24h_change'], 2)) + '%')
    table_crypto.add_row('Solana', str(toFixed(price['solana']['usd'], 4)) + '$', str(toFixed(price['solana']['usd_market_cap'], 2)) + '$', str(toFixed(price['solana']['usd_24h_vol'], 2)) + '$', str(toFixed(price['solana']['usd_24h_change'], 2)) + '%')
    
    # SECOND TABLE
    table_fiat = Table(title="Courses fiat currencies")
    table_fiat.add_column('Currency', style='cyan', no_wrap=True)
    table_fiat.add_column('Price', style='cyan', no_wrap=True)

    try:
        table_fiat.add_row('USD', str(usd_price.split(':')[1].split('}')[0]) + '₽')
        table_fiat.add_row('EUR', str(eur_price.split(':')[1].split('}')[0]) + '₽')
    except:
        table_fiat.add_row('USD', 'API ERROR')
        table_fiat.add_row('EUR', 'API ERROR')

    console = Console()

    if f == 'crypto':
        console.print(table_crypto)
    if f == 'fiat':
        console.print(table_fiat)
    if f == 'all':
        console.print(table_crypto, table_fiat)