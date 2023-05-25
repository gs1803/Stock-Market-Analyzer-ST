import bs4 as bs
import datetime as dt
import pandas as pd
import requests
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

class StandardPoorCorr:
    def save_sp500_tickers() -> list:
        resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})

        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            ticker = ticker[:-1]
            if "." in ticker:
                ticker = ticker.replace('.', '-')
            tickers.append(ticker)

        return tickers

    def get_data_from_yahoo() -> None:
        tickers = StandardPoorCorr.save_sp500_tickers()

        start = dt.datetime(2015, 1, 1)
        end = dt.datetime(2022, 12, 31)

        dfs = []
        for ticker in tickers:
            df = yf.download(ticker, start, end, progress = False)
            df.rename(columns = {'Adj Close': ticker}, inplace = True)
            df.drop(columns = ['Open' ,'High', 'Low', 'Close', 'Volume'], axis = 1, inplace = True)
            dfs.append(df)

        main_df = pd.concat(dfs, axis = 1)
        main_df.to_csv('sp500_joined_closes.csv')

    def visualize_data() -> None:
        df = pd.read_csv('sp500_joined_closes.csv')
        df_corr = df.corr(numeric_only = True)
        data = df_corr.values

        fig = go.Figure(data = go.Heatmap(
            z = data,
            x = df_corr.columns,
            y = df_corr.index,
            hovertemplate = 'Stock 1: %{y}<br>Stock 2: %{x}<br>Correlation: %{z}<extra></extra>',
            colorscale = 'RdYlGn',
            zmin = -1,
            zmax = 1)
        )

        fig.update_layout(
            autosize = False,
            width = 1000,
            height = 1000,
            xaxis = dict(ticktext = [], tickvals = []),
            yaxis = dict(autorange = 'reversed', ticktext = [], tickvals = [])
        )

        st.plotly_chart(fig)
