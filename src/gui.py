import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
)
from ocrspace_client import Configuration, RunClient

def RunOCR(file: str) -> str:
    ocr_config = Configuration()

    ocr_config.SetImageFilePath(file)
    ocr_config.SetOCREngineNumber(3)
    ocr_config.SetLanguage("eng")
    ocr_config.SetScale(True)

    return RunClient(ocr_config)

# PRIMARY GUI WINDOW CLASS
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handwriting Recognition")
        self.resize(900, 600)

        self.image_file_path = ""

        self.SetupGUI()
        self.ApplyStyles()
        self.ConnectSignals()

    def SetupGUI(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # file input section
        file_section_layout = QHBoxLayout()
        file_section_layout.setSpacing(8)

        file_label = QLabel("Input File:")
        file_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.file_path_field = QLineEdit()
        self.file_path_field.setReadOnly(True)
        self.file_path_field.setPlaceholderText("Select an image or PDF file...")

        self.select_file_button = QPushButton("Select File")
        self.select_file_button.setFixedHeight(36)

        file_section_layout.addWidget(file_label)
        file_section_layout.addWidget(self.file_path_field, 1)
        file_section_layout.addWidget(self.select_file_button)

        # run OCR button section
        self.ocr_button = QPushButton("Analyze Handwriting")
        self.ocr_button.setFixedHeight(44)
        self.ocr_button.setEnabled(False)

        # output display section
        output_label = QLabel("Recognition Output:")
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setPlaceholderText("Results and status messages will appear here...")

        # assemble main layout
        main_layout.addLayout(file_section_layout)
        main_layout.addWidget(self.ocr_button)
        main_layout.addWidget(output_label)
        main_layout.addWidget(self.output_display, 1)

    def ApplyStyles(self) -> None:
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-size: 14px;
            }

            QLabel {
                color: #e0e0e0;
            }

            QLineEdit {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px;
            }

            QTextEdit {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 8px;
            }

            QPushButton {
                background-color: #3f51b5;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
            }

            QPushButton:hover {
                background-color: #5c6bc0;
            }

            QPushButton:pressed {
                background-color: #3949ab;
            }

            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
            """
        )

    def ConnectSignals(self) -> None:
        self.select_file_button.clicked.connect(self.SelectFile)
        self.ocr_button.clicked.connect(self.RunOCR)

    def SelectFile(self) -> None:
        image_file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Handwriting File",
            "",
            "Images and PDFs (*.png *.jpg *.jpeg *.bmp *.tiff *.pdf)",
        )

        if image_file_path:
            self.selected_file_path = image_file_path
            self.file_path_field.setText(image_file_path)
            self.ocr_button.setEnabled(True)

    def RunOCR(self) -> None:
        self.output_display.clear()
        self.output_display.append("Processing handwriting...\n")
        self.ocr_button.setEnabled(False)
        QTimer.singleShot(100, self.OCRResults)

    def OCRResults(self):
        result = RunOCR(self.selected_file_path)
        self.output_display.append(result)
        self.ocr_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())