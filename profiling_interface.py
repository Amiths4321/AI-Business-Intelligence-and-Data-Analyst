
import streamlit as st
import plotly.express as px

from data_profiler import (
    profile_dataset,
    get_numeric_summary,
    get_categorical_summary
)


def display_profiling_interface():

    st.header("🔍 Automatic Data Profiling")

    dataframe = st.session_state.get("cleaned_dataset")

    if dataframe is None:
        dataframe = st.session_state.get("dataset")

    if dataframe is None:
        st.info("Please upload a dataset first.")
        return

    if dataframe.empty:
        st.warning("The dataset is empty.")
        return

    try:
        overview, column_profiles = profile_dataset(dataframe)

        st.subheader("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", overview["Total Rows"])
        col2.metric("Total Columns", overview["Total Columns"])
        col3.metric("Duplicate Rows", overview["Duplicate Rows"])

        col4, col5 = st.columns(2)

        col4.metric(
            "Missing Values",
            overview["Total Missing Values"]
        )

        col5.metric(
            "Memory Usage",
            f"{overview['Memory Usage (KB)']} KB"
        )

        st.divider()

        st.subheader("📋 Column Profile")

        st.dataframe(
            column_profiles,
            use_container_width=True
        )

        st.divider()

        st.subheader("📈 Numeric Data Analysis")

        numeric_summary = get_numeric_summary(dataframe)

        if numeric_summary is not None:

            st.dataframe(
                numeric_summary,
                use_container_width=True
            )

            numeric_columns = dataframe.select_dtypes(
                include="number"
            ).columns.tolist()

            selected_column = st.selectbox(
                "Select a numeric column",
                numeric_columns,
                key="profile_numeric_column"
            )

            fig = px.histogram(
                dataframe,
                x=selected_column,
                title=f"Distribution of {selected_column}",
                marginal="box"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No numeric columns found.")

        st.divider()

        st.subheader("📁 Categorical Data Analysis")

        categorical_summary = get_categorical_summary(dataframe)

        if categorical_summary:

            selected_category = st.selectbox(
                "Select a categorical column",
                list(categorical_summary.keys()),
                key="profile_category_column"
            )

            frequency_data = (
                dataframe[selected_category]
                .astype("string")
                .fillna("Missing")
                .value_counts()
                .head(10)
                .reset_index()
            )

            frequency_data.columns = [
                "Category",
                "Count"
            ]

            st.dataframe(
                frequency_data,
                use_container_width=True
            )

            fig = px.bar(
                frequency_data,
                x="Category",
                y="Count",
                title=f"Top Categories: {selected_category}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("No categorical columns found.")

    except Exception as error:
        st.error(f"Data profiling failed: {error}")
