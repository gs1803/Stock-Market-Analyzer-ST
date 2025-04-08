import yfinance as yf
import pytz
from datetime import datetime, timedelta

etNow = datetime.now(pytz.timezone('US/Eastern')).date()

def download_stock_data(userStock, startDate, endDate):
    dateDiff = abs((startDate - endDate).days) - 1

    if dateDiff == 0:
        if startDate.isoweekday() == 6:
            start = startDate - timedelta(days = 1)                  
            end = endDate - timedelta(days = 1)
            inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False, auto_adjust=False)
        elif startDate.isoweekday() == 7:
            start = startDate - timedelta(days = 2)                    
            end = endDate - timedelta(days = 2)
            inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False, auto_adjust=False)
        elif etNow - startDate.date() >= timedelta(days = 30):
            inputStock = yf.download(f"{userStock}", start, end, progress = False, auto_adjust=False)
        else:
            inputStock = yf.download(f"{userStock}", startDate, endDate, interval = '1m', progress = False, auto_adjust=False)
    elif dateDiff == 1:
        if startDate.isoweekday() == 6 or startDate.isoweekday() == 7 or endDate.isoweekday() - 1 == 6 or endDate.isoweekday() - 1 == 7:
            if startDate.isoweekday() == 5:
                end = endDate - timedelta(days = 1)
                inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False, auto_adjust=False)
            else:
                start = startDate - timedelta(days = 1)                    
                end = endDate - timedelta(days = 1)
                inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False, auto_adjust=False)
        else:
            inputStock = yf.download(f"{userStock}", startDate, endDate, progress = False, auto_adjust=False)
    elif dateDiff == 2 and startDate.isoweekday() == 5:
        end = endDate - timedelta(days = 2)
        inputStock = yf.download(f"{userStock}", startDate, end, interval = '1m', progress = False, auto_adjust=False)
    else:
        inputStock = yf.download(f"{userStock}", startDate, endDate, progress = False, auto_adjust=False)

    inputStock = inputStock.xs(f"{userStock}", axis=1, level="Ticker").reset_index()
    return inputStock
