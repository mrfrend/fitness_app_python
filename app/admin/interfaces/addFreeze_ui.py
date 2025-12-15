from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QHBoxLayout, QLineEdit, QPushButton, QDateEdit,
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import sys


class AddFreeze(QMainWindow):
    freeze_saved = pyqtSignal(dict)
    back_requested = pyqtSignal()

    def __init__(self, client_id=None, parent=None, freeze=None):
        super().__init__(parent)
        self.client_id = client_id
        self.freeze = freeze or {}
        self.setWindowTitle("Добавить заморозку")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(16)
        grid_layout.setVerticalSpacing(12)
        main_layout.addLayout(grid_layout)

        labels = [
            QLabel("ID клиента:"),
            QLabel("Дата начала:"),
            QLabel("Дата окончания:"),
            QLabel("Причина:")
        ]

        client_value = self.freeze.get('clientID') if self.freeze else client_id
        self.client_input = QLineEdit(str(client_value) if client_value else "")
        self.client_input.setReadOnly(client_id is not None)
        self.start_input = QDateEdit(calendarPopup=True)
        self.start_input.setDate(self._get_initial_date('startDate'))
        self.end_input = QDateEdit(calendarPopup=True)
        self.end_input.setDate(self._get_initial_date('endDate', default_offset_days=7))
        self.reason_input = QLineEdit(self.freeze.get('reason', ''))

        editors = [self.client_input, self.start_input, self.end_input, self.reason_input]

        for row, (label, editor) in enumerate(zip(labels, editors)):
            grid_layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignRight)
            grid_layout.addWidget(editor, row, 1)

        buttons = QHBoxLayout()
        self.btnSave = QPushButton("Сохранить")
        self.btnBack = QPushButton("Назад")
        buttons.addWidget(self.btnSave)
        buttons.addWidget(self.btnBack)
        main_layout.addLayout(buttons)

        self.btnSave.clicked.connect(self._on_save)
        self.btnBack.clicked.connect(self._on_back)

        self.styleApply()

    def styleApply(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
                font-size: 14px;
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

    def _get_initial_date(self, key, default_offset_days=0):
        if self.freeze.get(key):
            value = self.freeze[key]
            if hasattr(value, 'toPyDate'):
                return value
            if hasattr(value, 'strftime'):
                return QDate(value.year, value.month, value.day)
            if isinstance(value, str):
                try:
                    parts = [int(part) for part in value.split('-')]
                    if len(parts) == 3:
                        return QDate(parts[0], parts[1], parts[2])
                except ValueError:
                    pass
        return QDate.currentDate().addDays(default_offset_days)

    def _on_save(self):
        client_text = self.client_input.text().strip()
        if not client_text.isdigit():
            QMessageBox.warning(self, 'Ошибка', 'ID клиента должен быть числом')
            return

        start_date = self.start_input.date()
        end_date = self.end_input.date()

        if end_date < start_date:
            QMessageBox.warning(self, 'Ошибка', 'Дата окончания должна быть позже даты начала')
            return

        data = {
            'freezeID': self.freeze.get('freezeID'),
            'membershipID': self.freeze.get('membershipID'),
            'clientID': int(client_text),
            'startDate': start_date.toPyDate(),
            'endDate': end_date.toPyDate(),
            'reason': self.reason_input.text().strip(),
        }

        self.freeze_saved.emit(data)
        self._on_back()

    def _on_back(self):
        self.back_requested.emit()
        self.close()

    def closeEvent(self, event):
        self.back_requested.emit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddFreeze()
    window.show()
    sys.exit(app.exec())