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
            inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False)
        elif startDate.isoweekday() == 7:
            start = startDate - timedelta(days = 2)                    
            end = endDate - timedelta(days = 2)
            inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False)
        elif etNow - startDate.date() >= timedelta(days = 30):
            inputStock = yf.download(f"{userStock}", start, end, progress = False)
        else:
            inputStock = yf.download(f"{userStock}", startDate, endDate, interval = '1m', progress = False)
    elif dateDiff == 1:
        if startDate.isoweekday() == 6 or startDate.isoweekday() == 7 or endDate.isoweekday() - 1 == 6 or endDate.isoweekday() - 1 == 7:
            if startDate.isoweekday() == 5:
                end = endDate - timedelta(days = 1)
                inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False)
            else:
                start = startDate - timedelta(days = 1)                    
                end = endDate - timedelta(days = 1)
                inputStock = yf.download(f"{userStock}", start, end, interval = '1m', progress = False)
        else:
            inputStock = yf.download(f"{userStock}", startDate, endDate, progress = False)
    elif dateDiff == 2 and startDate.isoweekday() == 5:
        end = endDate - timedelta(days = 2)
        inputStock = yf.download(f"{userStock}", startDate, end, interval = '1m', progress = False)
    else:
        inputStock = yf.download(f"{userStock}", startDate, endDate, progress = False)

    return inputStock
