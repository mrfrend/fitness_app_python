from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow


class NavigableWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self._parent_window = parent_window

    def _back(self):
        parent = self._parent_window
        self.hide()
        if parent is not None:
            parent.show()

    def closeEvent(self, event: QCloseEvent):
        parent = self._parent_window
        if parent is not None:
            parent.show()
        super().closeEvent(event)
