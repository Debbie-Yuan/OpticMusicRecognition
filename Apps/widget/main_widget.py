import tempfile
from os import system, listdir
from os.path import exists, join

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QApplication, QMessageBox
from pymusicxml import Score

from Apps.ui import MainUI
from Apps.widget.commom import ChainedWorkerThread
from logic import PhaseOne, PhaseTwo, PhaseThree, Compose


class MainWidget(QWidget, MainUI):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(u"QTextBrowser {\n"
                           "	border: 3px solid rgb(52, 59, 72);\n"
                           "	border-radius: 0px;\n"
                           "	background: rgb(27, 29, 35)\n"
                           "}\n"
                           "QScrollBar:horizontal {\n"
                           "    border: none;\n"
                           "    background: rgb(52, 59, 72);\n"
                           "    height: 7px;\n"
                           "    margin: 0px 21px 0 21px;\n"
                           "	border-radius: 0px;\n"
                           "}\n"
                           " QScrollBar:vertical {\n"
                           "	border: none;\n"
                           "    background: rgb(52, 59, 72);\n"
                           "    width: 7px;\n"
                           "    margin: 21px 0 21px 0;\n"
                           "	border-radius: 0px;\n"
                           " }\n"
                           u"QGraphicsView {\n"
                           "	border: 3px solid rgb(52, 59, 72);\n"
                           "	border-radius: 0px;\n"
                           "	background: rgb(27, 29, 35)\n"
                           "}\n"
                           u"QProgressBar {\n"
                           "	border: none;\n"
                           "	border-radius: 3px;\n"
                           "	background: rgb(27, 29, 35)\n"
                           "}\n"
                           "QDialog {\n"
                           "	color: #ffffff;\n"
                           "	background-color: rgb(52, 59, 72);\n"
                           "	border: 1px solid rgb(40, 40, 40);\n"
                           "	border-radius: 2px;\n"
                           "}"
                           u"QPushButton {\n"
                           "	border: 2px solid rgb(52, 59, 72);\n"
                           "	border-radius: 5px;	\n"
                           "	background-color: rgb(52, 59, 72);\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           "	background-color: rgb(57, 65, 80);\n"
                           "	border: 2px solid rgb(61, 70, 86);\n"
                           "}\n"
                           "QPushButton:pressed {	\n"
                           "	background-color: rgb(35, 40, 49);\n"
                           "	border: 2px solid rgb(43, 50, 61);\n"
                           "}"
                           "QLabel {	\n"
                           "	background-color: transparent;\n"
                           "}"
                           )
        self.progress_bar.setTextVisible(False)
        self.play_btn.setEnabled(False)
        self.current_file = None
        self.current_img = None
        self.current_task = None
        self.scene = None
        self.current_dir = None
        self.current_phases = None
        self.result = None
        self.zoom_scale = 1
        self.percentage = 0
        self.item = None
        self.connect()

    def connect(self):
        self.open_file_btn.clicked.connect(self.open_file_handler)
        self.process_btn.clicked.connect(self.process)
        self.export_btn.clicked.connect(self.export)
        self.look_xml_btn.clicked.connect(self.xml_watcher)
        self.lookup_json_btn.clicked.connect(self.json_watcher)
        self.open_xml_btn.clicked.connect(self.system_open_temp)

    def system_open_temp(self):
        if not self.result:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        score: Score = self.result[0]
        _, tf = tempfile.mkstemp(suffix='.musicxml', dir=self.current_dir)
        score.export_to_file(tf)
        system(f"open {tf}")

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.modifiers() == Qt.ControlModifier and a0.key() == Qt.Key_Equal:
            self.zoom_graphic_out()
        elif a0.modifiers() == Qt.ControlModifier and a0.key() == Qt.Key_Minus:
            self.zoom_graphic_in()

    def zoom_graphic_in(self):
        if not self.item:
            return
        self.zoom_scale -= 0.05

        if self.zoom_scale <= 0:
            self.zoom_scale = 0.2
        self.item.setScale(self.zoom_scale)

    def zoom_graphic_out(self):
        if not self.item:
            return
        self.zoom_scale = self.zoom_scale + 0.05
        if self.zoom_scale >= 1.2:
            self.zoom_scale = 1.2
        self.item.setScale(self.zoom_scale)

    def setup_img(self):
        frame = QImage(self.current_file)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.item.setScale(0.15)
        if self.scene is None:
            scene = QGraphicsScene()
            scene.addItem(self.item)
            self.scene = scene
            self.graphicsView.setScene(self.scene)
        else:
            self.scene.clear()
            self.scene.addItem(self.item)

    def task_finished(self, t):
        assert len(t) == 3
        self.result = t
        self.current_task.quit()
        self.current_task = None
        self.progress_num.setText('已完成')
        self.progress_bar.setValue(100)
        self.process_btn.setEnabled(True)

    def open_file_handler(self):
        open_file_name, _ = QFileDialog.getOpenFileName(self, '打开乐谱图像', '', '*.png *.jpg *.jpeg')
        if open_file_name == '':
            QMessageBox.information(self, "INFO", "[GD UI-Main] [INFO] File not choose.")
            return
        self.current_file = open_file_name
        self.setup_img()

    def percentage_iadd(self, a, b, c):
        self.percentage += 100 * 0.25 * 1 / b
        self.progress_num.setText("{:.2f}".format(self.percentage) + '%')
        self.progress_bar.setValue(int(self.percentage))
        self.progress_bar.update()
        self.textBrowser.append(c)

    def json_watcher(self):
        if not self.result:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        fn = [i for i in listdir(self.current_dir) if i.endswith('json')]
        if len(fn) == 0:
            QMessageBox.information(self, "No Session", "可能没有保存JSON结果，无法找到。")
            return
        fn = fn[0]
        with open(join(self.current_dir, fn), 'r') as fp:
            content = fp.read()
            self.textBrowser.clear()
            self.textBrowser.append(content)

    def xml_watcher(self):
        if not self.result:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        resp = QMessageBox.question(self, "是否丢弃日志", f"离开此页面后日志将丢失！是否继续？")
        if resp == QMessageBox.Yes:
            score: Score = self.result[0]
            xml = score.to_xml(pretty_print=True)
            self.textBrowser.clear()
            self.textBrowser.setText(xml)
        else:
            return

    def export(self):
        if not self.result:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        fn, _ = QFileDialog.getSaveFileName(self)
        if fn == '':
            QMessageBox.information(self, "INFO", "[GD UI-Main] [INFO] File not choose.")
            return
        if exists(fn):
            resp = QMessageBox.question(self, "文件重复！", "文件已存在，是否覆盖？")
            if not (resp == QMessageBox.Ok or resp == QMessageBox.Yes):
                return
        score: Score = self.result[0]
        try:
            if 'musicxml' not in fn:
                fn = fn + '.musicxml'
            score.export_to_file(fn)
            QMessageBox.information(self, "导出成功！", f"已经导出至`{fn}`!")
        except Exception:
            QMessageBox.critical(self, "输出错误", "发生了一些错误，有可能是文件权限不足！")

    def process_temp(self, d):
        pass

    def collect_data(self):
        _q = {}
        title = self.title_le.text()
        if len(title) == 0:
            pass
        else:
            _q.setdefault('title', title)
        author = self.author_le.text()
        if len(author) == 0:
            pass
        else:
            _q.setdefault('author', author)
        try:
            speed = int(self.speed_le.text())
            _q.setdefault('speed', speed)
        except ValueError:
            pass
        sig = self.ts_le.text()
        if '/' in sig:
            _1, _2 = sig.split('/')
            try:
                _1 = int(_1)
                _2 = int(_2)
                _q.setdefault('time_signature', (_1, _2))
            except ValueError:
                pass
        clef = self.clef_le.text()
        if len(clef) == 0:
            clef = self.clef_le.placeholderText()

        _q.setdefault('clef', clef)
        return _q

    def process(self):
        if self.current_file is None:
            QMessageBox.information(self, "No selection!", "No file!")
            return
        self.process_btn.setEnabled(False)
        self.progress_num.setText('正在处理...')
        self.progress_bar.setValue(0)
        self.percentage = 0
        p1 = PhaseOne(self.current_file)
        p1.iter_callback.connect(self.percentage_iadd)
        self.current_dir = p1.cwd
        p2 = PhaseTwo(p1.cwd)
        p2.iter_callback.connect(self.percentage_iadd)
        p3 = PhaseThree(p1.cwd)
        p3.iter_callback.connect(self.percentage_iadd)

        compose = Compose(p1.cwd, **self.collect_data())
        compose.iter_callback.connect(self.percentage_iadd)
        self.current_phases = tuple((p1, p2, p3, compose))
        tasks = tuple((p1.run, p2.run, p3.run, compose.run))
        chained_worker = ChainedWorkerThread(tasks, parent=self)
        # chained_worker.partial_done.connect(self.partial_finished)
        chained_worker.finished.connect(self.task_finished)
        self.current_task = chained_worker
        chained_worker.start()


def main():
    import sys
    app = QApplication(sys.argv)
    phase_one = MainWidget()
    phase_one.show()
    app.exec_()
