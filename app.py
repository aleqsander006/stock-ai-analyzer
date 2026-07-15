import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="Stock AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock AI Analyzer")

# ---------------- WATCHLIST ----------------

stocks = st.text_input(
    "აქციები (მაგ: NVDA,AAPL,MSFT)",
    "NVDA,AAPL,MSFT"
)


# ---------------- PORTFOLIO ----------------

st.sidebar.header("💼 ჩემი პორტფელი")

portfolio_input = st.sidebar.text_input(
    "აქციები და რაოდენობა (მაგ: NVDA:10,AAPL:5)",
    "NVDA:10,AAPL:5"
)


if st.button("🔍 სრული ანალიზი"):

    tickers = [x.strip().upper() for x in stocks.split(",")]

    results = []
    details = {}

    best_stock = ""
    best_score = -99


    for ticker in tickers:

        data = yf.download(
            ticker,
            period="1y"
        )

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
            reasons.append("✅ ტენდენცია დადებითია")
        else:
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
            reasons.append("⚠️ MACD სუსტია")


        if score >= 2:
            signal_text = "🟢 BUY"
        elif score <= -1:
            signal_text = "🔴 SELL"
        else:
            signal_text = "🟡 HOLD"


        confidence = ((score + 3) / 6) * 100


        returns = close.pct_change().dropna()

        up_probability = (
            (returns > 0).sum()
            /
            len(returns)
        ) * 100


        results.append({
            "აქცია": ticker,
            "ფასი": round(price,2),
            "სიგნალი": signal_text,
            "ქულა": f"{score}/3",
            "Confidence": f"{confidence:.1f}%",
            "ხვალ ზრდის შანსი": f"{up_probability:.1f}%"
        })


        details[ticker] = reasons


        if score > best_score:
            best_score = score
            best_stock = ticker



    # TABLE

    df = pd.DataFrame(results)

    st.subheader("📊 აქციების შედარება")

    st.dataframe(
        df,
        use_container_width=True
    )



    # AI Recommendation

    st.divider()

    st.subheader("🤖 AI რეკომენდაცია")


    if best_stock:

        st.success(
            f"საუკეთესო არჩევანი: {best_stock}"
        )

        for r in details[best_stock]:
            st.write(r)



    # PORTFOLIO

    st.divider()

    st.subheader("💼 ჩემი პორტფელი")


    total_value = 0


    items = portfolio_input.split(",")


    for item in items:

        try:

            symbol, amount = item.split(":")

            symbol = symbol.strip().upper()

            amount = int(amount)


            data = yf.download(
                symbol,
                period="1d"
            )


            if not data.empty:

                price = float(
                    data["Close"].iloc[-1]
                )

                value = price * amount

                total_value += value


                st.write(
                    f"{symbol}: {amount} აქცია × ${price:.2f} = ${value:.2f}"
                )

        except:
            pass



    st.metric(
        "საერთო პორტფელის ღირებულება",
        f"${total_value:,.2f}"
    )



    # CHART

    st.divider()

    selected = st.selectbox(
        "გრაფიკის აქცია",
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

        chart["MA20"] = close.rolling(20).mean()
        chart["MA50"] = close.rolling(50).mean()


        st.subheader(
            f"📈 {selected} გრაფიკი"
        )

        st.line_chart(chart)
