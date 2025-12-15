import sys
import os
# from pathlib import Path


# Add the project root to Python path
# project_root = str(Path(__file__).parent.parent.parent.parent)
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

def main():
    try:
        # Initialize the application
        app = QApplication(sys.argv)
        
        # Set application style and properties
        # app.setStyle('Fusion')
        # app.setWindowIcon(QIcon(os.path.join(project_root, 'static', 'icon.ico')))
        
        # Import and create main window
        from app.admin.windows.admin_main_window import AdminPanelWindow
        
        # Create and show main window
        window = AdminPanelWindow()
        window.setWindowTitle("Фитнес-клуб - Панель администратора")
        window.showMaximized()
        
        # Start the application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        # Show error message if something goes wrong
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Icon.Critical)
        error_msg.setWindowTitle("Ошибка запуска")
        error_msg.setText("Не удалось запустить приложение")
        error_msg.setDetailedText(str(e))
        error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_msg.exec()
        return 1

if __name__ == "__main__":
    main()