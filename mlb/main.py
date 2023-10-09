from binance.spot import Spot  # pip install binance-connector
from binance.error import ClientError

import time
import datetime
import mlb
import os

print('start')

gNetRoot = ''
symbol = "BTCUSDT"
# interval = "30m"
# interval = "1h"
interval = "4h"
# interval = "1d"

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
        # print('api_key=', api_key)
        # print('api_secret=', api_secret)
        signal, LastCandleTime, gOpenPrice, gClosePrice, SL_for_S, SL_for_B, up_level, dn_level, gDights, gTick_size = mlb.get_candle_data(symbol, interval, cl)
        print('signal=', signal)
        print('LastCandleTime=', LastCandleTime)
        print('gOpenPrice=', gOpenPrice)
        print('gClosePrice=', gClosePrice)
        print('SL_for_S=', SL_for_S)
        print('SL_for_B=', SL_for_B)
        print('up_level=', up_level)
        print('dn_level=', dn_level)
        print('gDights=', gDights)
        print('gTick_size=', gTick_size)
        server_time = cl.time()['serverTime']
        Time1 = datetime.datetime.fromtimestamp(server_time / 1000).strftime('%H:%M:%S')
        Time2 = datetime.datetime.now().strftime('%H:%M:%S')
        mlb.synchronize_system_time(Time1, Time2)
        print('(', Time1, Time2, ')')

        global gAccountBalance, btc_balance, usdt_balance, BalanceFile
        gAccountBalance, btc_balance, usdt_balance, BalanceFile = mlb.account_balance(gNetRoot, cl)

        # Вычитаем 1 %
        lots_for_buy_btc = (usdt_balance / gOpenPrice) - (0.01 * (usdt_balance / gOpenPrice))
        print('lots_for_buy_btc=', round(lots_for_buy_btc, 4))

        if btc_balance == 0 and gClosePrice > SL_for_S:
            signal = 'BUY'

        if usdt_balance >= 100 and gClosePrice < SL_for_B:
            signal = 'SELL'

        if signal == 'BUY' or signal == 'SELL':

            if signal == 'BUY' and usdt_balance >= 100:
                trans_id = '1' + mlb.get_str_rnd(6)
                try:

                    mlb.send_market_order(symbol, signal, round(lots_for_buy_btc, 5), 'Market-P', cl, trans_id)
                except Exception as e:
                    print("Произошла ошибка при BUY:", e)

            if signal == 'SELL' and btc_balance != 0:
                trans_id = '2' + mlb.get_str_rnd(6)
                try:
                    mlb.send_market_order(symbol, signal, round(btc_balance, 5), 'Market-P', cl, trans_id)
                except Exception as e:
                    print("Произошла ошибка при SELL:", e)



        time.sleep(3)