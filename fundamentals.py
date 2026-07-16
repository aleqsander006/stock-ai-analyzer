import yfinance as yf
import streamlit as st


@st.cache_data(ttl=3600)
def get_fundamentals(ticker):

    try:
        stock = yf.Ticker(ticker)

        info = stock.get_info()

        return {
            "Company": info.get("longName", ticker),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Country": info.get("country", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Employees": info.get("fullTimeEmployees", "N/A")
        }

    except Exception as e:

        return {
            "Company": ticker,
            "Sector": "N/A",
            "Industry": "N/A",
            "Country": "N/A",
            "Market Cap": "N/A",
            "P/E Ratio": "N/A",
            "EPS": "N/A",
            "Dividend Yield": "N/A",
            "Employees": "N/A",
            "Error": "Yahoo Finance limit reached"
        }
