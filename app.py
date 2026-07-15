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

        score = 0

        # MA20 / MA50
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            score += 1
            st.write("✅ ტენდენცია დადებითია")
        else:
            score -= 1
            st.write("⚠️ ტენდენცია სუსტია")

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

        if current_rsi < 30:
            score += 1
            st.write("✅ RSI დაბალია")
        elif current_rsi > 70:
            score -= 1
            st.write("⚠️ RSI მაღალია")
        else:
            st.write("ℹ️ RSI ნეიტრალურია")

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            score += 1
            st.write("✅ MACD დადებითია")
        else:
            score -= 1
            st.write("⚠️ MACD სუსტია")

        # საბოლოო შეფასება
        st.subheader("🤖 საბოლოო შეფასება")

        st.write("ქულა:", score, "/ 3")

        if score >= 2:
            st.success("🟢 BUY")
        elif score <= -2:
            st.error("🔴 SELL")
        else:
            st.warning("🟡 HOLD")

        chart = close.to_frame(name="Close")
        chart["MA20"] = close.rolling(20).mean()
        chart["MA50"] = close.rolling(50).mean()

        st.line_chart(chart)
