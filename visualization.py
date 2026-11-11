
import plotly.express as px
import pandas as pd


def create_chart(dataframe, chart_type, x_column, y_column=None):
    if x_column not in dataframe.columns:
        raise ValueError("Invalid X-axis column.")

    if y_column and y_column not in dataframe.columns:
        raise ValueError("Invalid Y-axis column.")

    if chart_type == "Bar":
        if not y_column:
            raise ValueError("Select a Y-axis column.")
        return px.bar(dataframe, x=x_column, y=y_column)

    if chart_type == "Line":
        if not y_column:
            raise ValueError("Select a Y-axis column.")
        return px.line(dataframe, x=x_column, y=y_column, markers=True)

    if chart_type == "Scatter":
        if not y_column:
            raise ValueError("Select a Y-axis column.")
        return px.scatter(dataframe, x=x_column, y=y_column)

    if chart_type == "Histogram":
        return px.histogram(dataframe, x=x_column)

    if chart_type == "Box":
        return px.box(dataframe, x=x_column)

    if chart_type == "Pie":
        counts = (
            dataframe[x_column]
            .astype("string")
            .fillna("Missing")
            .value_counts()
            .head(15)
            .rename_axis(x_column)
            .reset_index(name="Count")
        )
        return px.pie(counts, names=x_column, values="Count")

    raise ValueError("Unsupported chart type.")
