import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Stock AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock AI Analyzer")

ticker = st.text_input("აქციის სიმბოლო", "NVDA")

if st.button("🔍 ანალიზი"):

    data = yf.download(ticker, period="1y")

    if data.empty:
        st.error("აქცია ვერ მოიძებნა")

    else:
        close = data["Close"].squeeze()
        price = float(close.iloc[-1])

        score = 0
        reasons = []

        # MA
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            score += 1
            reasons.append("✅ ტენდენცია დადებითია")
        else:
            score -= 1
            reasons.append("⚠️ ტენდენცია სუსტია")

        # RSI
        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        current_rsi = float(rsi.iloc[-1])

        if current_rsi < 30:
            score += 1
            reasons.append("✅ RSI დაბალია")
        elif current_rsi > 70:
            score -= 1
            reasons.append("⚠️ RSI მაღალია")
        else:
            reasons.append("ℹ️ RSI ნეიტრალურია")

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            score += 1
            reasons.append("✅ MACD დადებითია")
        else:
            score -= 1
            reasons.append("⚠️ MACD სუსტია")

        # Dashboard
        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 ბოლო ფასი", f"${price:.2f}")

        with col2:
            if score >= 2:
                signal_text = "BUY 🟢"
            elif score <= -2:
                signal_text = "SELL 🔴"
            else:
                signal_text = "HOLD 🟡"

            st.metric("სიგნალი", signal_text)

        with col3:
            confidence = ((score + 3) / 6) * 100
            st.metric("AI Confidence", f"{confidence:.1f}%")

        st.divider()

        st.subheader("📊 ინდიკატორები")
        st.write("RSI:", round(current_rsi, 2))
        st.write("ქულა:", score, "/ 3")

        st.subheader("🧠 ანალიზის მიზეზები")

        for reason in reasons:
            st.write(reason)

        st.subheader("📈 ფასის მოძრაობა")

        chart = close.to_frame(name="Close")
        chart["MA20"] = close.rolling(20).mean()
        chart["MA50"] = close.rolling(50).mean()

        st.line_chart(chart)
