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


# ---------------- SIDEBAR PORTFOLIO ----------------

st.sidebar.header("💼 ჩემი პორტფელი")

portfolio_input = st.sidebar.text_input(
    "მაგ: NVDA:0.02,AAPL:1.5",
    "NVDA:0.02,AAPL:1"
)


if st.sidebar.button("პორტფელის ნახვა"):

    total, positions = calculate_portfolio(
        portfolio_input
    )

    st.sidebar.subheader("შედეგი")

    for item in positions:
        st.sidebar.write(
            f"{item['Symbol']}: "
            f"{item['Shares']} აქცია = "
            f"${item['Value']}"
        )

    st.sidebar.metric(
        "საერთო ღირებულება",
        f"${total:.2f}"
    )


# ---------------- STOCK SEARCH ----------------


ticker = st.text_input(
    "შეიყვანე აქციის სიმბოლო",
    "NVDA"
)


analyze = st.button(
    "🔍 ანალიზი"
)


if analyze:

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

        close = data["Close"].squeeze()

        price = float(
            close.iloc[-1]
        )


        st.subheader(
            f"🏢 {ticker.upper()}"
        )


        st.metric(
            "მიმდინარე ფასი",
            f"${price:.2f}"
        )
