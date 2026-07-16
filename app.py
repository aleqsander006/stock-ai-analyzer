        st.sidebar.write(
            f"{p['Symbol']} - {p['Shares']} აქცია"
        )

    st.sidebar.metric(
        "ღირებულება",
        f"${total:.2f}"
    )


# ---------------- MODE ----------------

mode = st.radio(
    "რეჟიმი",
    [
        "📈 ერთი აქცია",
        "📊 შედარება"
    ]
)


tickers_text = st.text_input(
    "აქციები (მაგ: NVDA,SNDK,MSFT)",
    "NVDA"
)


tickers = [
    x.strip().upper()
    for x in tickers_text.split(",")
]


# ---------------- SINGLE ----------------

if mode == "📈 ერთი აქცია":


    ticker = tickers[0]


    if st.button("ანალიზი"):


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

            if isinstance(close, pd.DataFrame):
                close = close.iloc[:,0]


            price = float(
                close.iloc[-1]
            )


            st.subheader(
                f"🏢 {ticker}"
            )


            st.metric(
                "ფასი",
                f"${price:.2f}"
            )


            indicators = calculate_indicators(
                close
            )


            c1,c2,c3 = st.columns(3)


            c1.metric(
                "RSI",
                round(float(indicators["RSI"].iloc[-1]),2)
            )


            c2.metric(
                "MA20",
                round(float(indicators["MA20"].iloc[-1]),2)
            )


            c3.metric(
                "MA50",
                round(float(indicators["MA50"].iloc[-1]),2)
            )


            st.subheader(
                "🏢 ინფორმაცია"
            )


            st.json(
                get_fundamentals(ticker)
            )


            chart = pd.DataFrame()

            chart["Price"] = close
            chart["MA20"] = indicators["MA20"]
            chart["MA50"] = indicators["MA50"]


            st.subheader(
                "📈 გრაფიკი"
            )

            st.line_chart(chart)



# ---------------- COMPARE ----------------


else:


    if st.button("შედარება"):


        chart = pd.DataFrame()


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


                normalized = (
                    close / close.iloc[0]
                ) * 100


                chart[ticker] = normalized



        if not chart.empty:


            st.subheader(
                "📊 1 წლის შედარება"
            )


            st.line_chart(
                chart
            )
