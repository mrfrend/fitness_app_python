import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from app.admin.interfaces.admin_panel_ui import AdminPanel
from app.admin.windows.manage_client_window import ManageClientWindow
from app.admin.windows.memb_types_window import MembTypesWindow
from app.admin.windows.memb_report_window import MembReportWindow
from app.admin.windows.freezed_window import FreezedWindow
from app.admin.windows.schedule_train_window import ScheduleTrainWindow
from app.admin.windows.workload_gym_window import WorkloadGymWindow
from app.admin.windows.reports_window import ReportWindow
from app.admin.windows.notification_window import NotificationWindow

class AdminPanelWindow(AdminPanel):
    def __init__(self):
        super().__init__()

        self.btn1.clicked.connect(self.open_manage_clients)
        self.btn2.clicked.connect(self.open_memb_types)
        self.btn3.clicked.connect(self.open_memb_report)
        self.btn4.clicked.connect(self.open_freezed)
        self.btn5.clicked.connect(self.open_schedule)
        self.btn6.clicked.connect(self.open_workload_gym)
        self.btn7.clicked.connect(self.open_reports)
        self.btn8.clicked.connect(self.open_notification)

        self._child_window = None

    def _show_child(self, window, title):
        self._child_window = window
        window.setWindowTitle(title)
        window.show()
        self.hide()

    def open_manage_clients(self):
        self._show_child(ManageClientWindow(self), "Управление клиентами")

    def open_memb_types(self):
        self._show_child(MembTypesWindow(self), "Управление абонементами")

    def open_memb_report(self):
        self._show_child(MembReportWindow(self), "Отчеты об абонементах")

    def open_freezed(self):
        self._show_child(FreezedWindow(self), "Замороженные абонементы")

    def open_schedule(self):
        self._show_child(ScheduleTrainWindow(self), "Расписание занятий")

    def open_workload_gym(self):
        self._show_child(WorkloadGymWindow(self), "Загруженность залов")

    def open_reports(self):
        self._show_child(ReportWindow(self), "Жалобы и пожелания")

    def open_notification(self):
        self._show_child(NotificationWindow(self), "Уведомления")