import yfinance as yf

ticker = "NVDA"

data = yf.download(ticker, period="1y")

last_price = data["Close"].iloc[-1]

ma20 = data["Close"].rolling(20).mean().iloc[-1]
ma50 = data["Close"].rolling(50).mean().iloc[-1]

print("აქცია:", ticker)
print("ბოლო ფასი:", round(float(last_price), 2))

if ma20 > ma50:
    print("სიგნალი: BUY (ზრდის ტენდენცია)")
else:
    print("სიგნალი: HOLD")

print("ანალიზი დასრულდა")
