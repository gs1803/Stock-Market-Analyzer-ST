import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fredapi import Fred

fred = Fred(api_key = st.secrets['API_KEY'])

class USEconomy:
    inflationData = fred.get_series('CPIAUCSL', units = 'pc1', observation_start = '1/1/1970')
    coreInflationData = fred.get_series('CPILFESL', units = 'pc1', observation_start = '1/1/1970')
    unemploymentData = fred.get_series('UNRATE', observation_start = '1/1/1970')
    exchangeDataUsdEuro = fred.get_series('DEXUSEU', observation_start = '1/1/2015')
    exchangeDataUsdCad = fred.get_series('DEXCAUS', observation_start = '1/1/2015')
    exchangeDataUsdInr = fred.get_series('DEXINUS', observation_start = '1/1/2015')
    exchangeDataUsdYen = fred.get_series('DEXJPUS', observation_start = '1/1/2015')
    exchangeDataUsdRmb = fred.get_series('DEXCHUS', observation_start = '1/1/2015')
    marketYieldUSTresData = fred.get_series('DGS10', observation_start = '1/1/1970')
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
            inflationDf = pd.DataFrame(USEconomy.inflationData)
            inflationDf.index = pd.to_datetime(inflationDf.index)
            inflationDf.columns = ['inflation_rate']
            fig = go.Figure(data = go.Scatter(x = inflationDf.index, y = inflationDf['inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Inflation Rate')
            st.subheader(f"Latest Inflation Rate: {inflationDf['inflation_rate'].iloc[-1]:.3f}%")
            st.plotly_chart(fig, use_container_width = True)
        elif inflationOption == 'Core Inflation Rate':
            coreInflationDf = pd.DataFrame(USEconomy.coreInflationData)
            coreInflationDf.index = pd.to_datetime(coreInflationDf.index)
            coreInflationDf.columns = ['core_inflation_rate']
            fig = go.Figure(data = go.Scatter(x = coreInflationDf.index, y = coreInflationDf['core_inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Core Inflation Rate')
            st.subheader(f"Latest Core Inflation Rate: {coreInflationDf['core_inflation_rate'].iloc[-1]:.3f}%")
            st.plotly_chart(fig, use_container_width = True)

    def unemployment_rate() -> None:
        unemploymentDf = pd.DataFrame(USEconomy.unemploymentData)
        unemploymentDf.index = pd.to_datetime(unemploymentDf.index)
        unemploymentDf.columns = ['unemployment_rate']
        fig = go.Figure(data = go.Scatter(x = unemploymentDf.index, y = unemploymentDf['unemployment_rate']))

        fig.update_layout(xaxis_title = 'Date',
                          title = 'Unemployment Rate')
        st.subheader(f"Latest Unemployment Rate: {unemploymentDf['unemployment_rate'].iloc[-1]:.3f}%")
        st.plotly_chart(fig, use_container_width = True)
    
    def interest_rates() -> None:
        interestOption = st.radio("Select an option:", ['Federal Funds Effective Rate', 
                                                        'Market Yield on U.S. Treasury Securities (10 Year)', 
                                                        'Secured Overnight Financing Rate'])
        
        if interestOption == 'Federal Funds Effective Rate':
            fferDf = pd.DataFrame(USEconomy.fedFundEffecRateData)
            fferDf.index = pd.to_datetime(fferDf.index)
            fferDf.columns = ['ffer']
            fig = go.Figure(data = go.Scatter(x = fferDf.index, y = fferDf['ffer']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Federal Funds Effective Rate')
            st.subheader(f"Latest Federal Funds Effective Rate: {fferDf['ffer'].iloc[-1]:.2f}%")
            st.plotly_chart(fig, use_container_width = True)

        if interestOption == 'Market Yield on U.S. Treasury Securities (10 Year)':
            sofrDf = pd.DataFrame(USEconomy.marketYieldUSTresData)
            sofrDf.index = pd.to_datetime(sofrDf.index)
            sofrDf.columns = ['myuts']
            fig = go.Figure(data = go.Scatter(x = sofrDf.index, y = sofrDf['myuts']))

            fig.update_layout(xaxis_title = 'Date', 
                              title = 'Market Yield on U.S. Treasury Securities (10 Year) Rate')
            st.subheader(f"Latest Market Yield on U.S. Treasury Securities (10 Year) Rate: {sofrDf['myuts'].iloc[-1]:.2f}%")
            st.plotly_chart(fig, use_container_width = True)

        if interestOption == 'Secured Overnight Financing Rate':
            sofrDf = pd.DataFrame(USEconomy.sofrData)
            sofrDf.index = pd.to_datetime(sofrDf.index)
            sofrDf.columns = ['sofr']
            
            sofr30Df = pd.DataFrame(USEconomy.sofr30Data)
            sofr30Df.index = pd.to_datetime(sofr30Df.index)
            sofr30Df.columns = ['sofr30']
            sofr30Df['30-day Arrow'] = np.where(sofr30Df['sofr30'] > sofr30Df['sofr30'].shift(), '▲', 
                                                np.where(sofr30Df['sofr30'] < sofr30Df['sofr30'].shift(), '▼', '▬'))
            arrowColor30 = np.where(sofr30Df['sofr30'] > sofr30Df['sofr30'].shift(), 'green', 
                                    np.where(sofr30Df['sofr30'] < sofr30Df['sofr30'].shift(), 'red', 'gray'))
            arrowHtml30 = [f'<span style="color:{color}">{arrow}</span>' for arrow, color in zip(sofr30Df['30-day Arrow'], arrowColor30)]
            sofr30Df['30-day Arrow'] = arrowHtml30

            sofr90Df = pd.DataFrame(USEconomy.sofr90Data)
            sofr90Df.index = pd.to_datetime(sofr90Df.index)
            sofr90Df.columns = ['sofr90']
            sofr90Df['90-day Arrow'] = np.where(sofr90Df['sofr90'] > sofr90Df['sofr90'].shift(), '▲', 
                                                np.where(sofr90Df['sofr90'] < sofr90Df['sofr90'].shift(), '▼', '▬'))
            arrowColor90 = np.where(sofr90Df['sofr90'] > sofr90Df['sofr90'].shift(), 'green', 
                                    np.where(sofr90Df['sofr90'] < sofr90Df['sofr90'].shift(), 'red', 'gray'))
            arrowHtml90 = [f'<span style="color:{color}">{arrow}</span>' for arrow, color in zip(sofr90Df['90-day Arrow'], arrowColor90)]
            sofr90Df['90-day Arrow'] = arrowHtml90

            sofr180Df = pd.DataFrame(USEconomy.sofr180Data)
            sofr180Df.index = pd.to_datetime(sofr180Df.index)
            sofr180Df.columns = ['sofr180']
            sofr180Df['180-day Arrow'] = np.where(sofr180Df['sofr180'] > sofr180Df['sofr180'].shift(), '▲', 
                                                  np.where(sofr180Df['sofr180'] < sofr180Df['sofr180'].shift(), '▼', '▬'))
            arrowColor180 = np.where(sofr180Df['sofr180'] > sofr180Df['sofr180'].shift(), 'green', 
                                     np.where(sofr180Df['sofr180'] < sofr180Df['sofr180'].shift(), 'red', 'gray'))
            arrowHtml180 = [f'<span style="color:{color}">{arrow}</span>' for arrow, color in zip(sofr180Df['180-day Arrow'], arrowColor180)]
            sofr180Df['180-day Arrow'] = arrowHtml180

            fig = go.Figure(data = go.Scatter(x = sofrDf.index, y = sofrDf['sofr']))

            fig.update_layout(xaxis_title = 'Date', 
                              title = 'Secured Overnight Financing Rate')
            st.subheader(f"Latest Secured Overnight Financing Rate: {sofrDf['sofr'].iloc[-1]:.2f}%")
            sofrCol1, sofrCol2, sofrCol3 = st.columns([3, 3, 3])
            sofrCol1.markdown(f"30-day Average: {sofr30Df['sofr30'].iloc[-1]:.2f}% {sofr30Df['30-day Arrow'].iloc[-1]}", 
                              unsafe_allow_html = True)
            sofrCol2.markdown(f"90-day Average: {sofr90Df['sofr90'].iloc[-1]:.2f}% {sofr90Df['90-day Arrow'].iloc[-1]}", 
                              unsafe_allow_html = True)
            sofrCol3.markdown(f"180-day Average: {sofr180Df['sofr180'].iloc[-1]:.2f}% {sofr180Df['180-day Arrow'].iloc[-1]}", 
                              unsafe_allow_html = True)
            st.plotly_chart(fig, use_container_width = True)

    def exchange_rates() -> None:
        currCol1, currCol2, currCol3, currCol4, currCol5 = st.columns([2, 2, 2, 2, 2])
        usdEuro = currCol1.button("USD to EURO")
        usdCad = currCol2.button("USD to CAD")
        usdInr = currCol3.button("USD to INR")
        usdYen = currCol4.button("USD to YEN")
        usdRmb = currCol5.button("USD to RMB")

        if usdEuro:
            usdEuroDf = pd.DataFrame(USEconomy.exchangeDataUsdEuro)
            usdEuroDf.index = pd.to_datetime(usdEuroDf.index)
            usdEuroDf.columns = ['exchange_rate']
            usdEuroDf['exchange_rate'] = 1 / usdEuroDf['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdEuroDf.index, y = usdEuroDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to EURO')
            st.subheader(f"Latest USD to EURO Exchange Rate: {usdEuroDf['exchange_rate'].iloc[-1]:.3f}")
            st.plotly_chart(fig, use_container_width = True)

        if usdCad:
            usdCadDf = pd.DataFrame(USEconomy.exchangeDataUsdCad)
            usdCadDf.index = pd.to_datetime(usdCadDf.index)
            usdCadDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdCadDf.index, y = usdCadDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to CAD')
            st.subheader(f"Latest USD to CAD Exchange Rate: {usdCadDf['exchange_rate'].iloc[-1]:.3f} CAD")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdInr:
            usdInrDf = pd.DataFrame(USEconomy.exchangeDataUsdInr)
            usdInrDf.index = pd.to_datetime(usdInrDf.index)
            usdInrDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdInrDf.index, y = usdInrDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to INR')
            st.subheader(f"Latest USD to INR Exchange Rate: {usdInrDf['exchange_rate'].iloc[-1]:.3f} INR")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdYen:
            usdYenDf = pd.DataFrame(USEconomy.exchangeDataUsdYen)
            usdYenDf.index = pd.to_datetime(usdYenDf.index)
            usdYenDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdYenDf.index, y = usdYenDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to YEN')
            st.subheader(f"Latest USD to YEN Exchange Rate: {usdYenDf['exchange_rate'].iloc[-1]:.3f} YEN")
            st.plotly_chart(fig, use_container_width = True)

        if usdRmb:
            usdRmbDf = pd.DataFrame(USEconomy.exchangeDataUsdRmb)
            usdRmbDf.index = pd.to_datetime(usdRmbDf.index)
            usdRmbDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdRmbDf.index, y = usdRmbDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to RMB')
            st.subheader(f"Latest USD to RMB Exchange Rate: {usdRmbDf['exchange_rate'].iloc[-1]:.3f} RMB")
            st.plotly_chart(fig, use_container_width = True)

    def mortgage_rates() -> None:
        mortgage15Df = pd.DataFrame(USEconomy.mortgage15Data)
        mortgage15Df.index = pd.to_datetime(mortgage15Df.index)
        mortgage15Df.columns = ['mort15']

        mortgage30Df = pd.DataFrame(USEconomy.mortgage30Data)
        mortgage30Df.index = pd.to_datetime(mortgage30Df.index)
        mortgage30Df.columns = ['mort30']

        fig = make_subplots(specs = [[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = mortgage30Df.index, y = mortgage30Df['mort30'], name = '30 Year Rate'))
        fig.add_trace(go.Scatter(x = mortgage15Df.index, y = mortgage15Df['mort15'], name = '15 Year Rate'))

        fig.update_layout(title = 'Fixed Mortgage Rates',
                          yaxis = dict(title = 'Rate'),
                          xaxis = dict(title = 'Date'))
        st.subheader(f"Latest 15 Year Fixed Rate: {mortgage15Df['mort15'].iloc[-1]:.2f}%")
        st.subheader(f"Latest 30 Year Fixed Rate: {mortgage30Df['mort30'].iloc[-1]:.2f}%")
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
