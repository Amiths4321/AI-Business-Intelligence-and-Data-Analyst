
import streamlit as st

from data_cleaner import clean_dataset


def display_cleaning_interface():

    st.header("🧹 Data Cleaning and Preprocessing")

    dataframe = st.session_state.get("dataset")

    if dataframe is None:
        st.info("Please upload a dataset first.")
        return

    st.subheader("Cleaning Options")

    missing_strategy = st.selectbox(
        "How should missing values be handled?",
        [
            "Keep",
            "Remove rows",
            "Fill numeric with zero",
            "Fill with mean",
            "Fill with median"
        ]
    )

    remove_duplicates = st.checkbox(
        "Remove duplicate rows",
        value=True
    )

    if st.button("Clean Dataset", type="primary"):

        try:
            cleaned_dataframe, information = clean_dataset(
                dataframe,
                missing_strategy=missing_strategy,
                remove_duplicates=remove_duplicates
            )

            st.session_state["cleaned_dataset"] = cleaned_dataframe
            st.session_state["cleaning_information"] = information

            st.success("Dataset cleaned successfully!")

        except Exception as error:
            st.error(f"Data cleaning failed: {error}")

    cleaned_dataframe = st.session_state.get(
        "cleaned_dataset"
    )

    information = st.session_state.get(
        "cleaning_information"
    )

    if cleaned_dataframe is not None and information is not None:

        st.divider()
        st.subheader("📊 Cleaning Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Rows Before",
            information["original_rows"]
        )

        col2.metric(
            "Rows After",
            information["final_rows"]
        )

        col3.metric(
            "Duplicates Removed",
            information["original_duplicates"]
            - information["final_duplicates"]
        )

        col4, col5 = st.columns(2)

        col4.metric(
            "Missing Values Before",
            information["original_missing"]
        )

        col5.metric(
            "Missing Values After",
            information["final_missing"]
        )

        st.subheader("Cleaned Dataset Preview")

        st.dataframe(
            cleaned_dataframe.head(20),
            use_container_width=True
        )

        st.download_button(
            "Download Cleaned CSV",
            data=cleaned_dataframe.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )
