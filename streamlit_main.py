import streamlit as st
import yfinance as yf
import pytz
from datetime import date, datetime, timedelta
from stock_analyzer_st import StockAnalyzer
from stock_information_st import StockInformation
from standard_poor_corr_st import StandardPoorCorr
from us_economy_st import USEconomy
from stock_price_predict_st import StockPricePredictor
from stock_downloader_st import download_stock_data
import subprocess

etNow = datetime.now(pytz.timezone('US/Eastern')).date()

def stock_info():
    st.header("Graphs")
    startCol, endCol = st.columns([5, 5])

    start = startCol.date_input("Select the Start Date:",
                                value = etNow, 
                                min_value = date(1960, 1, 1), 
                                max_value = etNow)
    start = str(start).replace('/', '-')
    end = endCol.date_input("Select the End Date:", 
                             value = etNow, 
                             min_value = date(1960, 1, 1), 
                             max_value = etNow)
    end = end + timedelta(days = 1)
    end = str(end).replace('/', '-')

    startDate = datetime.strptime(start, '%Y-%m-%d')
    endDate = datetime.strptime(end, '%Y-%m-%d')

    if not start:
        pass
    else:
        stockOption = st.radio('Select an option:', ['Manual Search', 'S&P500', 'Dow Jones', 'Russell 2000', 'NASDAQ Composite'], 
                               label_visibility = 'collapsed', horizontal = True)
        
        if stockOption == 'Manual Search':
            userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
        if stockOption == 'S&P500':
            userStock = '^GSPC'
        if stockOption == 'Dow Jones':
            userStock = '^DJI'
        if stockOption == 'Russell 2000':
            userStock = '^RUT'
        if stockOption == 'NASDAQ Composite':
            userStock = '^IXIC'

        if not userStock:
            st.write(" ")
        elif not userStock.isascii():
            st.write(" ")
        else:
            inputStock = download_stock_data(userStock, startDate, endDate)
            if inputStock.empty:
                st.write("No Information Available for the Ticker.")
            else:
                infoStock = StockAnalyzer(inputStock, userStock)
                StockAnalyzer.graph_chooser(infoStock)

def industry_info():
    st.header("Ticker Information")
    StockInformation.stock_details()

def holder_info():
    st.header("Holders Information")
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
    stockOption = st.radio('Select an option:', ['Manual Search', 'S&P500', 'Dow Jones', 'Russell 2000', 'NASDAQ Composite'], horizontal = True)
    
    if stockOption == 'Manual Search':
        userStock = st.text_input("Enter the Stock Ticker:").upper().replace(" ", "")
    if stockOption == 'S&P500':
        userStock = '^GSPC'
    if stockOption == 'Dow Jones':
        userStock = '^DJI'
    if stockOption == 'Russell 2000':
        userStock = '^RUT'
    if stockOption == 'NASDAQ Composite':
        userStock = '^IXIC'

    end = str(etNow + timedelta(days = 1))
    if not userStock:
        st.write(" ")
    elif not userStock.isascii():
        st.write(" ")
    else:
        inputStock = yf.download(userStock, '2021-01-01', end, progress = False)
        if inputStock.empty:
            st.write("No Information Available for the Ticker.")
        else:
            predictStock = StockPricePredictor(inputStock, userStock)
            StockPricePredictor.ml_model_chooser(predictStock)

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
        # Command to get the pybind11 includes
    command = ["python", "-m", "pybind11", "--includes"]
    # Execute the command
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        st.write(output.strip())  # Print the includes path
    except subprocess.CalledProcessError as e:
        st.write("Error:", e.output)
