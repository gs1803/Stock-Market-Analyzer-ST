import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from fredapi import Fred

fred = Fred(api_key = '')

class USEconomy:
    inflationData = fred.get_series('CPIAUCSL', units = 'pc1', observation_start = '1/1/1970')
    coreInflationData = fred.get_series('CPILFESL', units = 'pc1', observation_start = '1/1/1970')
    unemploymentData = fred.get_series('UNRATE', observation_start = '1/1/1970')
    exchangeDataUsdEuro = fred.get_series('DEXUSEU', observation_start = '1/1/2015')
    exchangeDataUsdCad = fred.get_series('DEXCAUS', observation_start = '1/1/2015')
    exchangeDataUsdInr = fred.get_series('DEXINUS', observation_start = '1/1/2015')
    exchangeDataUsdYen = fred.get_series('DEXJPUS', observation_start = '1/1/2015')
    exchangeDataUsdRmb = fred.get_series('DEXCHUS', observation_start = '1/1/2015')

    def inflation_rate() -> None:
        inflationOption = st.radio("Select an option:", ['Inflation Rate', 'Core Inflation Rate'])

        if inflationOption == 'Inflation Rate':
            inflationDf = pd.DataFrame(USEconomy.inflationData)
            inflationDf.index = pd.to_datetime(inflationDf.index)
            inflationDf.columns = ['inflation_rate']
            fig = go.Figure(data = go.Scatter(x = inflationDf.index, y = inflationDf['inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Inflation Rate')
            st.subheader(f"Current Inflation Rate: {inflationDf['inflation_rate'].iloc[-1]:.3f}%")
            st.plotly_chart(fig, use_container_width = True)
        elif inflationOption == 'Core Inflation Rate':
            coreInflationDf = pd.DataFrame(USEconomy.coreInflationData)
            coreInflationDf.index = pd.to_datetime(coreInflationDf.index)
            coreInflationDf.columns = ['core_inflation_rate']
            fig = go.Figure(data = go.Scatter(x = coreInflationDf.index, y = coreInflationDf['core_inflation_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'Core Inflation Rate')
            st.subheader(f"Current Core Inflation Rate: {coreInflationDf['core_inflation_rate'].iloc[-1]:.3f}%")
            st.plotly_chart(fig, use_container_width = True)

    def unemployment_rate() -> None:
        unemploymentDf = pd.DataFrame(USEconomy.unemploymentData)
        unemploymentDf.index = pd.to_datetime(unemploymentDf.index)
        unemploymentDf.columns = ['unemployment_rate']
        fig = go.Figure(data = go.Scatter(x = unemploymentDf.index, y = unemploymentDf['unemployment_rate']))

        fig.update_layout(xaxis_title = 'Date',
                          title = 'Unemployment Rate')
        st.subheader(f"Current Unemployment Rate: {unemploymentDf['unemployment_rate'].iloc[-1]:.3f}%")
        st.plotly_chart(fig, use_container_width = True)

    def exchange_rate() -> None:
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
            st.subheader(f"Current USD to EURO Exchange Rate: {usdEuroDf['exchange_rate'].iloc[-1]:.3f}")
            st.plotly_chart(fig, use_container_width = True)

        if usdCad:
            usdCadDf = pd.DataFrame(USEconomy.exchangeDataUsdCad)
            usdCadDf.index = pd.to_datetime(usdCadDf.index)
            usdCadDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdCadDf.index, y = usdCadDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to CAD')
            st.subheader(f"Current USD to CAD Exchange Rate: {usdCadDf['exchange_rate'].iloc[-1]:.3f} CAD")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdInr:
            usdInrDf = pd.DataFrame(USEconomy.exchangeDataUsdInr)
            usdInrDf.index = pd.to_datetime(usdInrDf.index)
            usdInrDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdInrDf.index, y = usdInrDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to INR')
            st.subheader(f"Current USD to INR Exchange Rate: {usdInrDf['exchange_rate'].iloc[-1]:.3f} INR")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdYen:
            usdYenDf = pd.DataFrame(USEconomy.exchangeDataUsdYen)
            usdYenDf.index = pd.to_datetime(usdYenDf.index)
            usdYenDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdYenDf.index, y = usdYenDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to YEN')
            st.subheader(f"Current USD to YEN Exchange Rate: {usdYenDf['exchange_rate'].iloc[-1]:.3f} YEN")
            st.plotly_chart(fig, use_container_width = True)

        if usdRmb:
            usdRmbDf = pd.DataFrame(USEconomy.exchangeDataUsdRmb)
            usdRmbDf.index = pd.to_datetime(usdRmbDf.index)
            usdRmbDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdRmbDf.index, y = usdRmbDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to RMB')
            st.subheader(f"Current USD to RMB Exchange Rate: {usdRmbDf['exchange_rate'].iloc[-1]:.3f} RMB")
            st.plotly_chart(fig, use_container_width = True)
        
    def economy_chooser() -> None:
        economyOptions = {'Inflation Rate': USEconomy.inflation_rate,
                          'Unemployment Rate': USEconomy.unemployment_rate,
                          'Exchange Rate': USEconomy.exchange_rate}

        economyOptionList = list(economyOptions.keys())
        selectedEconomyOption = st.selectbox("Select an option", economyOptionList)

        selectedEconomyFunction = economyOptions.get(selectedEconomyOption)
        if selectedEconomyFunction:
            selectedEconomyFunction()
