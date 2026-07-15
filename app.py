KeyError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/stock-ai-analyzer/app.py", line 35, in <module>
    st.line_chart(chart_data[["Close", "MA20", "MA50"]])
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/metrics_util.py", line 568, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/vega_charts.py", line 848, in line_chart
    chart = generate_chart(
        chart_type=ChartType.LINE,
    ...<8 lines>...
        height=height,
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/lib/built_in_chart_utils.py", line 158, in generate_chart
    df, x_column, y_column, color_column, size_column, sort_column = _prep_data(
                                                                     ~~~~~~~~~~^
        df, x_column, y_column_list, color_column, size_column, sort_column
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/lib/built_in_chart_utils.py", line 384, in _prep_data
    selected_data = _drop_unused_columns(
        df, x_column, color_column, size_column, sort_column, *y_column_list
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/lib/built_in_chart_utils.py", line 559, in _drop_unused_columns
    return df[keep]  # type: ignore[no-any-return, unused-ignore]
           ~~^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/core/frame.py", line 4384, in __getitem__
    indexer = self.columns._get_indexer_strict(key, "columns")[1]
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/core/indexes/multi.py", line 3239, in _get_indexer_strict
    self._raise_if_missing(key, indexer, axis_name)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/core/indexes/multi.py", line 3257, in _raise_if_missing
    raise KeyError(f"{keyarr[cmask]} not in index")
