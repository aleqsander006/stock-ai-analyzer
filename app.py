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


# SIDEBAR PORTFOLIO

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


# MODE

mode = st.radio(
    "აირჩიე რეჟიმი",
    [
        "📈 ერთი აქციის ანალიზი",
        "📊 აქციების შედარება"
    ]
)


tickers_input = st.text_input(
    "შეიყვანე აქციები (მაგ: NVDA,SNDK,MSFT)",
    "NVDA"
)


tickers = [
    x.strip().upper()
    for x in tickers_input.split(",")
]


# SINGLE STOCK

if mode == "📈 ერთი აქციის ანალიზი":

    ticker = tickers[0]

    if st.button("🔍 ანალიზი"):

        data = yf.download(
            ticker,
            period="1y",
            progress=False
        )


        if not data.empty:

            close = data["Close"]

            if isinstance(close, pd.DataFrame):
                close = close.iloc[:,0]


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


            indicators = calculate_indicators(
                close
            )


            col1,col2,col3 = st.columns(3)


            col1.metric(
                "RSI",
                round(float(indicators["RSI"].iloc[-1]),2)
            )

            col2.metric(
                "MA20",
                round(float(indicators["MA20"].iloc[-1]),2)
            )

            col3.metric(
                "MA50",
                round(float(indicators["MA50"].iloc[-1]),2)
            )
                        # COMPANY INFO

            st.subheader(
                "🏢 კომპანიის ინფორმაცია"
            )

            info = get_fundamentals(
                ticker
            )

            st.json(info)


            # CHART

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



# COMPARE MODE

else:

    if st.button("📊 შედარება"):

        comparison = pd.DataFrame()


        for ticker in tickers:

            data = yf.download(
                ticker,
                period="1y",
                progress=False
            )


            if not data.empty:

                close = data["Close"]


                if isinstance(close, pd.DataFrame):
                    close = close.iloc[:,0]


                # პროცენტული ცვლილება
                normalized = (
                    close / close.iloc[0]
                ) * 100


                comparison[ticker] = normalized



        if not comparison.empty:

            st.subheader(
                "📊 აქციების შედარება (1 წელი)"
            )


            st.line_chart(
                comparison
            )


            st.subheader(
                "📈 ბოლო შედეგები"
            )


            results = pd.DataFrame()


            for col in comparison.columns:

                start = comparison[col].iloc[0]
                end = comparison[col].iloc[-1]

                results.loc[col,"ცვლილება %"] = round(
                    end-start,
                    2
                )


            st.dataframe(
                results
                )
