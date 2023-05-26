import streamlit as st
import yfinance as yf
from datetime import date
from stock_analyzer_st import StockAnalyzer
from stock_information_st import StockInformation
from standard_poor_corr_st import StandardPoorCorr
from us_economy_st import USEconomy
from stockprice_predict_st import StockPricePredictor

def stock_info():
    st.header("Graphs")
    startCol, endCol = st.columns([5, 5])
    start = startCol.date_input("Select the Start Date:",
                                 value = date(2021, 1, 1), 
                                 min_value = date(1960, 1, 1), 
                                 max_value = date.today())
    start = str(start).replace('/', '-')
    end = endCol.date_input("Select the End Date:", 
                             value = date.today(), 
                             min_value = date(1960, 1, 1), 
                             max_value = date.today())
    end = str(end).replace('/', '-')

    if not start:
        pass
    else:
        userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
        if not userStock:
            st.write(" ")
        elif not userStock.isascii():
            st.write(" ")
        else:
            inputStock = yf.download(f"{userStock}", start, end, progress = False)
            if inputStock.empty:
                st.write("No Information Available for the Ticker.")
            else:
                infoStock = StockAnalyzer(inputStock, userStock)
                StockAnalyzer.graph_chooser(infoStock)

def industry_info():
    st.header("Ticker Information")
    StockInformation.stock_details()

def holder_info():
    st.header("Holder Information")
    try:
        userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
        if not userStock:
            st.write(" ")
        elif not userStock.isascii():
            st.write(" ")
        else:
            holderStock = StockInformation(yf.Ticker(userStock))
            StockInformation.holder_chooser(holderStock)
    except ValueError:
        st.write("No Information Available for the Ticker.")

def div_or_split():
    st.header("Dividends and Splits")
    try:
        userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
        if not userStock:
            st.write(" ")
        elif not userStock.isascii():
            st.write(" ")
        else:
            divSplitStock = StockInformation(yf.Ticker(userStock))
            StockInformation.div_spl_chooser(divSplitStock)
    except ValueError:
        st.write("No Information Available for the Ticker.")

def corr_table():
    st.header('Correlation Heatmap of S&P 500 Adj Closes')
    st.write("Data from 2015-01-01 to 2022-12-31")
    StandardPoorCorr.visualize_data()

def us_economy():
    st.header('US Economy')
    USEconomy.economy_chooser()

def stock_price_predictor():
    st.header('Stock Price Predictor')
    try:
        userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
        end = str(date.today())
        if not userStock:
            st.write(" ")
        elif not userStock.isascii():
            st.write(" ")
        else:
            inputStock = yf.download(userStock, '2021-01-01', end, progress = False)
            if inputStock.empty:
                pass
            else:
                predictStock = StockPricePredictor(inputStock, userStock)
                StockPricePredictor.ml_model(predictStock)
    except ValueError:
        st.write("No Information Available for the Ticker.")

def main():
    st.title("Stock Market Analyzer")
    st.sidebar.title("Main Menu")

    optionsStock = {
        'Market Graphs and Analysis': stock_info,
        'Ticker Information': industry_info,
        'Holders Information': holder_info,
        'Dividends and Splits': div_or_split,
        'Correlation Matrix (S&P 500)': corr_table,
        'US Economy Graphs': us_economy,
        'Stock Price Predictor': stock_price_predictor}

    selectOption = st.sidebar.radio("Select an option:", list(optionsStock.keys()))
    selectedFunction = optionsStock.get(selectOption)

    if selectedFunction:
        selectedFunction()

if __name__ == "__main__":
    main()
