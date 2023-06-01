import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import tensorflow as tf
import datetime as dt
import math
import xgboost as xgb
from sklearn.svm import SVR
from keras.models import Sequential
from keras.layers import Dense, LSTM, GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.optimizers.legacy import Adam

tf.random.set_seed(42)

class StockPricePredictor:
    tomorrowDate = dt.date.today() + dt.timedelta(days = 1)

    def __init__(self, stock, titleStock) -> None:
        self.stock = stock
        self.titleStock = titleStock
        try:
            self.companyStock = yf.Ticker(titleStock).info['longName']
        except:
            self.companyStock = ('')

    def gru_ml_model(self) -> None:
        df = self.stock['Adj Close'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range = (0, 1))
        
        scaled_prices = scaler.fit_transform(df)
        x_train = []
        y_train = []
        for i in range(120, len(scaled_prices)):
            x_train.append(scaled_prices[i - 120:i, 0])
            y_train.append(scaled_prices[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        model = Sequential()
        model.add(GRU(units = 50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
        model.add(GRU(units = 50))
        model.add(Dense(units = 1))
        model.compile(optimizer = Adam(), loss = 'mean_squared_error')
        
        progressBar = st.progress(0)
        with st.spinner("Training model..."):
            epochs = 32
            for epoch in range(epochs):
                progressBar.progress((epoch + 1) / epochs)
                model.fit(x_train, y_train, epochs = 1, batch_size = 32, verbose = False)
            progressBar.empty()

        x_test = scaled_prices[-120:]
        x_test = np.reshape(x_test, (1, 120, 1))

        predictions = model.predict(x_test, verbose = False)
        predictions = scaler.inverse_transform(predictions)

        rmse = np.sqrt(mean_squared_error(df[-1], predictions))

        predicted = np.concatenate((df[-120:], predictions))
        predictedDf = pd.DataFrame(predicted, index = self.stock.index[-121:], columns = ['predicted_values'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = self.stock.index[:-121], y = self.stock['Adj Close'], name = 'Actual'))
        fig.add_trace(go.Scatter(x = predictedDf.index, y = self.stock['Adj Close'][-121:], name = 'Actual', showlegend = False))
        fig.add_trace(go.Scatter(x = predictedDf.index, y = predictedDf['predicted_values'], name = 'Predictions',
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

        st.write(f"Predicted Stock Adj Close Price for ({StockPricePredictor.tomorrowDate}): {nextDayPrediction:.2f}")
        st.write(f"RMSE: {rmse}")
        st.write(f"95% Confidence Interval: ±{format(predictionInterval, '0.10f')}")

    def lstm_ml_model(self) -> None:
        df = pd.DataFrame(self.stock['Adj Close'])

        scaler = MinMaxScaler(feature_range = (0, 1))
        scaled_data = scaler.fit_transform(df)

        training_data_len = math.ceil(len(df) * .7)
        train_data = scaled_data[0:training_data_len, :]

        x_train_data=[]
        y_train_data =[]
        for i in range(120,len(train_data)):
            x_train_data=list(x_train_data)
            y_train_data=list(y_train_data)
            x_train_data.append(train_data[i - 120:i, 0])
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

        test_data = scaled_data[training_data_len - 120:, :]
        x_test = []
        for i in range(120, len(test_data)):
            x_test.append(test_data[i - 120:i, 0])
        
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
        
        st.write(f"Predicted Stock Adj Close Price for ({StockPricePredictor.tomorrowDate}): {nextDayPrediction:.2f}")
        st.write(f"RMSE: {rmse}")
        st.write(f"95% Confidence Interval: ±{format(predictionInterval, '0.10f')}")

    def gb_ml_model(self) -> None:
        df = self.stock['Adj Close']
        n = 5
        features = []
        labels = []

        for i in range(n, len(df)):
            features.append(df[i - n:i])
            labels.append(df[i])

        features = np.array(features)
        labels = np.array(labels)

        split_index = int(len(features) * 0.8)

        X_train = features[:split_index]
        X_test = features[split_index:]
        y_train = labels[:split_index]
        y_test = labels[split_index:]

        xgb_model = xgb.XGBRegressor()
        xgb_model.fit(X_train, y_train)

        y_pred_train = xgb_model.predict(X_train)
        mse_train = mean_squared_error(y_train, y_pred_train)
        rmse_train = np.sqrt(mse_train)

        y_pred_test = xgb_model.predict(X_test)
        mse_test = mean_squared_error(y_test, y_pred_test)
        rmse_test = np.sqrt(mse_test)

        last_n_days = df[-n:]
        last_n_days = np.array([last_n_days])
        prediction = xgb_model.predict(last_n_days)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = self.stock.index[:-len(y_test)], y = self.stock['Adj Close'], name = 'Actual'))
        fig.add_trace(go.Scatter(x = self.stock.index[-len(y_test):], y = y_test, name = 'Actual', showlegend = False))
        fig.add_trace(go.Scatter(x = self.stock.index[-len(y_test):], y = y_pred_test, name = 'Predictions',
                                 line = dict(color = 'red')))
        
        fig.update_layout(title = f"Stock Price Prediction for {self.titleStock} ({self.companyStock})", 
                          xaxis_title = 'Date', 
                          yaxis_title = 'Adj Close')
        st.subheader(f"Latest Stock Adj Close Price: {self.stock['Adj Close'].iloc[-1]:.2f}")
        st.plotly_chart(fig, use_container_width = True)

        st.write(f"Predicted Stock Adj Close Price for ({StockPricePredictor.tomorrowDate}): {prediction[0]:.2f}")
        st.write(f"Training RMSE: {rmse_train}")
        st.write(f"Testing RMSE: {rmse_test}")

    def svm_ml_model(self) -> None:
        df = self.stock['Adj Close']
        n = 5
        features = []
        labels = []

        for i in range(n, len(df)):
            features.append(df[i - n:i])
            labels.append(df[i])

        features = np.array(features)
        labels = np.array(labels)

        split_index = int(len(features) * 0.8)

        X_train = features[:split_index]
        X_test = features[split_index:]
        y_train = labels[:split_index]
        y_test = labels[split_index:]

        svm_model = SVR(kernel = 'rbf')
        svm_model.fit(X_train, y_train)

        y_pred_train = svm_model.predict(X_train)
        mse_train = mean_squared_error(y_train, y_pred_train)
        rmse_train = np.sqrt(mse_train)

        y_pred_test = svm_model.predict(X_test)
        mse_test = mean_squared_error(y_test, y_pred_test)
        rmse_test = np.sqrt(mse_test)

        last_n_days = df[-n:]
        prediction = svm_model.predict([last_n_days])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = self.stock.index[:-len(y_test)], y = self.stock['Adj Close'], name = 'Actual'))
        fig.add_trace(go.Scatter(x = self.stock.index[-len(y_test):], y = y_test, name = 'Actual', showlegend = False))
        fig.add_trace(go.Scatter(x = self.stock.index[-len(y_test):], y = y_pred_test, name = 'Predictions',
                                 line = dict(color = 'red')))
        
        fig.update_layout(title = f"Stock Price Prediction for {self.titleStock} ({self.companyStock})", 
                          xaxis_title = 'Date', 
                          yaxis_title = 'Adj Close')
        st.subheader(f"Latest Stock Adj Close Price: {self.stock['Adj Close'].iloc[-1]:.2f}")
        st.plotly_chart(fig, use_container_width = True)
        
        st.write(f"Predicted Stock Adj Close Price for ({StockPricePredictor.tomorrowDate}): {prediction[0]:.2f}")
        st.write(f"Training RMSE: {rmse_train}")
        st.write(f"Testing RMSE: {rmse_test}")

    def ml_model_chooser(self) -> None:
        mlOptions = {
            'GRU (Gated Recurrent Unit) Model': self.gru_ml_model,
            'LSTM (Long Short-Term Memory) Model': self.lstm_ml_model,
            'XGB (Extreme Gradient Boosting) Model': self.gb_ml_model,
            'SVM (Support Vector Machine) Model': self.svm_ml_model
        }

        mlOptionList = list(mlOptions.keys())
        selectedMlOption = st.selectbox("Select an option:", mlOptionList)
        
        selectedMlFunction = mlOptions.get(selectedMlOption)
        selectedMlFunction()
