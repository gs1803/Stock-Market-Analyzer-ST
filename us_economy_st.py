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
    exchangeDataUsdEuro = fred.get_series('DEXUSEU', observation_start = '1/1/2015')
    exchangeDataUsdCad = fred.get_series('DEXCAUS', observation_start = '1/1/2015')
    exchangeDataUsdInr = fred.get_series('DEXINUS', observation_start = '1/1/2015')
    exchangeDataUsdYen = fred.get_series('DEXJPUS', observation_start = '1/1/2015')
    exchangeDataUsdRmb = fred.get_series('DEXCHUS', observation_start = '1/1/2015')
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
        fig = go.Figure(data = go.Scatter(x = unemploymentDf.index, y = unemploymentDf['unemployment_rate']))

        fig.update_layout(xaxis_title = 'Date',
                          title = 'Unemployment Rate')
        st.metric(label = f"Latest Unemployment Rate ({unemploymentDf.index[-1].strftime('%Y-%m')}):", 
                  value = f"{unemploymentDf['unemployment_rate'].iloc[-1]:.3f}%", 
                  delta = f"{unemploymentDf['unemployment_rate'].iloc[-1] - unemploymentDf['unemployment_rate'].iloc[-2]:.3f} From Previous Month",
                  delta_color = 'inverse')
        st.plotly_chart(fig, use_container_width = True)
    
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
        currCol1, currCol2, currCol3, currCol4, currCol5 = st.columns([2, 2, 2, 2, 2])
        usdEuro = currCol1.button("USD to EURO")
        usdCad = currCol2.button("USD to CAD")
        usdInr = currCol3.button("USD to INR")
        usdYen = currCol4.button("USD to YEN")
        usdRmb = currCol5.button("USD to RMB")

        if usdEuro:
            usdEuroDf = pd.DataFrame(USEconomy.exchangeDataUsdEuro).dropna(how = 'all')
            usdEuroDf.index = pd.to_datetime(usdEuroDf.index)
            usdEuroDf.columns = ['exchange_rate']
            usdEuroDf['exchange_rate'] = 1 / usdEuroDf['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdEuroDf.index, y = usdEuroDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to EURO')
            st.metric(label = f"Latest USD to EURO Exchange Rate ({usdEuroDf.index[-1].date()}):", 
                      value = f"{usdEuroDf['exchange_rate'].iloc[-1]:.3f} EUR", 
                      delta = f"{usdEuroDf['exchange_rate'].iloc[-1] - usdEuroDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

        if usdCad:
            usdCadDf = pd.DataFrame(USEconomy.exchangeDataUsdCad).dropna(how = 'all')
            usdCadDf.index = pd.to_datetime(usdCadDf.index)
            usdCadDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdCadDf.index, y = usdCadDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to CAD')
            st.metric(label = f"Latest USD to CAD Exchange Rate ({usdCadDf.index[-1].date()}):", 
                      value = f"{usdCadDf['exchange_rate'].iloc[-1]:.3f} CAD", 
                      delta = f"{usdCadDf['exchange_rate'].iloc[-1] - usdCadDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdInr:
            usdInrDf = pd.DataFrame(USEconomy.exchangeDataUsdInr).dropna(how = 'all')
            usdInrDf.index = pd.to_datetime(usdInrDf.index)
            usdInrDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdInrDf.index, y = usdInrDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to INR')
            st.metric(label = f"Latest USD to INR Exchange Rate ({usdInrDf.index[-1].date()}):", 
                      value = f"{usdInrDf['exchange_rate'].iloc[-1]:.3f} INR", 
                      delta = f"{usdInrDf['exchange_rate'].iloc[-1] - usdInrDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)
        
        if usdYen:
            usdYenDf = pd.DataFrame(USEconomy.exchangeDataUsdYen).dropna(how = 'all')
            usdYenDf.index = pd.to_datetime(usdYenDf.index)
            usdYenDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdYenDf.index, y = usdYenDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to YEN')
            st.metric(label = f"Latest USD to YEN Exchange Rate ({usdYenDf.index[-1].date()}):",
                      value = f"{usdYenDf['exchange_rate'].iloc[-1]:.3f} YEN", 
                      delta = f"{usdYenDf['exchange_rate'].iloc[-1] - usdYenDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
            st.plotly_chart(fig, use_container_width = True)

        if usdRmb:
            usdRmbDf = pd.DataFrame(USEconomy.exchangeDataUsdRmb).dropna(how = 'all')
            usdRmbDf.index = pd.to_datetime(usdRmbDf.index)
            usdRmbDf.columns = ['exchange_rate']
            fig = go.Figure(data = go.Scatter(x = usdRmbDf.index, y = usdRmbDf['exchange_rate']))

            fig.update_layout(xaxis_title = 'Date',
                              title = 'USD to RMB')
            st.metric(label = f"Latest USD to RMB Exchange Rate ({usdRmbDf.index[-1].date()}):",
                      value = f"{usdRmbDf['exchange_rate'].iloc[-1]:.3f} RMB", 
                      delta = f"{usdRmbDf['exchange_rate'].iloc[-1] - usdRmbDf['exchange_rate'].iloc[-2]:.3f} From Previous Day")
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
