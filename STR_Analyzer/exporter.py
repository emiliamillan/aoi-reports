import pandas as pd


def export_report(
        raw_df,
        combined_pareto,
        output_path):

    with pd.ExcelWriter(
            output_path,
            engine="xlsxwriter") as writer:

        raw_df.to_excel(
            writer,
            sheet_name="Raw_Data",
            index=False
        )

        combined_pareto.to_excel(
            writer,
            sheet_name="Combined_Pareto",
            index=False
        )

        workbook = writer.book

        header_fmt = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#4472C4",
                "font_color": "white"
            }
        )

        ws = writer.sheets["Raw_Data"]

        for col_num, value in enumerate(raw_df.columns):
            ws.write(
                0,
                col_num,
                value,
                header_fmt
            )

        ws.autofilter(
            0,
            0,
            len(raw_df),
            len(raw_df.columns)-1
        )

        ws.freeze_panes(1, 0)