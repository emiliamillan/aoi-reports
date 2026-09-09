import pandas as pd
from datetime import datetime
def load_excel(path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load sheet 1 and sheet 2."""

    #1. Cargar archivo

    sheet_1 = pd.read_excel(path, sheet_name=0, header=1)
    sheet_2 = pd.read_excel(path, sheet_name=1, header=2)

    return sheet_1, sheet_2


def normalize_str(series: pd.Series) -> pd.Series:
    """Normalize STR values."""

    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.lower()
    )


def search_value(df: pd.DataFrame, values: list[str]) -> pd.DataFrame:
    """Search multiple STR values."""

    #2. Buscar STR

    values = normalize_str(pd.Series(values)).dropna()

    return df[normalize_str(df["STR"]).isin(values)]


def add_lot_qty_rejects(
    results: pd.DataFrame,
    sheet_1: pd.DataFrame,
) -> pd.DataFrame:
    """Find Lot, Qty In and Rejects using STR#."""

    results = results.copy()
    sheet_1 = sheet_1.copy()

    results["_STR_LOOKUP"] = normalize_str(results["STR"])
    sheet_1["_STR_LOOKUP"] = normalize_str(sheet_1["STR#"])

    lookup = (
        sheet_1[["_STR_LOOKUP", "Lot", "Qty In", "Rejects"]]
        .drop_duplicates(subset="_STR_LOOKUP")
    )

    results = results.merge(
        lookup,
        on="_STR_LOOKUP",
        how="left",
    )

    results.drop(columns=["_STR_LOOKUP"], inplace=True)

    # Mover las columnas después de STR
    lot_values = results.pop("Lot")
    qty_in_values = results.pop("Qty In")
    rejects_values = results.pop("Rejects")

    position = results.columns.get_loc("STR") + 1

    results.insert(position, "Lot", lot_values)
    results.insert(position + 1, "Qty In", qty_in_values)
    results.insert(position + 2, "Rejects", rejects_values)

    return results


def add_total_row(df: pd.DataFrame) -> pd.DataFrame:
    """Add TOTAL row."""

    #4. Agregar TOTAL

    total = {}

    for column in df.columns:
        if column == "STR":
            total[column] = "TOTAL"
        elif pd.api.types.is_numeric_dtype(df[column]):
            total[column] = df[column].sum()
        else:
            total[column] = ""

    return pd.concat([df, pd.DataFrame([total])], ignore_index=True)


def organize_failure_modes(df: pd.DataFrame) -> pd.DataFrame:
    """Keep top 10 failure modes."""

    #5. Organizar modos de falla

    fixed_columns = list(df.columns[:8])
    failure_columns = list(df.columns[8:])

    totals = pd.to_numeric(
        df.iloc[-1][failure_columns],
        errors="coerce",
    ).fillna(0)

    top_failures = totals.sort_values(ascending=False).head(10)

    failure_columns = [
        column
        for column in top_failures.index
        if top_failures[column] > 0
    ]

    return df[fixed_columns + failure_columns]


def generate_report(
    input_path: str,
    output_path: str,
    values: list[str],
) -> int:
    """Generate the filtered Excel report."""

    #1. Cargar archivo
    sheet_1, sheet_2 = load_excel(input_path)

    #2. Buscar STR
    results = search_value(sheet_2, values)

    if results.empty:
        return 0

    #3. Buscar Lot
    results = add_lot_qty_rejects(results, sheet_1)     

    #4. Agregar TOTAL
    results_with_total = add_total_row(results)

    #5. Organizar modos de falla
    results_with_total = organize_failure_modes(results_with_total)

    #6. Guardar archivo
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        results_with_total.to_excel(
            writer,
            sheet_name="Filtered Results",
            index=False,
        )

    return len(results)