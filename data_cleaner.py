
import pandas as pd
import re


def standardize_column_names(dataframe):
    """Standardize column names."""

    dataframe = dataframe.copy()

    new_columns = []

    for column in dataframe.columns:

        name = str(column).strip().lower()

        name = re.sub(r"\s+", "_", name)
        name = re.sub(r"[^a-z0-9_]", "", name)
        name = re.sub(r"_+", "_", name).strip("_")

        if not name:
            name = "unnamed_column"

        new_columns.append(name)

    # Ensure column names remain unique.
    counts = {}
    unique_columns = []

    for name in new_columns:
        counts[name] = counts.get(name, 0) + 1

        if counts[name] > 1:
            unique_columns.append(
                f"{name}_{counts[name]}"
            )
        else:
            unique_columns.append(name)

    dataframe.columns = unique_columns

    return dataframe


def convert_data_types(dataframe):
    """Attempt safe automatic conversion of date and numeric columns."""

    dataframe = dataframe.copy()

    for column in dataframe.columns:

        if dataframe[column].dtype == "object":

            values = dataframe[column].dropna()

            if values.empty:
                continue

            # Attempt numeric conversion first.
            numeric_values = pd.to_numeric(
                dataframe[column],
                errors="coerce"
            )

            if numeric_values.notna().sum() == len(values):
                dataframe[column] = numeric_values
                continue

            # Attempt date conversion.
            date_values = pd.to_datetime(
                dataframe[column],
                errors="coerce"
            )

            if date_values.notna().sum() == len(values):
                dataframe[column] = date_values

    return dataframe


def clean_dataset(
    dataframe,
    missing_strategy="Keep",
    remove_duplicates=True
):
    """Clean a business dataset."""

    cleaned = dataframe.copy()

    original_rows = len(cleaned)
    original_columns = len(cleaned.columns)
    original_missing = int(cleaned.isnull().sum().sum())
    original_duplicates = int(cleaned.duplicated().sum())

    # Standardize column names.
    cleaned = standardize_column_names(cleaned)

    # Convert data types.
    cleaned = convert_data_types(cleaned)

    # Remove duplicate rows if requested.
    if remove_duplicates:
        cleaned = cleaned.drop_duplicates()

    # Handle missing values.
    if missing_strategy == "Remove rows":
        cleaned = cleaned.dropna()

    elif missing_strategy == "Fill numeric with zero":
        numeric_columns = cleaned.select_dtypes(
            include="number"
        ).columns

        cleaned[numeric_columns] = cleaned[
            numeric_columns
        ].fillna(0)

    elif missing_strategy == "Fill with mean":
        numeric_columns = cleaned.select_dtypes(
            include="number"
        ).columns

        for column in numeric_columns:
            mean_value = cleaned[column].mean()

            if pd.notna(mean_value):
                cleaned[column] = cleaned[column].fillna(
                    mean_value
                )

    elif missing_strategy == "Fill with median":
        numeric_columns = cleaned.select_dtypes(
            include="number"
        ).columns

        for column in numeric_columns:
            median_value = cleaned[column].median()

            if pd.notna(median_value):
                cleaned[column] = cleaned[column].fillna(
                    median_value
                )

    elif missing_strategy == "Keep":
        pass

    final_information = {
        "original_rows": original_rows,
        "final_rows": len(cleaned),
        "original_columns": original_columns,
        "final_columns": len(cleaned.columns),
        "original_missing": original_missing,
        "final_missing": int(cleaned.isnull().sum().sum()),
        "original_duplicates": original_duplicates,
        "final_duplicates": int(cleaned.duplicated().sum())
    }

    return cleaned, final_information
