import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet  import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START_DATE="2014-01-01"
CURR_DATE=date.today().strftime("%Y-%m-%d")

# print(CURR_DATE)

st.title("Stock Prediction App")

stocks={"Apple":"AAPL","Google":"GOOG","Microsoft":"MSFT","Marvell":"MRVL"}

selected_stock=st.selectbox("Select Dataset for Prediction",list(stocks.keys()))

num_years=st.slider("Years of Prediction:",1,6)

peirod=num_years*365

@st.cache
def load_data(ticker):
    data=yf.download(ticker,START_DATE,CURR_DATE)
    data.reset_index(inplace=True)
    return data

data_load_state=st.text("Loading Data...")

data=load_data(stocks[selected_stock])

data_load_state.text("Data Loading Complete...!")

st.subheader("Raw Data")
st.write(data.tail())

def plot_raw_data():
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"],y=data["Open"],name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"],y=data["Close"],name="stock_close"))
    fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()


df_train=data[["Date","Close"]]
df_train=df_train.rename(columns={"Date":"ds","Close":"y"})

model=Prophet()

model.fit(df_train)

future=model.make_future_dataframe(periods=peirod)

forecast=model.predict(future)

st.subheader("Forecast Data")
st.write(forecast.tail())

st.subheader("Forecast Data")
future_fig=plot_plotly(model,forecast)
st.plotly_chart(future_fig)

st.subheader("Forecast Components")

fig_com=model.plot_components(forecast)
st.write(fig_com)

