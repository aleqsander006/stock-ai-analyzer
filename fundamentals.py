import streamlit as st


@st.cache_data(ttl=3600)
def get_fundamentals(ticker):

    return {
        "Company": ticker,
        "Sector": "Loading later",
        "Industry": "Loading later",
        "Country": "N/A",
        "Market Cap": "N/A",
        "P/E Ratio": "N/A",
        "EPS": "N/A",
        "Dividend Yield": "N/A",
        "Employees": "N/A"
    }
