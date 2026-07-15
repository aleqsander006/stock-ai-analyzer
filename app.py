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

        current_rsi = rsi.iloc[-1]

        st.write("RSI:", round(float(current_rsi), 2))

        if current_rsi < 30:
            score += 1
            reasons.append("✅ RSI დაბალია — შესაძლო აღდგენა")
        elif current_rsi > 70:
            score -= 1
            reasons.append("⚠️ RSI მაღალია — შესაძლებელია გადახურება")
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

        # საბოლოო შეფასება
        st.subheader("🤖 საბოლოო შეფასება")

        if score >= 2:
            st.success("🟢 BUY")
        elif score <= -2:
            st.error("🔴 SELL")
        else:
            st.warning("🟡 HOLD")

        st.write("ქულა:", score, "/ 3")

        # Confidence
        confidence = ((score + 3) / 6) * 100

        st.subheader("🎯 AI Confidence")
        st.write("ნდობის დონე:", round(confidence, 1), "%")

        st.write("ანალიზის მიზეზები:")
        for reason in reasons:
            st.write(reason)

        # ისტორიული ზრდის შანსი
        st.subheader("📅 ისტორიული მიმართულება")

        returns = close.pct_change().dropna()

        up_days = (returns > 0).sum()
        total_days = len(returns)

        up_probability = (up_days / total_days) * 100

        st.write("📈 ზრდის ისტორიული შანსი:",
                 round(up_probability, 2), "%")

        st.write("📉 ვარდნის ისტორიული შანსი:",
                 round(100 - up_probability, 2), "%")

        # გრაფიკი
        chart = close.to_frame(name="Close")
        chart["MA20"] = close.rolling(20).mean()
        chart["MA50"] = close.rolling(50).mean()

        st.line_chart(chart)
