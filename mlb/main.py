from binance.spot import Spot  # pip install binance-connector
from binance.error import ClientError

import time
import mlb
import os

print('start')

gNetRoot = ''
symbol = "BTCUSDT"
interval = "15m"

def main(test):
    if test:
        # В тестовом режиме
        base_url = 'https://testnet.binance.vision'  # Ссылка на тестовую документацию
        api_key = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 't_api_key.txt'))
        api_secret = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 't_api_secret.txt'))
        gNetRoot = os.path.join('C:\\', '#TEST')
    else:
        # В реальном режиме
        base_url = 'https://api2.binance.com'  # Ссылка на документацию
        api_key = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 'r_api_key.txt'))
        api_secret = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 'r_api_secret.txt'))
        gNetRoot = os.path.join('C:\\', '#REAL')

    if not os.path.exists(gNetRoot):
        os.makedirs(gNetRoot)

    cl = Spot(api_key=api_key, api_secret=api_secret, base_url=base_url)
    print('base_url=', base_url)

    print('gNetRoot=', gNetRoot)
    while True:
        print('api_key=', api_key)
        print('api_secret=', api_secret)
        gOpenPrice, SL_for_S, SL_for_B, gDights, gTick_size = mlb.get_candle_data(symbol, interval, cl)
        print('gOpenPrice=', gOpenPrice)
        print('SL_for_S=', SL_for_S)
        print('SL_for_B=', SL_for_B)
        print('gDights=', gDights)
        print('gTick_size=', gTick_size)

        breakpoint()
        time.sleep(3)