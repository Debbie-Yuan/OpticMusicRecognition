from typing import Tuple, Callable

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal


class MyListView(QtWidgets.QListView):
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        e.ignore()


class WorkerThread(QThread):
    trigger = pyqtSignal()

    def __init__(self, task, parent=None):
        super(WorkerThread, self).__init__(parent=parent)
        self.task = task

    def run(self) -> None:
        self.task()

        self.trigger.emit()


class ChainedWorkerThread(QThread):
    finished = pyqtSignal(tuple)
    partial_done = pyqtSignal(int, int)

    def __init__(self, tasks: Tuple[Callable], parent=None):
        super(ChainedWorkerThread, self).__init__(parent=parent)
        self.tasks = tasks
        self.length = len(tasks)
        self.thread_active = True

    def run(self) -> None:
        res = ()
        for t, task in enumerate(self.tasks):
            if self.thread_active:
                res = task()
            else:
                exit(1)
            self.partial_done.emit(t + 1, self.length)

        self.finished.emit(res)

    def stop(self):
        self.thread_active = False
        self.wait()
