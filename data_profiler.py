
import pandas as pd


def profile_dataset(dataframe):
    """Generate a comprehensive dataset profile."""

    if dataframe is None or dataframe.empty:
        raise ValueError("Dataset is empty or unavailable.")

    total_rows = len(dataframe)
    total_columns = len(dataframe.columns)

    column_profiles = []

    for column in dataframe.columns:

        series = dataframe[column]

        missing_count = int(series.isna().sum())

        profile = {
            "Column": str(column),
            "Data Type": str(series.dtype),
            "Missing Values": missing_count,
            "Missing Percentage": round(
                (missing_count / total_rows) * 100, 2
            ),
            "Unique Values": int(series.nunique(dropna=True))
        }

        if pd.api.types.is_numeric_dtype(series):

            profile.update({
                "Mean": round(float(series.mean()), 2)
                if series.notna().any() else None,

                "Median": round(float(series.median()), 2)
                if series.notna().any() else None,

                "Minimum": float(series.min())
                if series.notna().any() else None,

                "Maximum": float(series.max())
                if series.notna().any() else None,

                "Standard Deviation": round(float(series.std()), 2)
                if series.notna().any() else None
            })

        elif pd.api.types.is_datetime64_any_dtype(series):

            profile.update({
                "Earliest Date": str(series.min())
                if series.notna().any() else None,

                "Latest Date": str(series.max())
                if series.notna().any() else None
            })

        else:

            top_values = (
                series.dropna()
                .astype(str)
                .value_counts()
                .head(5)
                .to_dict()
            )

            profile["Top 5 Values"] = str(top_values)

        column_profiles.append(profile)

    overview = {
        "Total Rows": total_rows,
        "Total Columns": total_columns,
        "Duplicate Rows": int(dataframe.duplicated().sum()),
        "Total Missing Values": int(dataframe.isna().sum().sum()),
        "Memory Usage (KB)": round(
            dataframe.memory_usage(deep=True).sum() / 1024,
            2
        )
    }

    return overview, pd.DataFrame(column_profiles)


def get_numeric_summary(dataframe):
    """Return descriptive statistics for numeric columns."""

    numeric_data = dataframe.select_dtypes(
        include="number"
    )

    if numeric_data.empty:
        return None

    return numeric_data.describe().T


def get_categorical_summary(dataframe):
    """Return frequency summaries for categorical columns."""

    categorical_data = dataframe.select_dtypes(
        include=["object", "category", "bool"]
    )

    summaries = {}

    for column in categorical_data.columns:

        summaries[column] = (
            categorical_data[column]
            .value_counts(dropna=False)
            .head(10)
        )

    return summaries
