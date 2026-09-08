import pandas as pd


class STRAnalyzer:

    def load_data(self, file_path):

        df = pd.read_excel(
            file_path,
            sheet_name="Sheet2",
            header=2
        )

        return df

    def filter_strs(self, df, str_list):

        df["STR"] = df["STR"].astype(str)

        return df[
            df["STR"].isin(str_list)
        ]

    def normalize_defects(self, filtered):

        metadata_cols = [
            "STR",
            "STR Type",
            "Part Number",
            "BU",
            "Technology",
            "Is Development",
            "Yield Day",
            "Week"
        ]

        defect_cols = [
            c for c in filtered.columns
            if c not in metadata_cols
        ]

        records = []

        for _, row in filtered.iterrows():

            for defect in defect_cols:

                qty = row[defect]

                if pd.notna(qty):

                    try:

                        qty = float(qty)

                        if qty > 0:

                            records.append(
                                {
                                    "STR": str(row["STR"]),
                                    "Defect": defect,
                                    "Qty": qty
                                }
                            )

                    except:
                        pass

        return pd.DataFrame(records)

    def build_pareto(self, defect_df):

        pareto = (
            defect_df.groupby("Defect")["Qty"]
            .sum()
            .reset_index()
        )

        pareto = pareto.sort_values(
            "Qty",
            ascending=False
        )

        total = pareto["Qty"].sum()

        pareto["Percent"] = (
            pareto["Qty"] / total * 100
        )

        pareto["CumPercent"] = (
            pareto["Percent"].cumsum()
        )

        return pareto