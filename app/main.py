
from __future__ import annotations

import logging
import sys

from PyQt6.QtWidgets import QApplication

from app.core.ui_styles import DARK_UI_STYLESHEET
from app.director.windows.director_main import DirectorMainWindow


def main() -> int:
    """Точка входа приложения."""
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_UI_STYLESHEET)
    window = DirectorMainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
