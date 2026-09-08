import sys
import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QTextEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout
)

from analyzer import STRAnalyzer
from exporter import export_report


class STRAnalyzerApp(QWidget):

    def __init__(self):

        super().__init__()

        self.file_path = None

        self.analyzer = STRAnalyzer()

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle(
            "STR Defect Analyzer"
        )

        self.resize(1200, 800)

        layout = QVBoxLayout()

        self.file_label = QLabel(
            "No file selected"
        )

        browse_btn = QPushButton(
            "Select Excel File"
        )

        browse_btn.clicked.connect(
            self.select_file
        )

        self.str_box = QTextEdit()

        self.str_box.setPlaceholderText(
            "Enter STRs\n\n319019\n319331\n319579"
        )

        analyze_btn = QPushButton(
            "Analyze"
        )

        analyze_btn.clicked.connect(
            self.run_analysis
        )

        export_btn = QPushButton(
            "Export Excel Report"
        )

        export_btn.clicked.connect(
            self.export_excel
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            analyze_btn
        )

        button_layout.addWidget(
            export_btn
        )

        self.summary_label = QLabel()

        self.table = QTableWidget()

        layout.addWidget(browse_btn)
        layout.addWidget(self.file_label)
        layout.addWidget(self.str_box)
        layout.addLayout(button_layout)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def select_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Workbook",
            "",
            "Excel Files (*.xlsx)"
        )

        if path:

            self.file_path = path

            self.file_label.setText(path)

    def run_analysis(self):

        if not self.file_path:

            QMessageBox.warning(
                self,
                "Warning",
                "Select a workbook first."
            )
            return

        raw = self.str_box.toPlainText()

        strs = []

        for line in raw.splitlines():

            val = (
                line.strip()
                .replace("STR-", "")
            )

            if val:

                strs.append(val)

        if not strs:

            QMessageBox.warning(
                self,
                "Warning",
                "Enter at least one STR."
            )
            return

        df = self.analyzer.load_data(
            self.file_path
        )

        self.filtered = (
            self.analyzer.filter_strs(
                df,
                strs
            )
        )

        self.defects = (
            self.analyzer.normalize_defects(
                self.filtered
            )
        )

        self.pareto = (
            self.analyzer.build_pareto(
                self.defects
            )
        )

        total_defects = int(
            self.pareto["Qty"].sum()
        )

        top_defect = (
            self.pareto.iloc[0]["Defect"]
        )

        self.summary_label.setText(
            f"""
            STRs Requested: {len(strs)}

            STRs Found:
            {self.filtered.shape[0]}

            Total Defects:
            {total_defects}

            Top Defect:
            {top_defect}
            """
        )

        self.load_table()

    def load_table(self):

        data = self.pareto.head(25)

        self.table.setColumnCount(
            len(data.columns)
        )

        self.table.setRowCount(
            len(data)
        )

        self.table.setHorizontalHeaderLabels(
            data.columns
        )

        for row in range(len(data)):

            for col in range(len(data.columns)):

                value = str(
                    data.iloc[row, col]
                )

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(value)
                )

    def export_excel(self):

        if not hasattr(
                self,
                "pareto"):

            QMessageBox.warning(
                self,
                "Warning",
                "Run analysis first."
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            "STR_Pareto_Report.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not path:
            return

        export_report(
            self.filtered,
            self.pareto,
            path
        )

        QMessageBox.information(
            self,
            "Complete",
            "Report exported successfully."
        )


app = QApplication(sys.argv)

window = STRAnalyzerApp()

window.show()

sys.exit(app.exec())