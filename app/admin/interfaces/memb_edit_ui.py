from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QMainWindow, QLabel, QHBoxLayout, \
    QComboBox, QLineEdit, QDateEdit
import sys

from ui_admin.add_client_ui import AddClientWindow


class MembEdit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменение абонемента")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.label = QLabel("Изменение абонемента")
        main_layout.addWidget(self.label)

        new_type_layout = QHBoxLayout()
        self.labelNew = QLabel("Новый тип: ")
        new_type_layout.addWidget(self.labelNew)
        self.comboBox = QLineEdit()
        new_type_layout.addWidget(self.comboBox)
        main_layout.addLayout(new_type_layout)

        start_layout = QHBoxLayout()
        self.labelStart = QLabel("Начало: ")
        start_layout.addWidget(self.labelStart)
        self.startDate = QDateEdit()
        start_layout.addWidget(self.startDate)
        main_layout.addLayout(start_layout)

        end_layout = QHBoxLayout()
        self.labelEnd = QLabel("Конец: ")
        end_layout.addWidget(self.labelEnd)
        self.endDate = QDateEdit()
        end_layout.addWidget(self.endDate)
        main_layout.addLayout(end_layout)

        btn_layout = QHBoxLayout()
        self.btnSave = QPushButton("Сохранить")
        btn_layout.addWidget(self.btnSave)
        self.btnBack = QPushButton("Назад")
        btn_layout.addWidget(self.btnBack)
        main_layout.addLayout(btn_layout)


        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel {
                font-size: 18px;
                color: #fff;
            }

            QDateEdit {
                padding: 6px;
                border: 1px solid #aaa;
                border-radius: 6px;
            }

            QPushButton {
                background-color: #3855c7;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MembEdit()
    window.show()
    sys.exit(app.exec())