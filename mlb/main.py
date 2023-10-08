import time
import mlb
print('start')

gNetRoot = ''

def main(test):
    if test:
        # test
        base_url = 'https://testnet.binance.vision'  # https://youtu.be/NczNjVxwx3A?t=636
        api_key = mlb.read_text_from_file('C:\\keys\\t_api_key.txt')
        api_secret = mlb.read_text_from_file('C:\\keys\\t_api_secret.txt')
        gNetRoot = "Z:\\#TEST\\"
    else:
        # real
        base_url = 'https://api2.binance.com'  # https://binance-docs.github.io/apidocs/spot/en/#general-info
        api_key = mlb.read_text_from_file('C:\\keys\\r_api_key.txt')
        api_secret = mlb.read_text_from_file('C:\\keys\\r_api_secret.txt')
        gNetRoot = "Z:\\#REAL\\"



    print('gNetRoot=', gNetRoot)
    while True:
        print('api_key=', api_key)
        print('api_secret=', api_secret)
        time.sleep(3)
