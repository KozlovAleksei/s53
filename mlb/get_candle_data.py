import requests  # Импорт модуля requests для выполнения HTTP-запросов
from pandas import DataFrame  # Импорт класса DataFrame из модуля pandas
import time  # Импорт модуля time для работы со временем
from datetime import datetime

# для вывода всех колонок для отладки print(df[['time', 'open', 'high', 'low', 'close']])
# import pandas as pd
# pd.set_option("display.max_columns", None)  # Установка значения display.max_columns равное None

def get_candle_data(symbol, interval, cl, base_url="https://api.binance.com", end_point="/api/v3/exchangeInfo"):

    print('symbol=', symbol)
    print('interval=', interval)
    print('cl=', cl)
    """
    Функция для получения информации о символе
    :param symbol: символ
    :param interval: интервал
    :param cl: экземпляр объекта для взаимодействия с биржей
    :param base_url: базовый URL для API биржи
    :param end_point: конечная точка для получения информации о символе
    :return: кортеж с значениями gOpenPrice, gDights, gTick_size
    """

    def get_open_price_0(symbol, interval):
        """
        Функция для получения открытой цены для заданного символа и интервала
        :param symbol: символ
        :param interval: интервал
        :return: объект DataFrame с данными об открытой цене
        """
        df = DataFrame(cl.klines(symbol, interval, limit=1)).iloc[:, :6]  # Получение данных о свечах и извлечение только нужных столбцов
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']  # Присвоение имен столбцам
        return df.iloc[-1]  # Возвращение последней записи (последней строки) данных

    def get_high_low(symbol, interval, num_candles):
        """
        Функция для получения максимального значения high и минимального значения low для заданного количества свечей
        :param symbol: символ
        :param interval: интервал
        :param num_candles: количество свечей (кроме нулевой)
        :return: кортеж с максимальным значением high и минимальным значением low
        """
        df = DataFrame(cl.klines(symbol, interval, limit=num_candles + 1)).iloc[-(num_candles + 1):,
             :6]  # Получение данных о последних (num_candles + 1) свечах и извлечение только нужных столбцов
        df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']  # Присвоение имен столбцам
        # df = df.iloc[::-1]  # Инвертирование порядка строк в DataFrame

        # Преобразование значения столбца 'time' в формат времени в немецком стиле
        df['time'] = df['time'].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime('%d.%m.%Y %H:%M:%S'))
        df = df.drop(df.index[-1])  # Удаление последней строки в DataFrame

        # print(df[['time', 'open', 'high', 'low', 'close']])

        highest = df['high'].max()  # Вычисление максимального значения high
        lowest = df['low'].min()  # Вычисление минимального значения low
        return highest, lowest  # Возвращение максимального значения high и минимального значения low

    def get_gDights(gTick_size):
        """
        Функция для вычисления количества значащих символов в заданной величине gTick_size
        :param gTick_size: заданная величина gTick_size
        :return: количество значащих символов
        """
        str_gTick_size = str(gTick_size)
        decimal_part = str_gTick_size.split('.')[-1]  # Получение десятичной части величины
        return len(decimal_part.rstrip('0'))  # Получение количества значащих символов


    while True:
        try:
            result01 = get_open_price_0(symbol, interval)  # Получение открытой цены
            SL_for_S, SL_for_B = get_high_low(symbol, interval, 3)
            get_json2 = requests.get(f"{base_url}{end_point}?symbol={symbol}")  # Выполнение GET-запроса к API биржи для получения информации о символе
            break
        except Exception as e:
            print('Ошибка:', e)
            time.sleep(21)  # Пауза в 21 секунду при возникновении исключения

    gTick_size = float(get_json2.json()["symbols"][0]["filters"][0]["tickSize"])  # Извлечение значения gTick_size из полученных JSON данных
    gDights = get_gDights(gTick_size)  # Вычисление значения gDights для gTick_size
    gOpenPrice = round(float(result01['open']), gDights)  # Округление открытой цены до заданного количества знаков после запятой
    SL_for_S = round(float(SL_for_S), gDights)
    SL_for_B = round(float(SL_for_B), gDights)



    # symbol_data = {}  # Создание пустого словаря symbol_data
    # symbol_data['gOpenPrice'] = gOpenPrice
    # symbol_data['gDights'] = gDights
    # symbol_data['gTick_size'] = gTick_size

    return gOpenPrice, SL_for_S, SL_for_B, gDights, gTick_size  # Возврат значений gOpenPrice, gDights, gTick_size