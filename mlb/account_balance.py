import datetime
import os
from binance.error import ClientError

def account_balance(gNetRoot, cl):
    # print('account_balance')
    btc_balance = None
    usdt_balance = None

    # json_data = None
    try:
        json_data = cl.account()

    except ClientError as ce:
        print(f"Ошибка в account_balance при получении данных в json_data из account: {ce}")
        return -1, -1, -1, 'NoFile'

    except Exception as e:
        print(f"Ошибка в account_balance при получении данных в json_data из account: {e}")
        return -1, -1, -1, 'NoFile'

    # if json_data == None:
    #     return -1, -1, -1, 'NoFile'

    for balance in json_data['balances']:
        if balance['asset'] == 'BTC':
            btc_balance = float(balance['free']) + float(balance['locked'])
        elif balance['asset'] == 'USDT':
            usdt_balance = float(balance['free']) + float(balance['locked'])

    # sellPrice = float(cl.book_ticker(symbol='BTCUSDT').get('bidPrice'))
    sellPrice = 30000  # Устанавливаем фиксированную, иначе не понятно растут деньги или нет

    if btc_balance is not None and usdt_balance is not None and sellPrice is not None:
        # Расчет итоговой суммы в USDT
        gAccountBalance = float((btc_balance * sellPrice) + usdt_balance)
        print('btc_balance=', round(btc_balance, 5),
              '~', int(gAccountBalance-usdt_balance),
              'usdt_balance=', int(usdt_balance),
               'gAccountBalance=', int(gAccountBalance))

        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        line = f'{timestamp}\t{int(gAccountBalance)}\n'

        # BalanceFile = gNetRoot + datetime.datetime.now().strftime('%d-%m-%Y') + '.txt'
        BalanceFile = os.path.join(gNetRoot, datetime.datetime.now().strftime('%d-%m-%Y') + '.txt')

        with open(BalanceFile, 'a', encoding='utf-8') as file:
            file.write(line)
        #plot_graph(filename)
        
        return round(gAccountBalance, 2), round(btc_balance, 6), round(usdt_balance, 2), BalanceFile

    return -1, -1,  -1, 'NoFile'
