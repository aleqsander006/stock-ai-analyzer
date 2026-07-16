import yfinance as yf


def get_fundamentals(ticker):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info


        return {
            "Company": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Country": info.get("country", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "EPS": info.get("trailingEps", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Employees": info.get("fullTimeEmployees", "N/A")
        }


    except Exception:

        return {
            "Company": ticker,
            "Sector": "Unavailable",
            "Industry": "Unavailable",
            "Country": "Unavailable",
            "Market Cap": "Unavailable",
            "P/E Ratio": "Unavailable",
            "EPS": "Unavailable",
            "Dividend Yield": "Unavailable",
            "Employees": "Unavailable"
        }
