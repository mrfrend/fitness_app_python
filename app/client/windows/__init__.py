"""
Модуль окон клиентской части приложения
"""

from .auth_window import AuthWindow
from .client_window import ClientWindow
from .record_window import RecordWindow
from .myrecord_window import MyRecordWindow
from .history_window import HistoryWindow
from .rate_window import RateWindow
from .progress_window import ProgressWindow

__all__ = [
    'AuthWindow',
    'ClientWindow',
    'RecordWindow',
    'MyRecordWindow',
    'HistoryWindow',
    'RateWindow',
    'ProgressWindow'
]