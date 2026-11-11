
import streamlit as st

from data_manager import (
    load_uploaded_file,
    get_dataset_information
)


def initialize_dataset():
    """Initialize dataset session state."""

    if "dataset" not in st.session_state:
        st.session_state["dataset"] = None

    if "dataset_info" not in st.session_state:
        st.session_state["dataset_info"] = None

    if "dataset_filename" not in st.session_state:
        st.session_state["dataset_filename"] = None


def display_upload_interface():
    """Display dataset upload interface."""

    st.header("📤 Upload Business Dataset")

    uploaded_file = st.file_uploader(
        "Choose an Excel or CSV file",
        type=["csv", "xlsx"],
        accept_multiple_files=False
    )

    if st.button("Load Dataset", type="primary"):

        if uploaded_file is None:
            st.warning("Please select a file first.")

        else:
            try:
                with st.spinner("Loading your dataset..."):

                    dataframe = load_uploaded_file(uploaded_file)

                    if dataframe.empty:
                        st.warning("The uploaded dataset is empty.")

                    elif len(dataframe.columns) == 0:
                        st.warning("No columns were found.")

                    else:
                        st.session_state["dataset"] = dataframe

                        st.session_state["dataset_info"] = (
                            get_dataset_information(dataframe)
                        )

                        st.session_state["dataset_filename"] = (
                            uploaded_file.name
                        )

                        st.success("Dataset loaded successfully!")

            except Exception as error:
                st.error(f"Dataset loading failed: {error}")

    dataframe = st.session_state["dataset"]

    if dataframe is not None:

        st.divider()

        st.subheader("📊 Dataset Preview")

        st.write(
            f"**Filename:** "
            f"{st.session_state['dataset_filename']}"
        )

        st.write(
            f"**File size:** "
            f"{len(uploaded_file.getvalue()) / 1024:.2f} KB"
            if uploaded_file is not None
            else "**File size:** Available after upload"
        )

        st.dataframe(
            dataframe.head(20),
            use_container_width=True
        )

        information = st.session_state["dataset_info"]

        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", information["rows"])
        col2.metric("Columns", information["columns"])
        col3.metric(
            "Missing Values",
            information["missing_values"]
        )
