import streamlit as st
import yfinance as yf

st.title("📈 Stock AI Analyzer")

ticker = st.text_input("შეიყვანე აქციის სიმბოლო", "NVDA")

if st.button("ანალიზი"):
    data = yf.download(ticker, period="1y")

    if data.empty:
        st.error("აქცია ვერ მოიძებნა")
    else:
        price = data["Close"].iloc[-1]

        st.write("აქცია:", ticker)
        st.write("ბოლო ფასი:", price)

        st.line_chart(data["Close"])
