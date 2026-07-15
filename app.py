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

        # BUY / SELL სიგნალი
        if ma20 > ma50:
            st.success("🟢 BUY სიგნალი")
        elif ma20 < ma50:
            st.error("🔴 SELL სიგნალი")
        else:
            st.warning("🟡 HOLD")

        # RSI გამოთვლა
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = rsi.iloc[-1]

        st.write("RSI:", round(float(current_rsi), 2))

        if current_rsi > 70:
            st.warning("⚠️ აქცია შეიძლება გადახურებული იყოს")
        elif current_rsi < 30:
            st.success("🟢 აქცია შეიძლება იაფად იყიდებოდეს")
        else:
            st.info("ℹ️ RSI ნეიტრალურ ზონაშია")

        # გრაფიკი
        chart_data = close.to_frame(name="Close")
        chart_data["MA20"] = close.rolling(20).mean()
        chart_data["MA50"] = close.rolling(50).mean()

        st.line_chart(chart_data)
