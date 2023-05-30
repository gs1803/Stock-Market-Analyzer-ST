import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import tensorflow as tf
import datetime as dt
import math
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

tf.random.set_seed(42)

class StockPricePredictor:
    def __init__(self, stock, titleStock) -> None:
        self.stock = stock
        self.titleStock = titleStock
        try:
            self.companyStock = yf.Ticker(titleStock).info['longName']
        except:
            self.companyStock = ('')

    def ml_model(self) -> None:
        df = pd.DataFrame(self.stock['Adj Close'])

        scaler = MinMaxScaler(feature_range = (0, 1))
        scaled_data = scaler.fit_transform(df)

        training_data_len = math.ceil(len(df) * .7)
        train_data = scaled_data[0:training_data_len, :]

        x_train_data=[]
        y_train_data =[]
        for i in range(60,len(train_data)):
            x_train_data=list(x_train_data)
            y_train_data=list(y_train_data)
            x_train_data.append(train_data[i - 60:i, 0])
            y_train_data.append(train_data[i, 0])

            x_train_data1, y_train_data1 = np.array(x_train_data), np.array(y_train_data)
            x_train_data2 = np.reshape(x_train_data1, (x_train_data1.shape[0], x_train_data1.shape[1], 1))

        model = Sequential()
        model.add(LSTM(units = 50, return_sequences = True,input_shape = (x_train_data2.shape[1], 1)))
        model.add(LSTM(units = 50, return_sequences = False))
        model.add(Dense(units = 25))
        model.add(Dense(units = 1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')

        progressBar = st.progress(0)
        with st.spinner("Training model..."):
            epochs = 32
            for epoch in range(epochs):
                progressBar.progress((epoch + 1) / epochs)
                model.fit(x_train_data2, y_train_data1, batch_size = 100, epochs = 1, verbose = 0)
            progressBar.empty()

        test_data = scaled_data[training_data_len - 60:, :]
        x_test = []
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])
        
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

        predictions = model.predict(x_test, verbose = 0)
        predictions = scaler.inverse_transform(predictions)

        train = df[:training_data_len]
        valid = df[training_data_len:]

        valid = valid.copy()
        valid['Predictions'] = predictions
        actual_values = np.array(valid['Adj Close'])

        rmse = np.sqrt(mean_squared_error(actual_values, predictions))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = train.index, y = train['Adj Close'], name = 'Actual'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid['Adj Close'], name = 'Actual', showlegend = False))
        fig.add_trace(go.Scatter(x = valid.index, y = valid['Predictions'], name = 'Predictions',
                                 line = dict(color = 'red')))
        
        fig.update_layout(title = f"Stock Price Prediction for {self.titleStock} ({self.companyStock})", 
                          xaxis_title = 'Date', 
                          yaxis_title = 'Adj Close')
        st.subheader(f"Latest Stock Adj Close Price: {self.stock['Adj Close'].iloc[-1]:.2f}")   
        st.plotly_chart(fig, use_container_width = True)

        nextDayPrediction = model.predict(np.array([x_test[-1]]), verbose = 0)
        nextDayPrediction = scaler.inverse_transform(nextDayPrediction)[0][0]

        predictionErrors = []
        for i in range(30):
            x_test_sample = np.array([x_test[-1]])
            predictionI = model.predict(x_test_sample, verbose = 0)
            predictionI = scaler.inverse_transform(predictionI)[0][0]
            predictionErrors.append(predictionI)

        predictionInterval = 1.96 * np.std(predictionErrors)

        tomorrowDate = dt.date.today() + dt.timedelta(days = 1)
        st.write(f"Predicted Stock Adj Close Price for ({tomorrowDate}): {nextDayPrediction:.2f}")
        st.write(f"RMSE: {rmse}")
        st.write(f"95% Confidence Interval: ±{format(predictionInterval, '0.10f')}")
        
