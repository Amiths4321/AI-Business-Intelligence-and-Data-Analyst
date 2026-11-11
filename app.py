
import streamlit as st
import plotly.express as px

from config import APP_TITLE

from data_interface import (
    initialize_dataset,
    display_upload_interface
)

from cleaning_interface import display_cleaning_interface
from profiling_interface import display_profiling_interface
from qa_interface import display_question_answering

from visualization import create_chart
from business_insights import generate_business_insights
from anomaly_detector import detect_anomalies

from report_generator import (
    generate_excel_report,
    generate_pdf_report
)

from business_dashboard import show_business_dashboard


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Business Intelligence Analyst")

st.write(
    "Upload business datasets, ask questions, "
    "discover insights, detect anomalies, and generate reports."
)

initialize_dataset()

if "business_insights" not in st.session_state:
    st.session_state["business_insights"] = None

if "anomalies" not in st.session_state:
    st.session_state["anomalies"] = None


st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Choose a section",
    [
        "Dataset Upload",
        "Data Cleaning",
        "Data Profiling",
        "AI Data Question Answering",
        "Charts and Visualizations",
        "Business Insights",
        "Anomaly Detection",
        "Dashboard",
        "Reports"
    ]
)


# Use cleaned data when available.
dataframe = st.session_state.get("cleaned_dataset")

if dataframe is None:
    dataframe = st.session_state.get("dataset")


# --------------------------------------------------
# DATASET UPLOAD
# --------------------------------------------------

if section == "Dataset Upload":

    display_upload_interface()


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

elif section == "Data Cleaning":

    display_cleaning_interface()


# --------------------------------------------------
# DATA PROFILING
# --------------------------------------------------

elif section == "Data Profiling":

    display_profiling_interface()


# --------------------------------------------------
# AI QUESTION ANSWERING
# --------------------------------------------------

elif section == "AI Data Question Answering":

    display_question_answering()


# --------------------------------------------------
# CHARTS AND VISUALIZATIONS
# --------------------------------------------------

elif section == "Charts and Visualizations":

    st.header("📈 Charts and Visualizations")

    if dataframe is None:
        st.info("Upload a dataset first.")

    else:

        chart_type = st.selectbox(
            "Chart type",
            ["Bar", "Line", "Scatter", "Histogram", "Box", "Pie"]
        )

        columns = dataframe.columns.tolist()

        x_column = st.selectbox(
            "Select X-axis or category",
            columns
        )

        y_column = None

        if chart_type in ["Bar", "Line", "Scatter"]:

            numeric_columns = dataframe.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:
                y_column = st.selectbox(
                    "Select Y-axis",
                    numeric_columns
                )
            else:
                st.warning("No numeric columns are available.")

        if st.button("Generate Chart", type="primary"):

            try:
                figure = create_chart(
                    dataframe,
                    chart_type,
                    x_column,
                    y_column
                )

                st.session_state["generated_chart"] = figure

            except Exception as error:
                st.error(f"Chart generation failed: {error}")

        if st.session_state.get("generated_chart") is not None:

            st.plotly_chart(
                st.session_state["generated_chart"],
                use_container_width=True
            )


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

elif section == "Business Insights":

    st.header("💡 AI Business Insights")

    if dataframe is None:
        st.info("Upload a dataset first.")

    else:

        if st.button("Generate Business Insights", type="primary"):

            try:
                with st.spinner("Analyzing business data with Qwen..."):

                    result = generate_business_insights(dataframe)

                st.session_state["business_insights"] = result

            except Exception as error:
                st.error(f"Insight generation failed: {error}")

        result = st.session_state.get("business_insights")

        if result:

            st.subheader("AI Analysis")

            st.write(result["insights"])

            st.subheader("Calculated Statistics")

            st.json(result["statistics"])


# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

elif section == "Anomaly Detection":

    st.header("🚨 Anomaly Detection")

    if dataframe is None:
        st.info("Upload a dataset first.")

    else:

        if st.button("Detect Anomalies", type="primary"):

            try:
                anomalies = detect_anomalies(dataframe)

                st.session_state["anomalies"] = anomalies

                st.success(
                    f"Detection completed. "
                    f"{len(anomalies)} unusual values flagged."
                )

            except Exception as error:
                st.error(f"Anomaly detection failed: {error}")

        anomalies = st.session_state.get("anomalies")

        if anomalies is not None:

            if anomalies.empty:
                st.success("No anomalies detected.")

            else:
                st.dataframe(
                    anomalies,
                    use_container_width=True
                )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

elif section == "Dashboard":

    st.header("📊 Business Dashboard")

    if dataframe is None:
        st.info("Upload a dataset first.")

    else:

        anomalies = st.session_state.get("anomalies")

        if anomalies is None:
            anomalies = detect_anomalies(dataframe)

        show_business_dashboard(
            dataframe,
            anomalies
        )


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif section == "Reports":

    st.header("📥 Business Reports")

    if dataframe is None:
        st.info("Upload a dataset before generating reports.")

    else:

        anomalies = st.session_state.get("anomalies")

        if anomalies is None:
            anomalies = detect_anomalies(dataframe)

        insight_result = st.session_state.get("business_insights")

        insights_text = (
            insight_result["insights"]
            if insight_result
            else "Business insights have not been generated yet."
        )

        try:

            excel_file = generate_excel_report(
                dataframe,
                anomalies,
                insights_text
            )

            pdf_file = generate_pdf_report(
                dataframe,
                anomalies,
                insights_text
            )

            st.download_button(
                "📊 Download Excel Report",
                data=excel_file,
                file_name="business_intelligence_report.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

            st.download_button(
                "📄 Download PDF Report",
                data=pdf_file,
                file_name="business_intelligence_report.pdf",
                mime="application/pdf"
            )

        except Exception as error:
            st.error(f"Report generation failed: {error}")
