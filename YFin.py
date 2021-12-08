import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA

st.title('Check your titles!')
st.markdown('### Predict the trend of your stocks!')
tit_dict = {"GOOG":'Google', "AAPL":'Apple', "TSLA":'Tesla', "MSFT":'Microsoft'}

title = st.selectbox("Pick your title among Google, Apple, Tesla and Microsoft ", ["GOOG", "AAPL", "TSLA", "MSFT"])
st.write('You selected --> ', tit_dict[title])

ticker = yf.Ticker(title)
data = ticker.history(period = '5Y')

st.markdown('##### A few rows to check the data!')
st.write(data.head(2))
st.markdown('#### Showing the stock as a time series !')

st.line_chart(data['Close'])

st.markdown('#### .. and its return in percentage during the last year! Click on double arrow to expand!')

st.line_chart(data['Close'].pct_change()*100)

st.markdown('### The prediction for the next 4 weeks (20 working days)')

def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)

# invert differenced value

def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]

# seasonal difference
X = data['Close'].values
days_in_year = 280
differenced = difference(X, days_in_year)
# fit model
model = ARIMA(differenced, order=(7,0,1))
model_fit = model.fit()
# multi-step out-of-sample forecast
forecast = model_fit.forecast(steps=20)
# invert the differenced forecast to something usable
history = [x for x in X]
day = 1
forecasted_val = {}
for yhat in forecast:
    inverted = inverse_difference(history, yhat, days_in_year)
    forecasted_val[day]=inverted
    #st.write('Day %d: %f' % (day, inverted))
    history.append(inverted)
    day += 1

st.line_chart(forecasted_val.values())
lista = list(forecasted_val.values())
last_val = lista[-1]
current_val = data['Close'].iloc[-1]
st.markdown('### Predicted a change of : ')
change = (last_val-current_val) / last_val * 100
change = round(change, 2)

st.write("### % ", change)
