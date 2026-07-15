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

        st.write("აქცია:", ticker)
        st.write("ბოლო ფასი:", float(price))

        # MA20 / MA50
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            st.success("🟢 BUY სიგნალი (MA)")
        else:
            st.error("🔴 SELL სიგნალი (MA)")

        # RSI
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = rsi.iloc[-1]

        st.write("RSI:", round(float(current_rsi), 2))

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        current_macd = macd.iloc[-1]
        current_signal = signal.iloc[-1]

        st.write("MACD:", round(float(current_macd), 3))

        if current_macd > current_signal:
            st.success("🟢 MACD: დადებითი ტენდენცია")
        else:
            st.warning("🟡 MACD: სუსტი ტენდენცია")

        # გრაფიკი
        chart_data = close.to_frame(name="Close")
        chart_data["MA20"] = ma20
        chart_data["MA50"] = ma50

        st.line_chart(chart_data)
