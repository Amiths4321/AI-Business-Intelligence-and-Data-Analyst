
from io import BytesIO
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from xml.sax.saxutils import escape


def generate_excel_report(dataframe, anomalies, insights):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        dataframe.to_excel(
            writer,
            sheet_name="Dataset",
            index=False
        )

        anomalies.to_excel(
            writer,
            sheet_name="Anomalies",
            index=False
        )

        numeric = dataframe.select_dtypes(include="number")

        numeric.describe().to_excel(
            writer,
            sheet_name="Statistics"
        )

        pd.DataFrame({
            "Business Insights": [insights]
        }).to_excel(
            writer,
            sheet_name="Insights",
            index=False
        )

        for worksheet in writer.sheets.values():
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for cells in worksheet.columns:
                width = max(
                    len(str(cell.value or ""))
                    for cell in cells
                )
                worksheet.column_dimensions[
                    cells[0].column_letter
                ].width = min(width + 2, 45)

    output.seek(0)
    return output


def generate_pdf_report(dataframe, anomalies, insights):
    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("Business Intelligence Report", styles["Title"])
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph(
            f"Total rows: {len(dataframe)} | "
            f"Total columns: {len(dataframe.columns)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("Numeric Summary", styles["Heading2"])
    )

    numeric = dataframe.select_dtypes(include="number")

    if not numeric.empty:

        summary = numeric.describe().round(2).reset_index()

        table_data = [
            [str(value) for value in summary.columns]
        ]

        for _, row in summary.iterrows():
            table_data.append([
                str(value) for value in row.tolist()
            ])

        table = Table(table_data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        story.append(table)

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("Anomaly Findings", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Number of flagged values: {len(anomalies)}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    story.append(
        Paragraph("Business Insights", styles["Heading2"])
    )

    for line in insights.splitlines():

        safe_line = escape(line.strip())

        if safe_line:
            story.append(
                Paragraph(safe_line, styles["BodyText"])
            )
            story.append(Spacer(1, 0.08 * inch))

    document.build(story)

    output.seek(0)
    return output
