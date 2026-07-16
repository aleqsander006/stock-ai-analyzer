import streamlit as st
import yfinance as yf
import pandas as pd

from indicators import calculate_indicators
from fundamentals import get_fundamentals
from portfolio import calculate_portfolio
from ai_score import calculate_score


st.set_page_config(
    page_title="Stock AI Analyzer Pro",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Stock AI Analyzer Pro")


# =====================
# PORTFOLIO
# =====================

st.sidebar.header("💼 ჩემი პორტფელი")

portfolio_input = st.sidebar.text_input(
    "მაგ: NVDA:0.02,AAPL:1",
    "NVDA:0.02"
)


if st.sidebar.button("პორტფელის ნახვა"):

    total, positions = calculate_portfolio(
        portfolio_input
    )

    for p in positions:
        st.sidebar.write(
            f"{p['Symbol']} - {p['Shares']} აქცია"
        )

    st.sidebar.metric(
        "სულ ღირებულება",
        f"${total:.2f}"
    )



# =====================
# MODE
# =====================

mode = st.radio(
    "რეჟიმი",
    [
        "📈 ერთი აქცია",
        "📊 შედარება"
    ]
)


tickers_text = st.text_input(
    "აქციები (მაგ: NVDA,SNDK,MSFT)",
    "NVDA"
)


tickers = [
    x.strip().upper()
    for x in tickers_text.split(",")
]



# =====================
# SINGLE STOCK
# =====================

if mode == "📈 ერთი აქცია":

    ticker = tickers[0]


    if st.button("ანალიზი"):

        data = yf.download(
            ticker,
            period="1y",
            progress=False
        )


        if data.empty:

            st.error(
                "აქცია ვერ მოიძებნა"
            )

        else:

            close = data["Close"]

            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]


            price = float(
                close.iloc[-1]
            )


            st.subheader(
                f"🏢 {ticker}"
            )


            st.metric(
                "ფასი",
                f"${price:.2f}"
            )


            indicators = calculate_indicators(
                close
            )


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "RSI",
                round(float(indicators["RSI"].iloc[-1]), 2)
            )


            col2.metric(
                "MA20",
                round(float(indicators["MA20"].iloc[-1]), 2)
            )


            col3.metric(
                "MA50",
                round(float(indicators["MA50"].iloc[-1]), 2)
            )



            # AI SCORE

            score, signal = calculate_score(
                close,
                indicators
            )


            st.subheader(
                "⭐ AI Score"
            )


            st.metric(
                "ქულა",
                f"{score}/100"
            )


            st.write(
                signal
            )



            # INFO

            st.subheader(
                "🏢 ინფორმაცია"
            )


            st.json(
                get_fundamentals(ticker)
            )



            # CHART

            chart = pd.DataFrame()

            chart["Price"] = close
            chart["MA20"] = indicators["MA20"]
            chart["MA50"] = indicators["MA50"]


            st.subheader(
                "📈 გრაფიკი"
            )


            st.line_chart(
                chart
            )



# =====================
# COMPARE STOCKS
# =====================

else:


    if st.button("შედარება"):


        chart = pd.DataFrame()

        scores = []


        for ticker in tickers:


            data = yf.download(
                ticker,
                period="1y",
                progress=False
            )


            if not data.empty:


                close = data["Close"]


                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:, 0]


                normalized = (
                    close / close.iloc[0]
                ) * 100


                chart[ticker] = normalized



                indicators = calculate_indicators(
                    close
                )


                score, signal = calculate_score(
                    close,
                    indicators
                )


                scores.append(
                    {
                        "აქცია": ticker,
                        "AI Score": score,
                        "სიგნალი": signal
                    }
                )



        if not chart.empty:


            st.subheader(
                "📊 1 წლის შედარება"
            )


            st.line_chart(
                chart
            )



            st.subheader(
                "⭐ AI რეიტინგი"
            )


            result = pd.DataFrame(
                scores
            )


            result = result.sort_values(
                "AI Score",
                ascending=False
            )


            st.dataframe(
                result
            )


            best = result.iloc[0]


            st.success(
                f"🏆 საუკეთესო: {best['აქცია']} - {best['AI Score']}/100"
            )
