import streamlit as st
import yfinance as yf

st.title("📈 Stock AI Analyzer")

ticker = st.text_input("შეიყვანე აქციის სიმბოლო", "NVDA")

if st.button("ანალიზი"):
    data = yf.download(ticker, period="1y")

    if data.empty:
        st.error("აქცია ვერ მოიძებნა")
    else:
        close = data["Close"].squeeze()

        price = close.iloc[-1]

        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        st.write("აქცია:", ticker)
        st.write("ბოლო ფასი:", float(price))

        if ma20 > ma50:
            st.success("🟢 BUY სიგნალი")
        elif ma20 < ma50:
            st.error("🔴 SELL სიგნალი")
        else:
            st.warning("🟡 HOLD")

        chart_data = close.to_frame(name="Close")
        chart_data["MA20"] = close.rolling(20).mean()
        chart_data["MA50"] = close.rolling(50).mean()

        st.line_chart(chart_data)
