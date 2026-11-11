
import pandas as pd
from io import BytesIO


def load_uploaded_file(uploaded_file):
    """Load an uploaded CSV or Excel file into a DataFrame."""

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if filename.endswith(".csv"):
        try:
            dataframe = pd.read_csv(BytesIO(file_bytes))
        except UnicodeDecodeError:
            dataframe = pd.read_csv(
                BytesIO(file_bytes),
                encoding="latin-1"
            )

    elif filename.endswith(".xlsx"):
        dataframe = pd.read_excel(
            BytesIO(file_bytes),
            engine="openpyxl"
        )

    else:
        raise ValueError(
            "Unsupported file format. Upload CSV or XLSX."
        )

    return dataframe


def get_dataset_information(dataframe):
    """Return basic dataset information."""

    return {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": dataframe.columns.tolist(),
        "missing_values": int(dataframe.isnull().sum().sum()),
        "duplicate_rows": int(dataframe.duplicated().sum())
    }
