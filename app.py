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

        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            score += 1
            reasons.append("მოკლევადიანი ტენდენცია დადებითია")
        else:
            score -= 1
            reasons.append("მოკლევადიანი ტენდენცია სუსტია")

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
            reasons.append("RSI მიუთითებს შესაძლო იაფ ფასზე")
        elif current_rsi > 70:
            score -= 1
            reasons.append("RSI მაღალია")
        else:
            reasons.append("RSI ნეიტრალურია")

        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            score += 1
            reasons.append("MACD დადებით მოძრაობას აჩვენებს")
        else:
            score -= 1
            reasons.append("MACD სუსტია")

        if score >= 2:
            result = "BUY 🟢"
            explanation = "ინდიკატორების უმეტესობა დადებით სიგნალს აჩვენებს."
        elif score <= -2:
            result = "SELL 🔴"
            explanation = "რამდენიმე ინდიკატორი სუსტ ტენდენციაზე მიუთითებს."
        else:
            result = "HOLD 🟡"
            explanation = "სიგნალები ერთმანეთში იყოფა და საჭიროა დაკვირვება."

        confidence = ((score + 3) / 6) * 100

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 ფასი", f"${price:.2f}")

        with col2:
            st.metric("📌 შეფასება", result)

        with col3:
            st.metric("🎯 Confidence", f"{confidence:.1f}%")

        st.divider()

        st.subheader("🤖 AI ანალიზი")
        st.write(explanation)

        st.subheader("📋 მიზეზები")

        for r in reasons:
            st.write("•", r)

        st.subheader("📈 გრაფიკი")

        chart = close.to_frame(name="Close")
        chart["MA20"] = close.rolling(20).mean()
        chart["MA50"] = close.rolling(50).mean()

        st.line_chart(chart)
