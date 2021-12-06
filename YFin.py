import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf

st.title('Check your titles!')
st.markdown('### This is an application that shows data and graphics on finance data.')

title = st.selectbox("Pick your title", ["GOOG", "AAPL", "TSLA", "MSFT"])
st.write('you selected ', title)

ticker = yf.Ticker(title)
data = ticker.history(period = '5Y')
st.write(data.head())
chart = st.line_chart(data['Close'])

# variability
change = st.line_chart(data['Close'].pct_change()*100)
