
import pandas as pd


def detect_anomalies(dataframe):
    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    anomaly_results = []

    for column in numeric_columns:

        series = dataframe[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

        mask = (
            (dataframe[column] < lower_limit)
            | (dataframe[column] > upper_limit)
        )

        for row_index in dataframe.index[mask]:

            anomaly_results.append({
                "Row Index": str(row_index),
                "Column": column,
                "Value": dataframe.loc[row_index, column],
                "Lower Limit": lower_limit,
                "Upper Limit": upper_limit
            })

    return pd.DataFrame(anomaly_results)
