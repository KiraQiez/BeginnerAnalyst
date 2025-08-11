import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📈 Crypto Price Tracker")
st.markdown("View cryptocurrency price trends using CoinGecko API.")

# Sidebar inputs
st.sidebar.header("Settings")
coin = st.sidebar.text_input("Coin ID (e.g., bitcoin, ethereum)", "bitcoin")
currency = st.sidebar.text_input("Currency (e.g., usd, eur, myr)", "usd")
days = st.sidebar.slider("Days of history", 1, 365, 30)
interval = st.sidebar.selectbox("Interval", ["daily", "hourly"])

# API URL & params
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {
    "vs_currency": currency.lower(),
    "days": days,
    "interval": interval
}

# Fetch data
try:
    response = requests.get(url, params=params)
    data = response.json()

    if "prices" in data:
        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Show Data Table
        with st.expander("Show Raw Data"):
            st.dataframe(df)

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df["date"], df["price"], marker="o")
        ax.set_title(f"{coin.capitalize()} Price Trend ({days} Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Price ({currency.upper()})")
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.error("Error fetching data. Check coin ID or currency.")

except Exception as e:
    st.error(f"An error occurred: {e}")
