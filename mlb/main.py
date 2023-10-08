import time
import mlb
import os

print('start')

gNetRoot = ''

def main(test):
    if test:
        # В тестовом режиме
        base_url = 'https://testnet.binance.vision'  # Ссылка на тестовую документацию
        api_key = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 't_api_key.txt'))
        api_secret = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 't_api_secret.txt'))
        gNetRoot = os.path.join('Z:\\', '#TEST')
    else:
        # В реальном режиме
        base_url = 'https://api2.binance.com'  # Ссылка на документацию
        api_key = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 'r_api_key.txt'))
        api_secret = mlb.read_text_from_file(os.path.join('C:\\', 'keys', 'r_api_secret.txt'))
        gNetRoot = os.path.join('Z:\\', '#REAL')

    print('gNetRoot=', gNetRoot)
    while True:
        print('api_key=', api_key)
        print('api_secret=', api_secret)
        time.sleep(3)