import tempfile
from os import listdir, system
from os.path import join, isdir, exists

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox

from Apps.ui import ComposeUi
from logic import Compose
from settings import CWD


class ComposeWidget(QWidget, ComposeUi):
    process = pyqtSignal()

    def __init__(self, parent=None):
        super(ComposeWidget, self).__init__(parent)
        self.setupUi(self)
        self.current_folder = None
        self.setStyleSheet(u"QTextBrowser, QGraphicsView, QTreeView {\n"
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
        self.connect()
        self.current_composer = None
        self.current_score = None

    def connect(self):
        self.open_folder_btn.clicked.connect(self.open_folder)
        self.export_btn.clicked.connect(self.export)
        self.popopen_btn.clicked.connect(self.popopen)
        self.process.connect(self.process_folder)

    def collect_data(self):
        q = {}
        title = self.title_le.text()
        if len(title) == 0:
            pass
        else:
            q.setdefault('title', title)
        author = self.author_le.text()
        if len(author) == 0:
            pass
        else:
            q.setdefault('author', author)
        try:
            speed = int(self.speed_le.text())
            q.setdefault('speed', speed)
        except ValueError:
            pass
        sig = self.ts_le.text()
        if '/' in sig:
            _1, _2 = sig.split('/')
            try:
                _1 = int(_1)
                _2 = int(_2)
                q.setdefault('time', (_1, _2))
            except ValueError:
                pass
        clef = self.clef_le.text()
        if len(clef) == 0:
            clef = self.clef_le.placeholderText()

        q.setdefault('clef', clef)
        return q

    def process_folder(self):

        cmp = Compose(self.current_folder, **self.collect_data())
        self.current_score = cmp()
        if self.current_score:
            self.log_and_dialog("[GD COMPOSE] Success!", "Success", "Processed successfully!", 'information')
            return
        self.log_and_dialog("[GD COMPOSE] Failed!", "Failed", "Failed!", 'critical')

    def log_and_dialog(self, msg, title, d_msg=None, type_=None):
        self.text_logs.append(msg)
        dlg = QMessageBox(self)
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        if not type_ or type_ == 'information':
            dlg.information(self, title, d_msg if d_msg else msg)
        elif type_ == 'critical':
            dlg.critical(self, title, d_msg if d_msg else msg)

    def lst_dir(self):
        if not self.current_inner_folder:
            return
        for fn in listdir(self.current_inner_folder):
            if not fn.startswith('.') and not \
                    isdir(join(self.current_inner_folder, fn)) and not \
                    fn.endswith('.txt') and 'p2-net' not in fn and 'p2-ori' not in fn:
                yield fn

    def lst_inner_dir(self):
        for folder in listdir(self.current_folder):
            abs_pth = join(self.current_folder, folder)
            if isdir(abs_pth) and exists(join(abs_pth, 'p3res.txt')):
                yield folder

    def load_res(self):
        if not self.current_inner_folder:
            return
        cls = [line.strip('\n') for line in open(join(self.current_inner_folder, 'p3res.txt'), 'r').readlines() if
               line != '\n']
        for cls_list in cls:
            yield tuple(int(k) for k in cls_list.split(' '))

    def open_folder(self):
        open_folder_name = QFileDialog.getExistingDirectory(self, '打开三阶段目录', CWD)
        if not open_folder_name or len(open_folder_name) == 0:
            return
        if self.current_folder == open_folder_name:
            self.log_and_dialog("[GD PH4-OPEN FOLDER]", "[GD PH4]",
                                "错误，与上次打开的文件夹相同", type_='information')
            return
        self.current_folder = open_folder_name

        inner_folders = [i for i in self.lst_inner_dir()]
        if len(inner_folders) == 0:
            self.log_and_dialog("[GD PH1-OPEN FOLDER] ERROR, No Meta File Detected!",
                                "[GD PH1]", "错误，没有检测到二阶段Meta信息或三阶段结果。", type_='critical')
            self.current_folder = None
            return
        self.status_now.setText("文件夹已经加载。")
        self.process.emit()

    def export(self):
        if not self.current_score:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        fn, _ = QFileDialog.getSaveFileName(self)
        if fn == '':
            QMessageBox.information(self, "INFO", "[GD UI-COMPOSE] [INFO] File not choose.")
            return
        if exists(fn):
            resp = QMessageBox.question(self, "文件重复！", "文件已存在，是否覆盖？")
            if not (resp == QMessageBox.Ok or resp == QMessageBox.Yes):
                return
        try:
            if 'musicxml' not in fn:
                fn = fn + '.musicxml'
            self.current_score[0].export_to_file(fn)
            QMessageBox.information(self, "导出成功！", f"已经导出至`{fn}`!")
        except Exception:
            QMessageBox.critical(self, "输出错误", "发生了一些错误，有可能是文件权限不足！")

    def popopen(self):
        if not self.current_score:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        _, tf = tempfile.mkstemp(suffix='.musicxml')
        self.current_score[0].export_to_file(tf)
        system(f"open {tf}")
