def calculate_score(close, indicators):

    score = 50


    rsi = float(
        indicators["RSI"].iloc[-1]
    )

    price = float(
        close.iloc[-1]
    )

    ma20 = float(
        indicators["MA20"].iloc[-1]
    )

    ma50 = float(
        indicators["MA50"].iloc[-1]
    )


    # RSI
    if 40 <= rsi <= 70:
        score += 15

    elif rsi < 30:
        score += 5

    elif rsi > 80:
        score -= 10


    # MA20
    if price > ma20:
        score += 15
    else:
        score -= 10


    # MA50
    if price > ma50:
        score += 15
    else:
        score -= 10


    # Limit
    score = max(0, min(100, score))


    if score >= 70:
        signal = "🟢 BUY"

    elif score >= 45:
        signal = "🟡 HOLD"

    else:
        signal = "🔴 SELL"


    return score, signal
