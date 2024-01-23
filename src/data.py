import requests
import pandas as pd
import yfinance as yf

달러원= 'USDKRW=X'

def 은행고시환율_가져오기():
    URL = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    return requests.get(URL).json()[0]

def 야후파이낸스환율_가져오기():
    df = yf.Ticker(달러원).history(period='1d', interval='1m')
    df.index = df.index.tz_convert('Asia/Seoul')
    return df

def 야후파이낸스환율추이_가져오기(기간, 이평선, ATR계수):
    df = yf.Ticker(달러원).history(period='max')
    df.index = df.index.date
    th = pd.concat([df.Close, df.High], axis=1).max(axis=1)
    tl = pd.concat([df.Close, df.Low], axis=1).min(axis=1)
    tr = th - tl
    df[f'ATR{이평선}'] = tr.ewm(이평선).mean().shift(1)
    df[f'SMA{이평선}'] = df.Close.rolling(이평선).mean().shift(1)
    df[f'SMA{이평선}_UPPER'] = df[f'SMA{이평선}'] + df[f'ATR{이평선}'] * ATR계수
    df[f'SMA{이평선}_LOWER'] = df[f'SMA{이평선}'] - df[f'ATR{이평선}'] * ATR계수
    df.dropna(inplace=True)
    return df.loc[:, ['Close', 'High', 'Low',
        f'SMA{이평선}', f'SMA{이평선}_UPPER', f'SMA{이평선}_LOWER']].tail(기간)