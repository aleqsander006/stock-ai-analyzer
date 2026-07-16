import pandas as pd

def calculate_indicators(close):

    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9).mean()

    return {
        "MA20": ma20,
        "MA50": ma50,
        "RSI": rsi,
        "MACD": macd,
        "SIGNAL": signal
    }
