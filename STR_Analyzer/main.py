import pandas as pd
from openpyxl.chart import BarChart, LineChart, Reference

def load_excel(path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load sheet 1 and sheet 2 using the correct header rows."""

    sheet_1 = pd.read_excel(
        path,
        sheet_name=0,
        header=1,
    )

    sheet_2 = pd.read_excel(
        path,
        sheet_name=1,
        header=2,
    )

    return sheet_1, sheet_2


def search_value(
    df: pd.DataFrame,
    values: list[str],
) -> pd.DataFrame:
    """Search multiple STR values."""

    values = [
        value.strip().lower()
        for value in values
    ]

    return df[
        df["STR"]
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(values)
    ]


def normalize_str(series: pd.Series) -> pd.Series:
    """
    Normalize STR values so values from Excel can be
    compared reliably between STR and STR#.

    Examples:
        315779       -> 315779
        "315779"     -> 315779
        "315779 "    -> 315779
        315779.0     -> 315779
        "315779.0"   -> 315779
    """

    return (
        series
        .astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.lower()
    )


def add_lote(
    results: pd.DataFrame,
    sheet_1: pd.DataFrame,
) -> pd.DataFrame:
    """Find Lot from sheet 1 using STR#."""

    results = results.copy()
    sheet_1 = sheet_1.copy()

    # ---------------------------------------------------------
    # Normalize STR from Sheet 2
    # ---------------------------------------------------------

    results["_STR_LOOKUP"] = normalize_str(
        results["STR"]
    )

    # ---------------------------------------------------------
    # Normalize STR# from Sheet 1
    # ---------------------------------------------------------

    sheet_1["_STR_LOOKUP"] = normalize_str(
        sheet_1["STR#"]
    )

    # ---------------------------------------------------------
    # DEBUG
    # ---------------------------------------------------------

    print("\n================ DEBUG ================")

    print("\nSTR de resultados (Hoja 2):")
    print(
        results["STR"]
        .head(10)
        .tolist()
    )

    print("\nSTR normalizado (Hoja 2):")
    print(
        results["_STR_LOOKUP"]
        .head(10)
        .tolist()
    )

    print("\nSTR# de hoja 1:")
    print(
        sheet_1["STR#"]
        .head(10)
        .tolist()
    )

    print("\nSTR# normalizado (Hoja 1):")
    print(
        sheet_1["_STR_LOOKUP"]
        .head(10)
        .tolist()
    )

    # ---------------------------------------------------------
    # Check every STR from Sheet 2 against Sheet 1
    # ---------------------------------------------------------

    print("\n================ MATCHES ================")

    unique_strs = (
        results["_STR_LOOKUP"]
        .dropna()
        .unique()
    )

    for value in unique_strs:

        matches = sheet_1[
            sheet_1["_STR_LOOKUP"] == value
        ]

        print(
            f"\nSTR buscado: {value}"
        )

        print(
            f"Matches encontrados: {len(matches)}"
        )

        if not matches.empty:

            print(
                matches[
                    ["STR#", "Lot"]
                ].to_string(index=False)
            )

        else:

            print("NO MATCH")

    # ---------------------------------------------------------
    # Create lookup table
    # ---------------------------------------------------------

    lote_lookup = (
        sheet_1[
            [
                "_STR_LOOKUP",
                "Lot",
            ]
        ]
        .drop_duplicates(
            subset="_STR_LOOKUP"
        )
    )

    # ---------------------------------------------------------
    # Merge STR from Sheet 2 with STR# from Sheet 1
    # ---------------------------------------------------------

    results = results.merge(
        lote_lookup,
        on="_STR_LOOKUP",
        how="left",
    )

    # ---------------------------------------------------------
    # Remove helper column
    # ---------------------------------------------------------

    results.drop(
        columns=["_STR_LOOKUP"],
        inplace=True,
    )

    # ---------------------------------------------------------
    # Move Lot next to STR
    # ---------------------------------------------------------

    lot_values = results.pop("Lot")

    position = (
        results.columns.get_loc("STR") + 1
    )

    results.insert(
        position,
        "Lot",
        lot_values,
    )

    return results


def add_total_row(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Add a TOTAL row with sums for numeric columns."""

    total = {}

    for column in df.columns:

        if column == "STR":

            total[column] = "TOTAL"

        elif pd.api.types.is_numeric_dtype(
            df[column]
        ):

            total[column] = df[column].sum()

        else:

            total[column] = ""

    return pd.concat(
        [
            df,
            pd.DataFrame([total]),
        ],
        ignore_index=True,
    )


def create_pareto(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create Pareto analysis for failure modes in columns I:JA."""

    # Excel column I = position 9
    # Excel column JA = position 244
    # pandas uses zero-based indexes:
    # I  -> 8
    # JA -> 243
    failure_data = df.iloc[:, 8:244].copy()

    # Empty cells are not failures
    failure_data = failure_data.replace(
        r"^\s*$",
        pd.NA,
        regex=True,
    )

    # Count non-empty cells per failure mode
    failure_counts = (
        failure_data
        .notna()
        .sum()
        .sort_values(ascending=False)
    )

    # Keep Top 10
    pareto = (
        failure_counts
        .head(10)
        .reset_index()
    )

    pareto.columns = [
        "Failure Mode",
        "Failures",
    ]

    # Total failures across ALL failure modes
    total_failures = failure_counts.sum()

    if total_failures == 0:

        pareto["Percentage"] = 0.0
        pareto["Cumulative Percentage"] = 0.0

    else:

        pareto["Percentage"] = (
            pareto["Failures"]
            / total_failures
            * 100
        )

        pareto["Cumulative Percentage"] = (
            pareto["Percentage"]
            .cumsum()
        )

    return pareto

def create_pareto_chart(
    pareto: pd.DataFrame,
    writer: pd.ExcelWriter,
) -> None:
    """Write Pareto table and create Pareto chart in Excel."""

    # Get the workbook
    workbook = writer.book

    # Create Pareto worksheet
    worksheet = workbook.create_sheet(
        "Pareto"
    )

    # Write Pareto table
    pareto.to_excel(
        writer,
        sheet_name="Pareto",
        index=False,
    )

    # Re-get worksheet after writing data
    worksheet = writer.sheets["Pareto"]

    # Create bar chart
    bar_chart = BarChart()

    bar_chart.type = "col"
    bar_chart.style = 10
    bar_chart.title = "Pareto - Top 10 Failure Modes"
    bar_chart.y_axis.title = "Failures"
    bar_chart.x_axis.title = "Failure Mode"

    # Failure counts
    failures = Reference(
        worksheet,
        min_col=2,
        min_row=1,
        max_row=len(pareto) + 1,
    )

    # Failure mode names
    categories = Reference(
        worksheet,
        min_col=1,
        min_row=2,
        max_row=len(pareto) + 1,
    )

    bar_chart.add_data(
        failures,
        titles_from_data=True,
    )

    bar_chart.set_categories(
        categories
    )

    # Create cumulative percentage line
    line_chart = LineChart()

    cumulative = Reference(
        worksheet,
        min_col=4,
        min_row=1,
        max_row=len(pareto) + 1,
    )

    line_chart.add_data(
        cumulative,
        titles_from_data=True,
    )

    line_chart.set_categories(
        categories
    )

    line_chart.y_axis.title = "Cumulative %"

    # Percentage axis: 0-100
    line_chart.y_axis.scaling.min = 0
    line_chart.y_axis.scaling.max = 100

    # Put percentage axis on the right
    line_chart.y_axis.axId = 200
    line_chart.y_axis.crosses = "max"

    # Combine charts
    bar_chart += line_chart

    # Add chart to worksheet
    worksheet.add_chart(
        bar_chart,
        "F2",
    )

    # Format columns
    worksheet.column_dimensions[
        "A"
    ].width = 40

    worksheet.column_dimensions[
        "B"
    ].width = 15

    worksheet.column_dimensions[
        "C"
    ].width = 15

    worksheet.column_dimensions[
        "D"
    ].width = 25

def main() -> None:

    path = input(
        "Enter the path to the Excel file: "
    )

    try:

        # ==========================================
        # 1. LOAD EXCEL
        # ==========================================

        sheet_1, sheet_2 = load_excel(path)

        print(
            "\nExcel file loaded successfully!"
        )

        print(
            f"Sheet 1 rows: {len(sheet_1)}"
        )

        print(
            f"Sheet 2 rows: {len(sheet_2)}"
        )

        # ==========================================
        # 2. GET STR VALUES
        # ==========================================

        value = input(
            "\nEnter the STR values to search, "
            "separated by commas: "
        )

        values = value.split(",")

        # ==========================================
        # 3. SEARCH STR
        # ==========================================

        results = search_value(
            sheet_2,
            values,
        )

        print(
            f"\nResults found: {len(results)}"
        )

        if results.empty:

            print(
                "No matching records found."
            )

            return

        # ==========================================
        # 4. ADD LOT
        # ==========================================

        results = add_lote(
            results,
            sheet_1,
        )

        # ==========================================
        # 5. CREATE PARETO
        # ==========================================
        #
        # IMPORTANT:
        # We create the Pareto BEFORE adding
        # the TOTAL row.
        #
        # Otherwise the TOTAL row could be
        # interpreted as a failure.
        #

        pareto = create_pareto(
            results
        )

        # ==========================================
        # 6. ADD TOTAL ROW
        # ==========================================

        results_with_total = add_total_row(
            results
        )

        # ==========================================
        # 7. DISPLAY RESULTS
        # ==========================================

        print(
            "\nMatching records:"
        )

        print(
            results_with_total.to_string(
                index=False
            )
        )

        # ==========================================
        # 8. DISPLAY PARETO
        # ==========================================

        print(
            "\n================ PARETO ================"
        )

        print(
            pareto.to_string(
                index=False
            )
        )

        # ==========================================
        # 9. OUTPUT FILE
        # ==========================================

        output_path = (
            "STR_Analyzer/filtered_results.xlsx"
        )

        # ==========================================
        # 10. CREATE EXCEL FILE
        # ==========================================

        with pd.ExcelWriter(
            output_path,
            engine="openpyxl",
        ) as writer:

            # --------------------------------------
            # Filtered Results sheet
            # --------------------------------------

            results_with_total.to_excel(
                writer,
                sheet_name="Filtered Results",
                index=False,
            )

            # --------------------------------------
            # Pareto sheet + chart
            # --------------------------------------

            create_pareto_chart(
                pareto,
                writer,
            )

        # ==========================================
        # 11. SUCCESS MESSAGE
        # ==========================================

        print(
            "\nResults saved successfully to: "
            f"{output_path}"
        )

        print(
            "\nThe Excel file contains:"
        )

        print(
            "  - Filtered Results"
        )

        print(
            "  - Pareto"
        )

        print(
            "  - Pareto chart"
        )

    # ==============================================
    # ERROR HANDLING
    # ==============================================

    except FileNotFoundError:

        print(
            f"\nError: File not found: {path}"
        )

    except KeyError as e:

        print(
            f"\nError: Missing column: {e}"
        )

    except Exception as e:

        print(
            f"\nError: {e}"
        )

if __name__ == "__main__":
    main()