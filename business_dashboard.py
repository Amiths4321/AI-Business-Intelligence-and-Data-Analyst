
import streamlit as st
import plotly.express as px


def show_business_dashboard(dataframe, anomalies):

    st.header("📊 Business Intelligence Dashboard")

    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns.tolist()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", len(dataframe))
    col2.metric("Total Columns", len(dataframe.columns))
    col3.metric("Missing Values", int(dataframe.isna().sum().sum()))
    col4.metric("Flagged Anomalies", len(anomalies))

    st.divider()

    if numeric_columns:

        selected_column = st.selectbox(
            "Choose a numeric metric",
            numeric_columns
        )

        total = dataframe[selected_column].sum()
        average = dataframe[selected_column].mean()
        maximum = dataframe[selected_column].max()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total", f"{total:,.2f}")
        col2.metric("Average", f"{average:,.2f}")
        col3.metric("Maximum", f"{maximum:,.2f}")

        chart = px.histogram(
            dataframe,
            x=selected_column,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(chart, use_container_width=True)

    else:
        st.info("No numeric columns are available.")

    st.subheader("Dataset Preview")

    st.dataframe(
        dataframe.head(20),
        use_container_width=True
    )

    st.subheader("Anomaly Review")

    if anomalies.empty:
        st.success("No anomalies were detected by the IQR method.")
    else:
        st.dataframe(
            anomalies,
            use_container_width=True
        )
