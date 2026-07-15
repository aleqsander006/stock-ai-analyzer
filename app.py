import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stock AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock AI Analyzer v2")

stocks = st.text_input(
    "Watchlist (მაგ: NVDA,AAPL,MSFT,TSLA)",
    "NVDA,AAPL,MSFT"
)

if st.button("🔍 სრული ანალიზი"):

    tickers = [x.strip().upper() for x in stocks.split(",")]

    results = []

    best_stock = ""
    best_score = -99

    for ticker in tickers:

        data = yf.download(ticker, period="1y")

        if data.empty:
            continue

        close = data["Close"].squeeze()

        price = float(close.iloc[-1])

        # დღიური ცვლილება
        daily_change = (
            (close.iloc[-1] - close.iloc[-2])
            / close.iloc[-2]
        ) * 100

        score = 0

        # MA
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            score += 1

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
        elif current_rsi > 70:
            score -= 1

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            score += 1

        if score >= 2:
            signal_text = "🟢 BUY"
        elif score <= -2:
            signal_text = "🔴 SELL"
        else:
            signal_text = "🟡 HOLD"

        confidence = ((score + 3) / 6) * 100

        results.append({
            "აქცია": ticker,
            "ფასი": round(price, 2),
            "დღე %": round(daily_change, 2),
            "RSI": round(current_rsi, 2),
            "სიგნალი": signal_text,
            "ქულა": f"{score}/3",
            "Confidence": f"{confidence:.1f}%"
        })

        if score > best_score:
            best_score = score
            best_stock = ticker


    df = pd.DataFrame(results)

    st.subheader("📊 აქციების შედარება")
    st.dataframe(df, use_container_width=True)


    st.subheader("🏆 საუკეთესო არჩევანი")

    if best_stock:
        st.success(
            f"საუკეთესო ამ სიიდან: {best_stock} "
            f"(ქულა {best_score}/3)"
        )


    selected = st.selectbox(
        "აირჩიე გრაფიკისთვის",
        tickers
    )


    chart_data = yf.download(
        selected,
        period="1y"
    )

    if not chart_data.empty:

        chart_close = chart_data["Close"].squeeze()

        chart = chart_close.to_frame(
            name="Close"
        )

        chart["MA20"] = chart_close.rolling(20).mean()
        chart["MA50"] = chart_close.rolling(50).mean()

        st.subheader(
            f"📈 {selected} გრაფიკი"
        )

        st.line_chart(chart)
