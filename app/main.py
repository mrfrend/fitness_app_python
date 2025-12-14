
from __future__ import annotations

import logging
import signal
import sys
from typing import Optional

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from app.core.ui_styles import DARK_UI_STYLESHEET
from app.director.windows.director_main import DirectorMainWindow


_INTERRUPT_TIMER_INTERVAL_MS = 100
_interrupt_timer: Optional[QTimer] = None


def setup_qt_interrupt_handling(app: QApplication) -> None:
    """Настраивает корректное завершение Qt-приложения по Ctrl+C/Ctrl+Break.

    Args:
        app: Экземпляр QApplication.
    """

    def _signal_handler(signum: int, frame) -> None:  # type: ignore[no-untyped-def]
        app.quit()

    signal.signal(signal.SIGINT, _signal_handler)
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, _signal_handler)

    global _interrupt_timer
    _interrupt_timer = QTimer()
    _interrupt_timer.setInterval(_INTERRUPT_TIMER_INTERVAL_MS)
    _interrupt_timer.timeout.connect(lambda: None)
    _interrupt_timer.start()


def main() -> int:
    """Точка входа приложения."""
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_UI_STYLESHEET)
    setup_qt_interrupt_handling(app)
    window = DirectorMainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
