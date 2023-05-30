import pandas as pd
import numpy as np

class TechnicalAnalysis:
    def rsi_calculation(data, lookback) -> pd.DataFrame:
        returns = data.diff()
        up = []
        down = []

        for i in range(len(returns)):
            if returns[i] < 0:
                up.append(0)
                down.append(returns[i])
            else:
                up.append(returns[i])
                down.append(0)
        
        up_series = pd.Series(up)
        down_series = pd.Series(down).abs()
        
        up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
        down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()

        rs = up_ewm / down_ewm
        rsi = 100 - (100 / (1 + rs))
        rsi_df = pd.DataFrame(rsi).rename(columns = {0: 'rsi'}).set_index(data.index)
        rsi_df = rsi_df.dropna()

        return rsi_df[3:]

    def macd_calculations(data, slow, fast, smooth) -> pd.DataFrame:
        exp1 = data.ewm(span = fast, adjust = False).mean()
        exp2 = data.ewm(span = slow, adjust = False).mean()
        macd = pd.DataFrame(exp1 - exp2).rename(columns = {'Adj Close': 'macd'})
        signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
        hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
        frames =  [macd, signal, hist]
        macdInfoDf = pd.concat(frames, join = 'inner', axis = 1)
        
        return macdInfoDf

    def sma_calculations(data, window) -> pd.DataFrame:
        sma = data.rolling(window = window).mean()
        
        return sma

    def bollinger_bands_calculations(data, sma, window) -> pd.DataFrame:
        std = data.rolling(window = window).std()
        upper_band = sma + std * 2
        lower_band = sma - std * 2

        return upper_band, lower_band

    def donchian_breakout_calculations(data, high_prices, low_prices, window) -> tuple:
        upper_channel = high_prices.rolling(window = window).max()
        lower_channel = low_prices.rolling(window = window).min()
    
        return upper_channel, lower_channel

    def implement_rsi(data, rsi) -> tuple:    
        rsi_buy_price = []
        rsi_sell_price = []
        rsi_signal = []
        signal = 0

        for i in range(len(rsi)):
            if rsi[i - 1] > 30 and rsi[i] < 30:
                if signal != 1:
                    rsi_buy_price.append(data[i])
                    rsi_sell_price.append(np.nan)
                    signal = 1
                    rsi_signal.append(signal)
                else:
                    rsi_buy_price.append(np.nan)
                    rsi_sell_price.append(np.nan)
                    rsi_signal.append(0)
            elif rsi[i - 1] < 70 and rsi[i] > 70:
                if signal != -1:
                    rsi_buy_price.append(np.nan)
                    rsi_sell_price.append(data[i])
                    signal = -1
                    rsi_signal.append(signal)
                else:
                    rsi_buy_price.append(np.nan)
                    rsi_sell_price.append(np.nan)
                    rsi_signal.append(0)
            else:
                rsi_buy_price.append(np.nan)
                rsi_sell_price.append(np.nan)
                rsi_signal.append(0)
                
        return rsi_buy_price, rsi_sell_price

    def implement_macd(data, data_macd) -> tuple:    
        macd_buy_price = []
        macd_sell_price = []
        macd_signal = []
        signal = 0

        for i in range(len(data_macd)):
            if data_macd['macd'][i] > data_macd['signal'][i]:
                if signal != 1:
                    macd_buy_price.append(data[i])
                    macd_sell_price.append(np.nan)
                    signal = 1
                    macd_signal.append(signal)
                else:
                    macd_buy_price.append(np.nan)
                    macd_sell_price.append(np.nan)
                    macd_signal.append(0)
            elif data_macd['macd'][i] < data_macd['signal'][i]:
                if signal != -1:
                    macd_buy_price.append(np.nan)
                    macd_sell_price.append(data[i])
                    signal = -1
                    macd_signal.append(signal)
                else:
                    macd_buy_price.append(np.nan)
                    macd_sell_price.append(np.nan)
                    macd_signal.append(0)
            else:
                macd_buy_price.append(np.nan)
                macd_sell_price.append(np.nan)
                macd_signal.append(0)
                
        return macd_buy_price, macd_sell_price
    
    def implement_bollinger(data, lower_bb, upper_bb) -> tuple:
        bollinger_buy_price = []
        bollinger_sell_price = []
        bollinger_signal = []
        signal = 0
        
        for i in range(len(data)):
            if data[i - 1] > lower_bb[i - 1] and data[i] < lower_bb[i]:
                if signal != 1:
                    bollinger_buy_price.append(data[i])
                    bollinger_sell_price.append(np.nan)
                    signal = 1
                    bollinger_signal.append(signal)
                else:
                    bollinger_buy_price.append(np.nan)
                    bollinger_sell_price.append(np.nan)
                    bollinger_signal.append(0)
            elif data[i - 1] < upper_bb[i - 1] and data[i] > upper_bb[i]:
                if signal != -1:
                    bollinger_buy_price.append(np.nan)
                    bollinger_sell_price.append(data[i])
                    signal = -1
                    bollinger_signal.append(signal)
                else:
                    bollinger_buy_price.append(np.nan)
                    bollinger_sell_price.append(np.nan)
                    bollinger_signal.append(0)
            else:
                bollinger_buy_price.append(np.nan)
                bollinger_sell_price.append(np.nan)
                bollinger_signal.append(0)
                
        return bollinger_buy_price, bollinger_sell_price

    def implement_donchian(data, upper_channel, lower_channel) -> tuple:
        donchian_buy_price = []
        donchian_sell_price = []
        donchian_signal = []
        signal = 0

        for i in range(len(data)):
            if data[i] > upper_channel[i - 1] and data[i - 1] <= upper_channel[i - 1]:
                if signal != 1:
                    donchian_buy_price.append(data[i])
                    donchian_sell_price.append(np.nan)
                    signal = 1
                    donchian_signal.append(signal)
                else:
                    donchian_buy_price.append(np.nan)
                    donchian_sell_price.append(np.nan)
                    donchian_signal.append(0)
            elif data[i] < lower_channel[i - 1] and data[i - 1] >= lower_channel[i - 1]:
                if signal != -1:
                    donchian_buy_price.append(np.nan)
                    donchian_sell_price.append(data[i])
                    signal = -1
                    donchian_signal.append(signal)
                else:
                    donchian_buy_price.append(np.nan)
                    donchian_sell_price.append(np.nan)
                    donchian_signal.append(0)
            else:
                donchian_buy_price.append(np.nan)
                donchian_sell_price.append(np.nan)
                donchian_signal.append(0)

        return donchian_buy_price, donchian_sell_price
