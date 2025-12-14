
import sys

from PyQt6.QtWidgets import QApplication

from app.trainer.windows.main_trainer_window import MainTrainerWindow


def main() -> int:
    trainer_id = 7
    if len(sys.argv) > 1:
        try:
            trainer_id = int(sys.argv[1])
        except ValueError:
            trainer_id = 7

    app = QApplication(sys.argv)
    w = MainTrainerWindow(trainer_id=trainer_id)
    w.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
