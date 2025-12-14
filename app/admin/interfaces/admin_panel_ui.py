from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QMainWindow
import sys

class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("admin panel")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.btn1 = QPushButton("Управление клиентами")
        main_layout.addWidget(self.btn1)
        self.btn2 = QPushButton("Управление абонементами")
        main_layout.addWidget(self.btn2)
        self.btn3 = QPushButton("Отчеты об абонементах")
        main_layout.addWidget(self.btn3)
        self.btn4 = QPushButton("Замороженные абонементы")
        main_layout.addWidget(self.btn4)
        self.btn5 = QPushButton("Расписание занятий")
        main_layout.addWidget(self.btn5)
        self.btn6 = QPushButton("Загруженность залов")
        main_layout.addWidget(self.btn6)
        self.btn7 = QPushButton("Жалобы и пожелания")
        main_layout.addWidget(self.btn7)
        self.btn8 = QPushButton("Уведомления")
        main_layout.addWidget(self.btn8)


        self.styleApply()


    def styleApply(self):
        self.setStyleSheet("""
                    QWidget {
                        font-family: Segoe UI;
                        font-size: 14px;
                    }
    
                    QLabel {
                        font-size: 20px;
                        color: #fff;
                    }
    
                    QComboBox, QLineEdit {
                        padding: 6px;
                        border: 1px solid #aaa;
                        border-radius: 6px;
                    }
    
                    QComboBox::drop-down {
                        border: 0;
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
    window = AdminPanel()
    window.show()
    sys.exit(app.exec())
