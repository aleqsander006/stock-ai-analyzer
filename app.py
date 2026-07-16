import streamlit as st
import yfinance as yf
import pandas as pd

from indicators import calculate_indicators
from fundamentals import get_fundamentals
from portfolio import calculate_portfolio


st.set_page_config(
    page_title="Stock AI Analyzer Pro",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Stock AI Analyzer Pro")


# ---------------- PORTFOLIO ----------------

st.sidebar.header("💼 ჩემი პორტფელი")

portfolio_input = st.sidebar.text_input(
    "მაგ: NVDA:0.02,AAPL:1",
    "NVDA:0.02,AAPL:1"
)


if st.sidebar.button("პორტფელის ნახვა"):

    total, positions = calculate_portfolio(
        portfolio_input
    )

    st.sidebar.subheader("შედეგი")

    for item in positions:
        st.sidebar.write(
            f"{item['Symbol']} - "
            f"{item['Shares']} აქცია = "
            f"${item['Value']}"
        )

    st.sidebar.metric(
        "სულ ღირებულება",
        f"${total:.2f}"
    )


# ---------------- STOCK ANALYSIS ----------------

ticker = st.text_input(
    "შეიყვანე აქციის სიმბოლო",
    "NVDA"
)


if st.button("🔍 ანალიზი"):

    ticker = ticker.upper().strip()

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

        # yfinance-ის ახალი ფორმატის დაცვა
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]


        price = float(
            close.iloc[-1]
        )


        st.subheader(
            f"🏢 {ticker}"
        )


        st.metric(
            "მიმდინარე ფასი",
            f"${price:.2f}"
        )


        # Indicators

        indicators = calculate_indicators(
            close
        )


        st.subheader(
            "📊 ტექნიკური ანალიზი"
        )


        col1, col2, col3 = st.columns(3)


        with col1:
            st.write(
                "RSI:",
                round(
                    float(indicators["RSI"].iloc[-1]),
                    2
                )
            )


        with col2:
            st.write(
                "MA20:",
                round(
                    float(indicators["MA20"].iloc[-1]),
                    2
                )
            )


        with col3:
            st.write(
                "MA50:",
                round(
                    float(indicators["MA50"].iloc[-1]),
                    2
                )
            )


        # Company info

        st.subheader(
            "🏢 კომპანიის ინფორმაცია"
        )


        info = get_fundamentals(
            ticker
        )


        st.json(info)


        # Chart

        st.subheader(
            "📈 1 წლის გრაფიკი"
        )


        chart = pd.DataFrame()

        chart["ფასი"] = close
        chart["MA20"] = indicators["MA20"]
        chart["MA50"] = indicators["MA50"]


        st.line_chart(
            chart
        )
