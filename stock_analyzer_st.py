import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import pytz
from datetime import datetime
from millify import millify
from plotly.subplots import make_subplots
from technical_analysis_st import TechnicalAnalysis

class StockAnalyzer:
    def __init__(self, stock, titleStock) -> None:
        self.stock = stock
        self.titleStock = titleStock
        try:
            self.companyStock = yf.Ticker(titleStock).info['longName']
            self.mktCap = yf.Ticker(titleStock).info['marketCap']
        except:
            self.companyStock = ('')
            if self.titleStock == '^GSPC':
                self.companyStock = 'S&P500'
            if self.titleStock == '^DJI':
                self.companyStock = 'Dow Jones Industrial Average'
            if self.titleStock == '^RUT':
                self.companyStock = 'Russell 2000'
            if self.titleStock == '^IXIC':
                self.companyStock = 'NASDAQ Composite'
            self.companyStock = ('')
            self.mktCap = ('')
        self.dayStock = yf.download(titleStock, period = '3d', progress = False)
        self.etNow = datetime.now(pytz.timezone('US/Eastern')).date()
        
    def stock_prices(self) -> None:
        fig = make_subplots(specs = [[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Open'], name = 'Open'),
                                 secondary_y = False)
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Adj Close'], name = 'Adj Close'),
                                 secondary_y = False)
        fig.update_layout(title = f"Stock Price for {self.titleStock} ({self.companyStock})",
                          yaxis = dict(title = 'Price'))
        
        priceCol1, priceCol2, mktCapCol = st.columns([3.25, 3.75, 3])
        priceCol1.metric(label = f"Latest Stock Open Price ({self.dayStock.index[-1].date()}):", 
                         value = f"{self.dayStock['Open'].iloc[-1]:.2f}", 
                         delta = f"{self.dayStock['Open'].iloc[-1] - self.dayStock['Open'].iloc[-2]:.2f} From Previous Day")
        priceCol2.metric(label = f"Latest Stock Adj Close Price ({self.dayStock.index[-1].date()}):", 
                         value = f"{self.dayStock['Adj Close'].iloc[-1]:.2f}", 
                         delta = f"{self.dayStock['Adj Close'].iloc[-1] - self.dayStock['Adj Close'].iloc[-2]:.2f} From Previous Day")
        try:
            mktCapCol.metric(label = f"Latest Market Cap ({self.dayStock.index[-1].date()}):", 
                             value = f"{millify(self.mktCap, precision = 5)}")
        except:
            pass
        st.plotly_chart(fig, use_container_width = True)

    def stock_volume(self) -> None:
        fig = go.Figure(data = go.Scatter(x = self.stock.index, 
                                          y = self.stock['Volume'], 
                                          mode = 'lines'))
        fig.update_layout(title = f"Volume of Stock Traded of {self.titleStock} ({self.companyStock})",
                          yaxis = dict(title = 'Volume'))
        st.metric(label = f"Latest Stock Volume ({self.dayStock.index[-1].date()}):", 
                  value = f"{self.dayStock['Volume'].iloc[-1]:,.2f}", 
                  delta = f"{self.dayStock['Volume'].iloc[-1] - self.dayStock['Volume'].iloc[-2]:,.2f} From Previous Day")
        st.plotly_chart(fig, use_container_width = True)

    def stock_trading_value(self) -> None:
        self.stock['Trad_Val'] = self.stock['Adj Close'] * self.stock['Volume']
        self.dayStock['Trad_Val'] = self.dayStock['Adj Close'] * self.dayStock['Volume']
        fig = go.Figure(data = go.Scatter(x = self.stock.index, 
                                          y = self.stock['Trad_Val'], 
                                          mode = 'lines'))
        fig.update_layout(title = f"Trading Value for {self.titleStock} ({self.companyStock})",
                          yaxis = dict(title = 'Trading Value'))
        st.metric(label = f"Latest Stock Trading Value ({self.dayStock.index[-1].date()}):", 
                  value = f"{self.dayStock['Trad_Val'].iloc[-1]:,.2f}", 
                  delta = f"{self.dayStock['Trad_Val'].iloc[-1] - self.dayStock['Trad_Val'].iloc[-2]:,.2f} From Previous Day")
        st.plotly_chart(fig, use_container_width = True)
    
    def stock_volatility(self) -> None:
        self.stock['returns'] = (self.stock['Adj Close'] / self.stock['Adj Close'].shift(1)) - 1
        dateRange = (self.stock.index[-1] - self.stock.index[0]).days
        volCol1, volCol2, volCol3 = st.columns([3.33, 3.33, 3.33])

        if dateRange < 1 and self.stock.index[-1].date() == self.etNow:
            datePeriod = st.select_slider("Select a Date Period:", ['1d', '5d', '10d', '1mo', '3mo', '6mo', 
                                                                    '1y', '2y', '5y', '10y', 'YTD', 'MAX'])
            yearStock = yf.download(self.titleStock, period = datePeriod, progress = False)
            yearStock['returns'] = (yearStock['Adj Close'] / yearStock['Adj Close'].shift(1)) - 1
            if datePeriod == '1d':
                dailyVolatility = np.std(self.stock['returns'])
            else:
                dailyVolatility = np.std(yearStock['returns'])

            monthlyReturns = yearStock['Adj Close'].resample('M').ffill().pct_change()
            monthlyVolatility = np.std(monthlyReturns)
            annualReturns = yearStock['Adj Close'].resample('Y').ffill().pct_change()
            annualVolatility = np.std(annualReturns)

            volCol1.metric(label = f"Latest Daily Volatility ({datePeriod} Period):", 
                           value = f"{dailyVolatility * 100:,.2f}%", 
                           delta = ' ')
            if datePeriod != '1d' and datePeriod != '5d' and datePeriod != '10d' and datePeriod != '1mo':
                volCol2.metric(label = f"Latest Monthly Volatility ({datePeriod} Period):", 
                               value = f"{monthlyVolatility * 100:,.2f}%", 
                               delta = ' ')
            if datePeriod != '1d' and datePeriod != '5d' and datePeriod != '10d' and datePeriod != '1mo'\
                and datePeriod != '3mo' and datePeriod != '6mo'and datePeriod != '1y' and datePeriod != 'YTD':
                volCol3.metric(label = f"Latest Annual Volatility ({datePeriod} Period):",
                               value = f"{annualVolatility * 100:,.2f}%", 
                               delta = ' ')
        else:
            dailyVolatility = np.std(self.stock['returns'])
            monthlyReturns = self.stock['Adj Close'].resample('M').ffill().pct_change()
            monthlyVolatility = np.std(monthlyReturns)
            annualReturns = self.stock['Adj Close'].resample('Y').ffill().pct_change()
            annualVolatility = np.std(annualReturns)

            volCol1.metric(label = f"Daily Volatility (Selected Range):", 
                           value = f"{dailyVolatility * 100:,.2f}%", 
                           delta = ' ')
            if dateRange > 30:
                volCol2.metric(label = f"Monthly Volatility (Selected Range):", 
                               value = f"{monthlyVolatility * 100:,.2f}%", 
                               delta = ' ')
            if dateRange > 365:
                volCol3.metric(label = f"Annual Volatility (Selected Range):",
                               value = f"{annualVolatility * 100:,.2f}%", 
                               delta = ' ')
        
        fig = go.Figure(data = go.Histogram(x = self.stock['returns'], nbinsx = 100))
        fig.update_layout(title = f"Volatility of {self.titleStock} ({self.companyStock})")
        st.plotly_chart(fig, use_container_width = True)

    def stock_candlestick_graph(self) -> None:
        fig = make_subplots(rows = 2, cols = 1, 
                            shared_xaxes = True, 
                            vertical_spacing = 0.1, 
                            row_heights = [0.75, 0.25])
        
        fig.add_trace(
            go.Candlestick(x = self.stock.index, 
                           open = self.stock['Open'], 
                           high = self.stock['High'],
                           low = self.stock['Low'], 
                           close = self.stock['Close'],
                           showlegend = False, name = ''),
            row = 1, col = 1)
        
        fig.add_trace(
            go.Bar(x = self.stock.index, 
                   y = self.stock['Volume'],
                   marker_color = 'red',
                   showlegend = False, name = ''),
            row = 2, col = 1)
              
        fig.update_layout(title = f"Candlestick Graph for {self.titleStock} ({self.companyStock})",
                          yaxis = dict(title = 'Price'),
                          yaxis2 = dict(title = 'Volume'))
        fig.update_layout(xaxis_rangeslider_visible = False)
        st.plotly_chart(fig, use_container_width = True)

    def stock_moving_average(self) -> None:
        fig = make_subplots(specs = [[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Open'], name = 'Open'),
                                 secondary_y = False)
        
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Adj Close'], name = 'Adj Close'),
                                 secondary_y = False)
        
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Adj Close'].rolling(50).mean(), name = '50 Days MA'),
                                 secondary_y = False)
        
        fig.add_trace(go.Scatter(x = self.stock.index, 
                                 y = self.stock['Adj Close'].rolling(200).mean(), name = '200 Days MA'), 
                                 secondary_y = False)
                
        fig.update_layout(title = f"Moving Average for {self.titleStock} ({self.companyStock})",
                          yaxis = dict(title = 'Price'))
        st.plotly_chart(fig, use_container_width = True)

    def stock_rsi(self) -> None:
        self.stock['rsi_14'] = TechnicalAnalysis.rsi_calculation(self.stock['Adj Close'], 14)
        rsi_buy_price, rsi_sell_price = TechnicalAnalysis.implement_rsi(self.stock['Adj Close'], self.stock['rsi_14'])
        fig = make_subplots(rows = 2, cols = 1, 
                            shared_xaxes = True, 
                            vertical_spacing = 0.1, 
                            row_heights = [0.75, 0.25])

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['Adj Close'],
            mode = 'lines',
            name = 'Adj Close Price',
            showlegend = False
        ), row = 1, col = 1)

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = rsi_buy_price,
            mode = 'markers',
            marker = dict(symbol = 'triangle-up', size = 20, color = 'green'),
            name = 'Buy Signal'
        ), row = 1, col = 1)

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = rsi_sell_price,
            mode = 'markers',
            marker = dict(symbol = 'triangle-down', size = 20, color = 'red'),
            name = 'Sell Signal'
        ), row = 1, col = 1)

        fig.update_layout(
            title = f'RSI Trade Signals for {self.titleStock} ({self.companyStock})',
            yaxis = dict(title = 'Adj Close Price'),
            yaxis2 = dict(title = 'RSI'),
        )

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['rsi_14'],
            mode = 'lines',
            name = 'RSI',
            line = dict(color = 'orange', width = 1.5),
            yaxis = 'y2',
            showlegend = False
        ), row = 2, col = 1)

        fig.add_shape(type = 'line', x0 = self.stock.index[0], x1 = self.stock.index[-1], y0 = 30, y1 = 30,
                      line = dict(color = 'green', width = 1, dash = 'dash'), yref = 'y2', row = 2, col = 1)
        fig.add_shape(type = 'line', x0 = self.stock.index[0], x1 = self.stock.index[-1], y0 = 70, y1 = 70,
                      line = dict(color = 'red', width = 1, dash='dash'), yref = 'y2', row = 2, col = 1)
        st.plotly_chart(fig, use_container_width = True)

    def stock_macd(self) -> None:
        df_macd = TechnicalAnalysis.macd_calculations(self.stock['Adj Close'], 26, 12, 9)
        macd_buy_price, macd_sell_price = TechnicalAnalysis.implement_macd(self.stock['Adj Close'], df_macd)        
        fig = make_subplots(rows = 2, cols = 1, 
                            shared_xaxes = True, 
                            vertical_spacing = 0.1, 
                            row_heights = [0.75, 0.25])
        
        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['Adj Close'],
            mode = 'lines',
            name = 'Adj Close Price',
            showlegend = False
        ), row = 1, col = 1)

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = macd_buy_price,
            mode = 'markers',
            marker = dict(symbol = 'triangle-up', size = 20, color = 'green'),
            name = 'Buy Signal'
        ), row = 1, col = 1)

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = macd_sell_price,
            mode = 'markers',
            marker = dict(symbol = 'triangle-down', size = 20, color = 'red'),
            name = 'Sell Signal'
        ), row = 1, col = 1)

        fig.add_trace(go.Scatter(
            x = df_macd.index,
            y = df_macd['macd'],
            mode = 'lines',
            name = 'MACD',
            line = dict(color = 'blue'),
            showlegend = False
        ), row = 2, col = 1)

        fig.add_trace(go.Scatter(
            x = df_macd.index,
            y = df_macd['signal'],
            mode = 'lines',
            name = 'MACD Signal',
            line = dict(color = 'orange', dash = 'dash'),
            showlegend = False
        ), row = 2, col = 1)

        c = ['red' if cl < 0 else 'green' for cl in df_macd['hist']]
        fig.add_trace(go.Bar(
            x = df_macd.index,
            y = df_macd['hist'],
            marker = dict(color = c),
            name = 'Histogram',
            showlegend = False
        ), row = 2, col = 1)

        fig.update_layout(
            title = f'MACD Trade Signals for {self.titleStock} ({self.companyStock})',
            yaxis = dict(title = 'Adj Close Price'),
            yaxis2 = dict(title = 'MACD')
        )
        st.plotly_chart(fig, use_container_width = True)

    def stock_bollinger(self) -> None:
        self.stock['sma_20'] = TechnicalAnalysis.sma_calculations(self.stock['Adj Close'], 20)
        self.stock['upper_bb'], self.stock['lower_bb'] = TechnicalAnalysis.bollinger_bands_calculations(self.stock['Adj Close'], self.stock['sma_20'], 20)
        bollingerBuyPrice, bollingerSellPrice = TechnicalAnalysis.implement_bollinger(self.stock['Adj Close'], self.stock['lower_bb'], self.stock['upper_bb'])
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['Adj Close'],
            mode = 'lines',
            name = 'Adj Close Price',
            showlegend = False
        ))
    
        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['upper_bb'],
            mode = 'lines',
            name = 'Upper Band',
            line = dict(color = '#ffa8b5', dash = 'dash'),
            showlegend = False
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['sma_20'],
            mode = 'lines',
            name = 'Middle Band',
            line = dict(color = '#808080', dash = 'dash'),
            showlegend = False
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['lower_bb'],
            mode = 'lines',
            name = 'Lower Band',
            line = dict(color = '#ffa8b5', dash = 'dash'),
            showlegend = False
        ))

        fig.update_layout(
            title = f'Bollinger Bands Trade Signals for {self.titleStock} ({self.companyStock})',
            yaxis = dict(title = 'Adj Close Price')
        )

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = bollingerBuyPrice,
            mode = 'markers',
            marker = dict(symbol = 'triangle-up', size = 20, color = 'green'),
            name = 'Buy Signal'
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = bollingerSellPrice,
            mode = 'markers',
            marker = dict(symbol = 'triangle-down', size = 20, color = 'red'),
            name = 'Sell Signal'
        ))
        st.plotly_chart(fig, use_container_width = True)

    def stock_donchian(self) -> None:
        self.stock['upper_db'], self.stock['lower_db'] = TechnicalAnalysis.donchian_breakout_calculations(self.stock['Adj Close'],
                                                                                                          self.stock['High'],
                                                                                                          self.stock['Low'], 20)
        donchianBuyPrice, donchianSellPrice = TechnicalAnalysis.implement_donchian(self.stock['Adj Close'], 
                                                                                   self.stock['upper_db'], 
                                                                                   self.stock['lower_db'])
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['Adj Close'],
            mode = 'lines',
            name = 'Adj Close Price',
            showlegend = False
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['upper_db'],
            mode = 'lines',
            name = 'Upper Channel',
            line = dict(color = '#ffa8b5', dash = 'dash'),
            showlegend = False
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = self.stock['lower_db'],
            mode = 'lines',
            name = 'Lower Channel',
            line = dict(color = '#ffa8b5', dash = 'dash'),
            showlegend = False
        ))

        fig.update_layout(
            title = f'Donchian Breakout Trade Signals for {self.titleStock} ({self.companyStock})',
            yaxis = dict(title = 'Adj Close Price')
        )

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = donchianBuyPrice,
            mode = 'markers',
            marker = dict(symbol = 'triangle-up', size = 20, color = 'green'),
            name = 'Buy Signal'
        ))

        fig.add_trace(go.Scatter(
            x = self.stock.index,
            y = donchianSellPrice,
            mode = 'markers',
            marker = dict(symbol = 'triangle-down', size = 20, color = 'red'),
            name = 'Sell Signal'
        ))
        st.plotly_chart(fig, use_container_width = True)

    def graph_chooser(self) -> None:
        graphOptions = {
            'Prices': self.stock_prices,
            'Volume': self.stock_volume,
            'Trading Value': self.stock_trading_value,
            'Volatility': self.stock_volatility,
            'Candlestick Graph': self.stock_candlestick_graph,
            'Moving Average': self.stock_moving_average,
            'RSI Strategy': self.stock_rsi,
            'MACD Strategy': self.stock_macd,
            'Bollinger Bands Strategy': self.stock_bollinger,
            'Donchian Breakout Strategy': self.stock_donchian}

        graphOptionList = list(graphOptions.keys())
        graphTab1, graphTab2 = st.tabs(['Information Graphs', 'Technical Analysis Graphs'])
        selectedGraphOption1 = graphTab1.selectbox("Select an option:", graphOptionList[0:5])
        selectedGraphOption2 = graphTab2.selectbox("Select an option:", graphOptionList[5:10])

        with graphTab1:
            selectedGraphFunction1 = graphOptions.get(selectedGraphOption1)
            selectedGraphFunction1()

        with graphTab2:
            selectedGraphFunction2 = graphOptions.get(selectedGraphOption2)
            selectedGraphFunction2()
