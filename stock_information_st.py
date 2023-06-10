import streamlit as st
import pandas as pd
import yfinance as yf

class StockInformation:
    def __init__(self, stock) -> None:
        self.stock = stock

    def stock_major_holders(self) -> None:
        try:
            majorHolders = pd.DataFrame(self.stock.major_holders)
            majorHolders = majorHolders.reset_index(drop = True)
            majorHolders.columns = ['Percentage', 'Information']
            st.dataframe(majorHolders, use_container_width = True)
        except KeyError:
            st.write(" ")

    def stock_institutional_holders(self) -> None:
        try:
            institutionalHolders = pd.DataFrame(self.stock.institutional_holders)
            institutionalHolders = institutionalHolders.reset_index(drop = True)
            institutionalHolders.columns = ['Holder', 'Shares', 'Date Reported', '% Out', 'Value']
            institutionalHolders['Date Reported'] = pd.to_datetime(institutionalHolders['Date Reported']).dt.date
            st.dataframe(institutionalHolders, use_container_width = True)
        except KeyError:
            st.write(" ")

    def stock_mutualfund_holders(self) -> None:
        try:
            mutualfundHolders = pd.DataFrame(self.stock.mutualfund_holders)
            mutualfundHolders = mutualfundHolders.reset_index(drop = True)
            mutualfundHolders.columns = ['Holder', 'Shares', 'Date Reported', '% Out', 'Value']
            mutualfundHolders['Date Reported'] = pd.to_datetime(mutualfundHolders['Date Reported']).dt.date
            st.dataframe(mutualfundHolders, use_container_width = True)
        except KeyError:
            st.write(" ")

    def stock_dividends(self) -> None:
        try:
            df_StockDiv = pd.DataFrame(self.stock.dividends)
            df_StockDiv.reset_index(inplace = True)
            df_StockDiv['Date'] = pd.to_datetime(df_StockDiv['Date']).dt.date
            df_StockDiv.columns = ['Date', 'Dividends']
            st.dataframe(df_StockDiv.tail(), use_container_width = True)
        except KeyError:
            st.write(" ")

    def stock_splits(self) -> None:
        try:
            df_StockSpl = pd.DataFrame(self.stock.splits)
            df_StockSpl.reset_index(inplace = True)
            df_StockSpl['Date'] = pd.to_datetime(df_StockSpl['Date']).dt.date
            df_StockSpl.columns = ['Date', 'Splits']
            st.dataframe(df_StockSpl.tail(), use_container_width = True)
        except KeyError:
            st.write(" ")

    def stock_news(self) -> None:
        newsList = self.stock.news
        relevantInfo = []
        relatedStocks = []

        st.subheader("Related News Articles")
        for news in newsList:
            title = news['title'].rstrip('\\').replace(':', '\:').replace('$', '\$')
            link = news['link']
            relatedTicker = news['relatedTickers']
            relevantInfo.append({'title': title, 'link': link})
            relatedStocks.extend(relatedTicker)
        
        for item in relevantInfo:
            st.markdown("- [{}]({})".format(item['title'], item['link']))

        st.subheader("Related Tickers")
        uniqueTickers = list(set(relatedStocks))
        st.markdown("- " + ", ".join(uniqueTickers))
    
    def stock_info(self) -> None:
        infoDictionary = self.stock.info
        data = {
            'Metric': [],
            'Value': []
        }
        column_names = {
            'dividendRate': 'Dividend Rate',
            'dividendYield': 'Dividend Yield',
            'payoutRatio': 'Payout Ratio',
            'beta': 'Beta',
            'trailingPE': 'Trailing PE',
            'forwardPE': 'Forward PE',
            'bid': 'Bid',
            'ask': 'Ask',
            'bidSize': 'Bid Size',
            'askSize': 'Ask Size',
            'sharesOutstanding': 'Outstanding Shares',
            'sharesShort': 'Short Shares'
        }
        for key in column_names:
            if key in infoDictionary:
                data['Metric'].append(column_names[key])
                value = infoDictionary[key]
                if key == 'bid' or key == 'ask':
                    size_key = key + 'Size'
                    if size_key in infoDictionary:
                        size = infoDictionary[size_key]
                        value = f'{value:.2f} x {size}'
                elif isinstance(value, (int, float)):
                    value = '{:.2f}'.format(value)
                elif isinstance(value, str):
                    value = value.replace(',', '')
                data['Value'].append(value)
                
        infoDf = pd.DataFrame(data)
        infoDf = infoDf[~infoDf['Metric'].isin(['Bid Size', 'Ask Size'])]
        st.dataframe(infoDf, use_container_width = True)
    
    def holder_chooser(self) -> None:
        holderOption = st.selectbox("Select an option:", ['Major Holders', 'Institutional Holders', 'Mutual Fund Holders'])
        if holderOption == 'Major Holders':
            StockInformation.stock_major_holders(self)
        elif holderOption == 'Institutional Holders':
            StockInformation.stock_institutional_holders(self)
        elif holderOption == 'Mutual Fund Holders':
            StockInformation.stock_mutualfund_holders(self)
    
    def div_spl_chooser(self) -> None:
        divSplOption = st.selectbox("Select an option:", ['Dividends', 'Splits'])
        if divSplOption == 'Dividends':
            StockInformation.stock_dividends(self)
        elif divSplOption == 'Splits':
            StockInformation.stock_splits(self)

    def stock_details() -> None:
        names_head = ['Company Name', 'Ticker', 'Industry']
        data = pd.read_csv("stock_details.csv", encoding = 'utf-8', usecols = names_head)
        df = pd.DataFrame(data)
        df['Ticker'] = df['Ticker'].str.replace('.', '-', regex = False)
        detailChoose = st.selectbox("Select an option:", ['Ticker Details', 
                                                          'Filter by Industry', 
                                                          'Filter by Company'])

        if detailChoose == 'Ticker Details':
            details = st.text_input("Enter the Ticker for the Stock:").upper().replace(" ", "")
            if not details:
                st.write(" ")
            elif not details.isascii():
                st.write(" ")
            elif (df[df['Ticker'] == details].empty):
                st.write("No Company and Industry Information Available for the Ticker")
            else:
                detail_stock = (df[df['Ticker'] == details])
                st.dataframe(detail_stock, use_container_width = True)
            try:
                userStock = StockInformation(yf.Ticker(details))
                StockInformation.stock_info(userStock)
                StockInformation.stock_news(userStock)
            except Exception:
                st.write(" ")

        elif detailChoose == 'Filter by Industry':
            filterCol, searchCol = st.columns([5, 5])
            df_sort = sorted(set(df['Industry']))

            industry_filter = filterCol.text_input("Filter industries by alphabet (A-Z):").lower()
            alpha_list = [element for element in df_sort if element.startswith(f"{industry_filter}")]
            df_alpha_list = pd.DataFrame({'Industry Name': alpha_list}).reset_index(drop = True)
            filterCol.dataframe(df_alpha_list, use_container_width = True)
            
            industryChoice = searchCol.text_input("Enter an industry name: ").lower()
            if industryChoice:
                detailIndustry = (df[df['Industry'] == industryChoice])
                searchCol.dataframe(detailIndustry[['Ticker', 'Company Name']], use_container_width = True)

        elif detailChoose == 'Filter by Company':
            company_filter = st.text_input("Filter companies by alphabet (A-Z):").title()

            filtered_df = df[df['Company Name'].str.startswith(company_filter)]
            sorted_df = filtered_df.sort_values('Company Name').reset_index(drop = True)
            st.dataframe(sorted_df[['Company Name', 'Ticker']], use_container_width = True)
