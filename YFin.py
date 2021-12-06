import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf

st.title('Check your titles!')
st.markdown('### This is an application that shows data and graphics on finance data.')

ticker = yf.Ticker('AAPL')

data = ticker.history(period = '5Y')
st.write(data.head())

chart = st.line_chart(data['Close'])