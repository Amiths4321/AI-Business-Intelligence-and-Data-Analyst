
import streamlit as st
import pandas as pd

from ai_data_analyzer import answer_data_question


def display_question_answering():

    st.header("🤖 AI Business Data Analyst")

    dataframe = st.session_state.get("cleaned_dataset")

    if dataframe is None:
        dataframe = st.session_state.get("dataset")

    if dataframe is None:
        st.info("Upload a dataset before asking questions.")
        return

    st.write("Ask questions about your business data in plain English.")

    question = st.text_input(
        "Your business question",
        placeholder="Example: What is the total sales revenue?"
    )

    if st.button("Analyze Question", type="primary"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:

            try:
                with st.spinner(
                    "Qwen is interpreting your question and analyzing data..."
                ):

                    analysis = answer_data_question(
                        dataframe,
                        question
                    )

                st.session_state["latest_analysis"] = analysis

                if "analysis_history" not in st.session_state:
                    st.session_state["analysis_history"] = []

                st.session_state["analysis_history"].append({
                    "Question": question,
                    "Operation": analysis["plan"].get("operation"),
                    "Explanation": analysis["plan"].get("explanation")
                })

            except Exception as error:
                st.error(f"Analysis failed: {error}")

    analysis = st.session_state.get("latest_analysis")

    if analysis:

        st.divider()

        st.subheader("💡 Analysis Result")

        st.write(
            f"**Question:** {analysis['question']}"
        )

        st.write(
            f"**AI explanation:** "
            f"{analysis['plan'].get('explanation', '')}"
        )

        result = analysis["result"]

        if isinstance(result, pd.DataFrame):
            st.dataframe(result, use_container_width=True)

        elif isinstance(result, pd.Series):
            st.dataframe(
                result.rename("Result").reset_index(),
                use_container_width=True
            )

        else:
            st.metric(
                "Calculated Result",
                str(result)
            )

        with st.expander("View AI Analysis Plan"):
            st.json(analysis["plan"])

    st.divider()

    st.subheader("📜 Question History")

    history = st.session_state.get("analysis_history", [])

    if history:
        st.dataframe(
            pd.DataFrame(history),
            use_container_width=True
        )
    else:
        st.info("No questions have been analyzed yet.")
