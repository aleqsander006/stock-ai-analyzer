import yfinance as yf

def calculate_portfolio(portfolio_input):
    total_value = 0
    positions = []

    if not portfolio_input.strip():
        return total_value, positions

    for item in portfolio_input.split(","):
        try:
            symbol, amount = item.split(":")
            symbol = symbol.strip().upper()
            amount = float(amount)

            data = yf.download(symbol, period="1d", progress=False)

            if data.empty:
                continue

            price = float(data["Close"].iloc[-1])
            value = price * amount

            total_value += value

            positions.append({
                "Symbol": symbol,
                "Shares": amount,
                "Price": round(price, 2),
                "Value": round(value, 2)
            })

        except Exception:
            continue

    return total_value, positions
