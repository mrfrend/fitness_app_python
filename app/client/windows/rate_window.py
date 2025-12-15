from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
from app.client.interfaces.rate_ui import RateUi
from app.client.dao.client_dao import ClientDAO


class RateWindow(RateUi):
    def __init__(self, client_id, parent=None):
        super().__init__()
        self.client_id = client_id
        self.parent_window = parent
        self.dao = ClientDAO()

        # Настраиваем дату на текущую
        current_date = QDate.currentDate()
        self.dateEdit.setDate(current_date)

        # Подключаем обработчики событий
        self.btnSend.clicked.connect(self.handle_send)
        self.btnBack.clicked.connect(self.go_back)

    def handle_send(self):
        """Обработка отправки отзыва"""
        try:
            # Получаем данные из формы
            review_type = self.boxReason.currentText()
            review_date = self.dateEdit.date().toString('yyyy-MM-dd')
            review_text = self.textEdit.toPlainText().strip()

            # Валидация
            if not review_text:
                QMessageBox.warning(self, "Ошибка", "Введите текст отзыва")
                return

            # Проверяем длину в зависимости от типа
            if review_type == "Пожелание":
                # Для Review ограничение text (обычно большой текст)
                if len(review_text) > 2000:
                    QMessageBox.warning(self, "Ошибка", "Текст пожелания слишком длинный (макс. 2000 символов)")
                    return
            else:  # Жалоба
                # Для Complaints ограничение 250 символов
                if len(review_text) > 250:
                    QMessageBox.warning(self, "Ошибка", "Текст жалобы слишком длинный (макс. 250 символов)")
                    return

            # Определяем тип сообщения для пользователя
            message_type = "пожелание" if review_type == "Пожелание" else "жалобу"

            # Подтверждение отправки
            reply = QMessageBox.question(
                self, 'Подтверждение отправки',
                f"Вы уверены, что хотите отправить {message_type}?\n\n"
                f"Текст: {review_text[:100]}{'...' if len(review_text) > 100 else ''}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = False

                # Сохраняем в соответствующую таблицу
                if review_type == "Пожелание":
                    # Сохраняем пожелание в таблицу Review
                    success = self.dao.save_review(
                        self.client_id,
                        'Suggestion',  # reviewType в таблице Review
                        review_text,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    )
                else:  # Жалоба
                    # Сохраняем жалобу в таблицу Complaints
                    success = self.dao.save_complaint(
                        self.client_id,
                        review_text,
                        review_date
                    )

                if success:
                    QMessageBox.information(self, "Успех", f"{message_type.capitalize()} успешно отправлено!")
                    # Очищаем форму
                    self.textEdit.clear()
                    # Возвращаемся назад
                    self.go_back()
                else:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось отправить {message_type}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при отправке отзыва: {str(e)}")

    def go_back(self):
        """Возврат к предыдущему окну"""
        if self.parent_window:
            self.parent_window.show()
        self.close()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.parent_window:
            self.parent_window.show()
        event.accept()