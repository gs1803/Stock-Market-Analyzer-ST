import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fredapi import Fred

fred = Fred(api_key = st.secrets['API_KEY'])

class USEconomy:
    inflationData = fred.get_series('CPIAUCSL', units = 'pc1', observation_start = '1/1/1970')
    coreInflationData = fred.get_series('CPILFESL', units = 'pc1', observation_start = '1/1/1970')
    unemploymentData = fred.get_series('UNRATE', observation_start = '1/1/1970')
    marketYieldUSTres1Data = fred.get_series('DGS1', observation_start = '1/1/1970')
    marketYieldUSTres10Data = fred.get_series('DGS10', observation_start = '1/1/1970')
    fedFundEffecRateData = fred.get_series('DFF', observation_start = '1/1/1970')
    sofrData = fred.get_series('SOFR', observation_start = '3/4/2018')
    sofr30Data = fred.get_series('SOFR30DAYAVG', observation_start = '2/5/2018')
    sofr90Data = fred.get_series('SOFR90DAYAVG', observation_start = '2/5/2018')
    sofr180Data = fred.get_series('SOFR180DAYAVG', observation_start = '2/5/2018')
    mortgage15Data = fred.get_series('MORTGAGE15US', observation_start = '1/1/1992')
    mortgage30Data = fred.get_series('MORTGAGE30US', observation_start = '1/1/1992')

    def inflation_rate() -> None:
        inflationOption = st.radio("Select an option:", ['Inflation Rate', 'Core Inflation Rate'])

        if inflationOption == 'Inflation Rate':
            inflationDf = pd.DataFrame(USEconomy.inflationData).dropna(how = 'all')
            inflationDf.index = pd.to_datetime(inflationDf.index)
            inflationDf.columns = ['inflation_rate']

            fig = go.Figure(data = go.Scatter(x = inflationDf.index, y = inflationDf['inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Inflation Rate')
            st.metric(label = f"Latest Inflation Rate ({inflationDf.index[-1].strftime('%Y-%m')}):", 
                      value = f"{inflationDf['inflation_rate'].iloc[-1]:.3f}%", 
                      delta = f"{inflationDf['inflation_rate'].iloc[-1] - inflationDf['inflation_rate'].iloc[-2]:.3f} From Previous Month",
                      delta_color = 'inverse')
            st.plotly_chart(fig, use_container_width = True)
        if inflationOption == 'Core Inflation Rate':
            coreInflationDf = pd.DataFrame(USEconomy.coreInflationData).dropna(how = 'all')
            coreInflationDf.index = pd.to_datetime(coreInflationDf.index)
            coreInflationDf.columns = ['core_inflation_rate']
            fig = go.Figure(data = go.Scatter(x = coreInflationDf.index, y = coreInflationDf['core_inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Core Inflation Rate')
            st.metric(label = f"Latest Core Inflation Rate ({coreInflationDf.index[-1].strftime('%Y-%m')}):", 
                      value = f"{coreInflationDf['core_inflation_rate'].iloc[-1]:.3f}%", 
                      delta = f"{coreInflationDf['core_inflation_rate'].iloc[-1] - coreInflationDf['core_inflation_rate'].iloc[-2]:.3f} From Previous Month",
                      delta_color = 'inverse')
            st.plotly_chart(fig, use_container_width = True)

    def unemployment_rate() -> None:
        unemploymentDf = pd.DataFrame(USEconomy.unemploymentData).dropna(how = 'all')
        unemploymentDf.index = pd.to_datetime(unemploymentDf.index)
        unemploymentDf.columns = ['unemployment_rate']
        
        unempStateDf = fred.search('unemployment rate state', filter = ('frequency', 'Monthly'))
        unempStateDf = unempStateDf.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
        unempStateDf = unempStateDf.loc[unempStateDf['title'].str.startswith('Unemployment Rate in')]
        unempStateDf = unempStateDf[~unempStateDf['title'].str.contains(',')]
        unempStateDf = unempStateDf[~unempStateDf['title'].str.contains('Region')]

        cleanUnempStateDf = unempStateDf[['id', 'title']].reset_index(drop = True)
        cleanUnempStateDf['title'] = [t.replace('Unemployment Rate in ', '').title() for t in cleanUnempStateDf['title']]
        cleanUnempStateDf = cleanUnempStateDf.sort_values(['title']).reset_index(drop = True)
        cleanUnempStateDf = cleanUnempStateDf.rename(columns = {'title': 'name'})

        unemCol1, unemCol2 = st.tabs(['Total Unemployment Rate', 'Unemployment Rate by State'])
        with unemCol1:
            fig = go.Figure(data = go.Scatter(x = unemploymentDf.index, y = unemploymentDf['unemployment_rate']))
            fig.update_layout(xaxis_title = 'Date',
                              title = 'Unemployment Rate')
            st.metric(label = f"Latest Unemployment Rate ({unemploymentDf.index[-1].strftime('%Y-%m')}):", 
                      value = f"{unemploymentDf['unemployment_rate'].iloc[-1]:.3f}%", 
                      delta = f"{unemploymentDf['unemployment_rate'].iloc[-1] - unemploymentDf['unemployment_rate'].iloc[-2]:.3f} From Previous Month",
                      delta_color = 'inverse')
            st.plotly_chart(fig, use_container_width = True)
        
        with unemCol2:
            selectedName = st.selectbox('Select a State:', cleanUnempStateDf['name'])
            selectedID = cleanUnempStateDf.loc[cleanUnempStateDf['name'] == selectedName, 'id'].values[0]

            stateData = fred.get_series(f'{selectedID}', observation_start = '1/1/1975')
            stateUnemploymentDf = pd.DataFrame(stateData).dropna(how = 'all')
            stateUnemploymentDf.index = pd.to_datetime(stateUnemploymentDf.index)
            stateUnemploymentDf.columns = ['sa_unemployment_rate']

            figState = go.Figure(data = go.Scatter(x = stateUnemploymentDf.index, y = stateUnemploymentDf['sa_unemployment_rate']))
            figState.update_layout(xaxis_title = 'Date',
                                   title = f'Unemployment Rate in {selectedName}')
            st.metric(label = f"Latest Unemployment Rate in {selectedName} ({stateUnemploymentDf.index[-1].strftime('%Y-%m')}):", 
                      value = f"{stateUnemploymentDf['sa_unemployment_rate'].iloc[-1]:.3f}%", 
                      delta = f"{stateUnemploymentDf['sa_unemployment_rate'].iloc[-1] - stateUnemploymentDf['sa_unemployment_rate'].iloc[-2]:.3f} From Previous Month",
                      delta_color = 'inverse')
            st.plotly_chart(figState, use_container_width = True)
    
    def interest_rates() -> None:
        interestOption = st.radio("Select an option:", ['Federal Funds Effective Rate', 
                                                        'Market Yield on U.S. Treasury Securities', 
                                                        'Secured Overnight Financing Rate'])
        
        if interestOption == 'Federal Funds Effective Rate':
            fferDf = pd.DataFrame(USEconomy.fedFundEffecRateData).dropna(how = 'all')
            fferDf.index = pd.to_datetime(fferDf.index)
            fferDf.columns = ['ffer']
            fig = go.Figure(data = go.Scatter(x = fferDf.index, y = fferDf['ffer']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Federal Funds Effective Rate')
            st.metric(label = f"Latest Federal Funds Effective Rate ({fferDf.index[-1].date()}):", 
                      value = f"{fferDf['ffer'].iloc[-1]:.2f}%", 
                      delta = f"{fferDf['ffer'].iloc[-1] - fferDf['ffer'].iloc[-2]:.2f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

        if interestOption == 'Market Yield on U.S. Treasury Securities':
            mktYieldTres1Df = pd.DataFrame(USEconomy.marketYieldUSTres1Data).dropna(how = 'all')
            mktYieldTres1Df.index = pd.to_datetime(mktYieldTres1Df.index)
            mktYieldTres1Df.columns = ['myuts1']
            
            mktYieldTres10Df = pd.DataFrame(USEconomy.marketYieldUSTres10Data).dropna(how = 'all')
            mktYieldTres10Df.index = pd.to_datetime(mktYieldTres10Df.index)
            mktYieldTres10Df.columns = ['myuts10']

            mktYieldCol1, mktYieldCol2 = st.columns([5, 5])
            fig = make_subplots(specs = [[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x = mktYieldTres1Df.index, y = mktYieldTres1Df['myuts1'], name = '1 Year'))
            fig.add_trace(go.Scatter(x = mktYieldTres10Df.index, y = mktYieldTres10Df['myuts10'], name = '10 Year'))

            fig.update_layout(title = 'Market Yield on U.S. Treasury Securities Rate',
                              yaxis = dict(title = 'Rate'),
                              xaxis = dict(title = 'Date'))
            
            mktYieldCol1.metric(label = f"Latest Market Yield (1 Year) Rate ({mktYieldTres1Df.index[-1].date()}):", 
                                value = f"{mktYieldTres1Df['myuts1'].iloc[-1]:.2f}%", 
                                delta = f"{mktYieldTres1Df['myuts1'].iloc[-1] - mktYieldTres1Df['myuts1'].iloc[-2]:.2f} From Previous Day")
            mktYieldCol2.metric(label = f"Latest Market Yield (10 Year) Rate ({mktYieldTres10Df.index[-1].date()}):", 
                                value = f"{mktYieldTres10Df['myuts10'].iloc[-1]:.2f}%", 
                                delta = f"{mktYieldTres10Df['myuts10'].iloc[-1] - mktYieldTres10Df['myuts10'].iloc[-2]:.2f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

        if interestOption == 'Secured Overnight Financing Rate':
            sofrDf = pd.DataFrame(USEconomy.sofrData).dropna(how = 'all')
            sofrDf.index = pd.to_datetime(sofrDf.index)
            sofrDf.columns = ['sofr']
            
            sofr30Df = pd.DataFrame(USEconomy.sofr30Data).dropna(how = 'all')
            sofr30Df.index = pd.to_datetime(sofr30Df.index)
            sofr30Df.columns = ['sofr30']

            sofr90Df = pd.DataFrame(USEconomy.sofr90Data).dropna(how = 'all')
            sofr90Df.index = pd.to_datetime(sofr90Df.index)
            sofr90Df.columns = ['sofr90']

            sofr180Df = pd.DataFrame(USEconomy.sofr180Data).dropna(how = 'all')
            sofr180Df.index = pd.to_datetime(sofr180Df.index)
            sofr180Df.columns = ['sofr180']

            fig = go.Figure(data = go.Scatter(x = sofrDf.index, y = sofrDf['sofr']))

            fig.update_layout(xaxis_title = 'Date', 
                              title = 'Secured Overnight Financing Rate')
            sofrCol1, sofrCol2, sofrCol3, sofrCol4 = st.columns([4, 2, 2, 2])
            sofrCol1.metric(label = f"Latest SOFR ({sofrDf.index[-1].date()}):", 
                            value = f"{sofrDf['sofr'].iloc[-1]:.2f}%", 
                            delta = f"{sofrDf['sofr'].iloc[-1] - sofrDf['sofr'].iloc[-2]:.2f} From Previous Day")
            sofrCol2.metric(label = '30-day Average:', 
                            value = f"{sofr30Df['sofr30'].iloc[-1]:.2f}%", 
                            delta = f"{sofr30Df['sofr30'].iloc[-1] - sofr30Df['sofr30'].iloc[-2]:.2f}")
            sofrCol3.metric(label = '90-day Average:', 
                            value = f"{sofr90Df['sofr90'].iloc[-1]:.2f}%", 
                            delta = f"{sofr90Df['sofr90'].iloc[-1] - sofr90Df['sofr90'].iloc[-2]:.2f}")
            sofrCol4.metric(label = '180-day Average:', 
                            value = f"{sofr180Df['sofr180'].iloc[-1]:.2f}%", 
                            delta = f"{sofr180Df['sofr180'].iloc[-1] - sofr180Df['sofr180'].iloc[-2]:.2f}")
            st.plotly_chart(fig, use_container_width = True)

    def exchange_rates() -> None:
        exchangeDf = fred.search('U.S. Dollar Spot Exchange Rate')
        exchangeDict = {}
        for _, row in exchangeDf.iterrows():
            if 'U.S. Dollar Spot Exchange Rate' in row['title']:
                if row['id'].startswith('D'):
                    newTitle = row['title'].replace(' Spot Exchange Rate', 's')
                    exchangeDict[newTitle] = row['id']

        exchangeCleanDf = pd.DataFrame([exchangeDict.values(), exchangeDict.keys()]).transpose()
        exchangeCleanDf.columns = ['id', 'name']
        isoCodeList = ['YEN', 'CNY', 'KRW', 'CAD', 'MXN', 'VEF', 'INR', 
                       'BRL', 'LKR', 'CHF', 'MYR', 'THB', 'ZAR', 'TWD', 
                       'HKD','NOK', 'DKK', 'SEK', 'SGD']
        exchangeCleanDf['iso_code'] = isoCodeList
        euroRate = {'id': 'DEXUSEU', 'name': 'Euro to U.S. Dollars', 'iso_code': 'EUR'}
        ukRate = {'id': 'DEXUSUK', 'name': 'Pound Sterling to U.S. Dollars', 'iso_code': 'GBP'}
        exchangeCleanDf = pd.concat([pd.DataFrame(ukRate, index = [0]), exchangeCleanDf]).reset_index(drop = True)
        exchangeCleanDf = pd.concat([pd.DataFrame(euroRate, index = [0]), exchangeCleanDf]).reset_index(drop = True)
        selectedName = st.selectbox('Select an exchange rate', exchangeCleanDf['name'])

        selectedId = exchangeCleanDf.loc[exchangeCleanDf['name'] == selectedName, 'id'].values[0]
        selectedDf = fred.get_series(selectedId, observation_start = '1/1/2015')
        selectedIso = exchangeCleanDf.loc[exchangeCleanDf['name'] == selectedName, 'iso_code'].values[0]
        
        if selectedName == 'Euro to U.S. Dollars' or selectedName == 'Pound Sterling to U.S. Dollars':
            usdModDf = pd.DataFrame(selectedDf).dropna(how = 'all')
            usdModDf.index = pd.to_datetime(usdModDf.index)
            usdModDf.columns = ['exchange_rate']
            usdModDf['exchange_rate'] = 1 / usdModDf['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdModDf.index, y = usdModDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Exchange Rate')
            st.metric(label = f"Latest {selectedName} ({usdModDf.index[-1].date()}):", 
                      value = f"{usdModDf['exchange_rate'].iloc[-1]:.3f} {selectedIso}", 
                      delta = f"{usdModDf['exchange_rate'].iloc[-1] - usdModDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

        else:
            usdDf = pd.DataFrame(selectedDf).dropna(how = 'all')
            usdDf.index = pd.to_datetime(usdDf.index)
            usdDf.columns = ['exchange_rate']

            fig = go.Figure(data = go.Scatter(x = usdDf.index, y = usdDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                            title = f'Exchange Rate')
            st.metric(label = f"Latest {selectedName} ({usdDf.index[-1].date()}):", 
                    value = f"{usdDf['exchange_rate'].iloc[-1]:.3f} {selectedIso}", 
                    delta = f"{usdDf['exchange_rate'].iloc[-1] - usdDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

    def mortgage_rates() -> None:
        mortgage15Df = pd.DataFrame(USEconomy.mortgage15Data).dropna(how = 'all')
        mortgage15Df.index = pd.to_datetime(mortgage15Df.index)
        mortgage15Df.columns = ['mort15']

        mortgage30Df = pd.DataFrame(USEconomy.mortgage30Data).dropna(how = 'all')
        mortgage30Df.index = pd.to_datetime(mortgage30Df.index)
        mortgage30Df.columns = ['mort30']

        fig = make_subplots(specs = [[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = mortgage30Df.index, y = mortgage30Df['mort30'], name = '30 Year Rate'))
        fig.add_trace(go.Scatter(x = mortgage15Df.index, y = mortgage15Df['mort15'], name = '15 Year Rate'))

        fig.update_layout(title = 'Fixed Mortgage Rates',
                          yaxis = dict(title = 'Rate'),
                          xaxis = dict(title = 'Date'))
        mortCol1, mortCol2 = st.columns([5, 5])
        mortCol1.metric(label = f"Latest 15 Year Fixed Rate ({mortgage15Df.index[-1].date()}):", 
                        value = f"{mortgage15Df['mort15'].iloc[-1]:.2f}%", 
                        delta = f"{mortgage15Df['mort15'].iloc[-1] - mortgage15Df['mort15'].iloc[-2]:.2f} From Previous Week")
        mortCol2.metric(label = f"Latest 30 Year Fixed Rate ({mortgage30Df.index[-1].date()}):", 
                        value = f"{mortgage30Df['mort30'].iloc[-1]:.2f}%", 
                        delta = f"{mortgage30Df['mort30'].iloc[-1] - mortgage30Df['mort30'].iloc[-2]:.2f} From Previous Week")
        st.plotly_chart(fig, use_container_width = True)
        
    def economy_chooser() -> None:
        economyOptions = {'Inflation Rate': USEconomy.inflation_rate,
                          'Unemployment Rate': USEconomy.unemployment_rate,
                          'Interest Rates': USEconomy.interest_rates,
                          'Exchange Rates': USEconomy.exchange_rates,
                          'Mortgage Rates': USEconomy.mortgage_rates}

        economyOptionList = list(economyOptions.keys())
        selectedEconomyOption = st.selectbox("Select an option", economyOptionList)

        selectedEconomyFunction = economyOptions.get(selectedEconomyOption)
        if selectedEconomyFunction:
            selectedEconomyFunction()
     
