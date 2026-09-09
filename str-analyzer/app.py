import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from main import generate_report


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("STR Analyzer")
        self.setMinimumSize(700, 500)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Create the application interface."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 20)
        main_layout.setSpacing(15)

        # 1. Título

        title = QLabel("STR Analyzer")
        title.setObjectName("title")

        subtitle = QLabel(
            "Generate filtered Excel reports from STR values."
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # 2. Archivo

        raw_data_label = QLabel("Raw Data Excel")
        raw_data_label.setObjectName("sectionLabel")

        main_layout.addWidget(raw_data_label)

        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText(
            "Select the raw data Excel file..."
        )

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)

        main_layout.addLayout(file_layout)

        # 3. STR Values

        str_label = QLabel("STR Values")
        str_label.setObjectName("sectionLabel")

        main_layout.addWidget(str_label)

        self.str_input = QLineEdit()
        self.str_input.setPlaceholderText(
            "Example: 315779, 315780, 315781"
        )

        main_layout.addWidget(self.str_input)

        # 4. Generar reporte

        self.generate_button = QPushButton("Generate Report")
        self.generate_button.setObjectName("generateButton")
        self.generate_button.setMinimumHeight(45)
        self.generate_button.clicked.connect(self.generate_report)

        main_layout.addWidget(self.generate_button)

        # 5. Status

        status_label = QLabel("Status")
        status_label.setObjectName("sectionLabel")

        main_layout.addWidget(status_label)

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)

        main_layout.addWidget(self.status_box)

        # 6. Espacio flexible

        main_layout.addStretch()

        # 7. Autor

        author_label = QLabel("Author: Emilia Millan \nSeptember 2026")
        author_label.setObjectName("author")

        main_layout.addWidget(author_label)

        self.apply_styles()

    # 1. Seleccionar archivo

    def browse_file(self) -> None:
        """Select the raw data Excel file."""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Raw Data Excel",
            "",
            "Excel Files (*.xlsx *.xls)",
        )

        if file_path:
            self.file_input.setText(file_path)
            self.status_box.append(
                f"File selected: {file_path}"
            )

    # 2. Generar reporte

    def generate_report(self) -> None:
        """Generate the Excel report."""

        input_path = self.file_input.text().strip()
        str_text = self.str_input.text().strip()

        # 1. Validar archivo

        if not input_path:
            QMessageBox.warning(
                self,
                "Missing File",
                "Please select the raw data Excel file.",
            )
            return

        if not Path(input_path).exists():
            QMessageBox.warning(
                self,
                "File Not Found",
                "The selected Excel file does not exist.",
            )
            return

        # 2. Validar STR

        if not str_text:
            QMessageBox.warning(
                self,
                "Missing STR Values",
                "Please enter at least one STR value.",
            )
            return

        # 3. Obtener STR

        values = [
            value.strip()
            for value in str_text.split(",")
            if value.strip()
        ]

        # 4. Seleccionar archivo de salida

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            f"str_report_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx",
            "Excel Files (*.xlsx)",
        )

        if not output_path:
            return

        # 5. Generar reporte

        self.generate_button.setEnabled(False)
        self.status_box.clear()
        self.status_box.append("Processing Excel file...")

        QApplication.processEvents()

        try:
            results_count = generate_report(
                input_path,
                output_path,
                values,
            )

            if results_count == 0:
                self.status_box.append(
                    "No matching records found."
                )

                QMessageBox.information(
                    self,
                    "No Results",
                    "No matching STR records were found.",
                )

                return

            self.status_box.append(
                f"Results found: {results_count}"
            )
            self.status_box.append(
                f"Report saved: {output_path}"
            )

            QMessageBox.information(
                self,
                "Success",
                (
                    "Report generated successfully!\n\n"
                    f"Results: {results_count}\n"
                    f"File: {output_path}"
                ),
            )

        except FileNotFoundError:
            self.status_box.append(
                "Error: File not found."
            )

            QMessageBox.critical(
                self,
                "Error",
                "The Excel file could not be found.",
            )

        except KeyError as e:
            self.status_box.append(
                f"Error: Missing column: {e}"
            )

            QMessageBox.critical(
                self,
                "Missing Column",
                f"Required column not found: {e}",
            )

        except Exception as e:
            self.status_box.append(
                f"Error: {e}"
            )

            QMessageBox.critical(
                self,
                "Error",
                str(e),
            )

        finally:
            self.generate_button.setEnabled(True)

    # 3. Estilos

    def apply_styles(self) -> None:
        """Apply application styling."""

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f5f6f8;
            }

            QLabel#title {
                font-size: 28px;
                font-weight: bold;
                color: #202124;
            }

            QLabel#subtitle {
                font-size: 14px;
                color: #6b7280;
            }

            QLabel#sectionLabel {
                font-size: 14px;
                font-weight: bold;
                color: #374151;
            }

            QLabel#author {
                font-size: 11px;
                color: #9ca3af;
                padding-top: 5px;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
            }

            QPushButton {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #f3f4f6;
            }

            QPushButton#generateButton {
                background-color: #2563eb;
                color: white;
                border: none;
                font-size: 15px;
            }

            QPushButton#generateButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton#generateButton:disabled {
                background-color: #93c5fd;
            }

            QTextEdit {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }
            """
        )


def main() -> None:
    """Application entry point."""

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()