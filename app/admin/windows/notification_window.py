from app.admin.interfaces.notification_ui import NotificatioUi

class NotificationWindow(NotificatioUi):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_window = parent

        if hasattr(self, 'btnBack'):
            self.btnBack.clicked.connect(self._go_back)

    def _go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()
