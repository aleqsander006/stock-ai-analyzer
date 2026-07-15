import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stock AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock AI Analyzer")

stocks = st.text_input(
    "ჩაწერე აქციები (მაგ: NVDA,AAPL,MSFT)",
    "NVDA,AAPL,MSFT"
)

if st.button("🔍 ანალიზი"):

    tickers = [x.strip().upper() for x in stocks.split(",")]

    results = []
    details = {}

    best_stock = None
    best_score = -99

    for ticker in tickers:

        data = yf.download(ticker, period="1y")

        if data.empty:
            continue

        close = data["Close"].squeeze()

        price = float(close.iloc[-1])

        score = 0
        reasons = []

        # MA
        ma20 = close.rolling(20).mean().iloc[-1]
        ma50 = close.rolling(50).mean().iloc[-1]

        if ma20 > ma50:
            score += 1
            reasons.append("ტენდენცია დადებითია")
        else:
            reasons.append("ტენდენცია სუსტია")

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
            reasons.append("RSI დაბალია")
        elif current_rsi > 70:
            score -= 1
            reasons.append("RSI მაღალია")
        else:
            reasons.append("RSI ნეიტრალურია")

        # MACD
        ema12 = close.ewm(span=12).mean()
        ema26 = close.ewm(span=26).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            score += 1
            reasons.append("MACD დადებითია")
        else:
            reasons.append("MACD სუსტია")

        if score >= 2:
            result = "🟢 BUY"
        elif score <= -1:
            result = "🔴 SELL"
        else:
            result = "🟡 HOLD"

        confidence = ((score + 3) / 6) * 100

        results.append({
            "აქცია": ticker,
            "ფასი": round(price, 2),
            "სიგნალი": result,
            "ქულა": f"{score}/3",
            "Confidence": f"{confidence:.1f}%"
        })

        details[ticker] = reasons

        if score > best_score:
            best_score = score
            best_stock = ticker


    df = pd.DataFrame(results)

    st.subheader("📊 აქციების შედარება")
    st.dataframe(df, use_container_width=True)


    st.divider()

    st.subheader("🤖 AI რეკომენდაცია")

    if best_stock:

        if best_score >= 2:
            st.success(
                f"{best_stock} გამოიყურება ყველაზე ძლიერად 🟢"
            )
        elif best_score <= 0:
            st.warning(
                f"{best_stock}-ს სჭირდება დაკვირვება 🟡"
            )
        else:
            st.info(
                f"{best_stock} ნეიტრალურ მდგომარეობაშია"
            )

        st.write("მიზეზები:")

        for reason in details[best_stock]:
            st.write("•", reason)

    st.warning(
        "⚠️ ეს არის ტექნიკური ანალიზი და არა გარანტირებული ფინანსური რჩევა."
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

        close = chart_data["Close"].squeeze()

        chart = close.to_frame(
            name="ფასი"
        )

        chart["MA20
