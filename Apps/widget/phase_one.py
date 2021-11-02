from os import listdir, system
from os.path import exists, join, isdir, split

from PIL import ImageQt
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QApplication, QMessageBox

from Apps.ui import P1Ui
from Apps.widget.commom import WorkerThread
from logic import PhaseOne
from settings import CWD


class PhaseOneWidget(QWidget, P1Ui):
    update_image = pyqtSignal(str)

    def __init__(self, parent=None):
        super(PhaseOneWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.current_phase_one: [PhaseOne or None] = None
        self.scene = None
        self.wkt = None
        self.current_file = None
        self.current_folder = None
        self.current_meta = None
        self.item = None
        self.current_graphic = 1
        self.zoom_scale = 1
        self.connect()
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.setStyleSheet(u"QTextBrowser, QGraphicsView, QListView {\n"
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

    def connect(self):
        self.open_file.clicked.connect(self.open_file_handler)
        self.open_dir.clicked.connect(self.read_from_exist)
        self.listView.clicked.connect(self.list_view_changed)
        self.update_image.connect(self.setup_img)
        self.next_btn.clicked.connect(self.next)
        self.previous_btn.clicked.connect(self.previous)
        self.show_net_btn.clicked.connect(self.load_net_res)
        self.show_files_btn.clicked.connect(self.load_origin)
        self.p1_predict.clicked.connect(self.predict)
        self.exp_btn.clicked.connect(self.export)

        # self.p1_predict.clicked.connect(self.predict)

    def export(self):
        if not self.current_folder:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        fn = QFileDialog.getExistingDirectory(self)
        if fn == '':
            QMessageBox.information(self, "INFO", "[GD UI-Main] [INFO] File not choose.")
            return
        ret = system(f"cp -r {self.current_folder} {fn}")
        pth, dirn = split(self.current_folder)
        new_pth = join(fn, dirn)

        if ret == 0:
            QMessageBox.information(self, "成功", "导出成功。")
            new_p1_meta = join(new_pth, '.p1meta.txt')
            with open(new_p1_meta, 'r') as frd:
                lines = frd.readlines()

            with open(new_p1_meta, 'w') as frw:
                for line in lines:
                    if len(line) <= 0:
                        continue
                    _, name = split(line.strip('\n'))
                    frw.write(f"{join(new_pth, name)}\n")
        else:
            QMessageBox.information(self, "失败", "导出失败。")

    def load_origin(self):
        if self.current_graphic == 3:
            return
        fn = join(self.current_folder, 'p1-origin.jpg')
        if exists(fn):
            self.setup_img('p1-origin.jpg')
            self.current_graphic = 3
        else:
            self.log_and_dialog("[GD P1-LO] File DOES NOT EXIST!", '文件不存在', type_='critical')

    def load_net_res(self):
        if self.show_net_btn.text() == '显示网络结果':
            if self.current_graphic == 2:
                return

            fn = join(self.current_folder, 'p1-net-res.jpg')
            if exists(fn):
                self.current_graphic = 2
                self.show_net_btn.setText('显示分割文件')
                self.setup_img('p1-net-res.jpg')
            else:
                self.log_and_dialog("[GD P1-LO] File DOES NOT EXIST!", '文件不存在', type_='critical')
        else:
            if self.current_graphic == 1:
                return
            self.current_graphic = 1
            self.show_net_btn.setText('显示网络结果')
            crd = self.listView.currentIndex().data()
            self.setup_img(crd)

    def list_view_changed(self, idx: QModelIndex):
        if self.current_graphic != 1:
            return
        self.setup_img(idx.data())

    def next(self):
        if not self.listView or not self.model:
            return
        cr = self.listView.currentIndex()
        r = cr.row()
        mr = self.listView.model().rowCount()
        if r >= mr - 1:
            return
        fn = self.model.index(r + 1, 0).data()
        self.update_image.emit(fn)
        self.listView.setCurrentIndex(self.model.index(r + 1, 0))

    def previous(self):
        if not self.listView or not self.model:
            return
        cr = self.listView.currentIndex()
        r = cr.row()
        if r < 1:
            return
        fn = self.model.index(r - 1, 0).data()
        self.update_image.emit(fn)
        self.listView.setCurrentIndex(self.model.index(r - 1, 0))

    def setup_img(self, fn, img_cnt=None):
        if fn:
            frame = QImage(join(self.current_folder, fn))
            pix = QPixmap.fromImage(frame)
        elif img_cnt:
            pix = ImageQt.toqpixmap(img_cnt)

        self.item = QGraphicsPixmapItem(pix)
        self.item.setScale(0.7)
        if self.scene is None:
            scene = QGraphicsScene()
            scene.addItem(self.item)
            self.scene = scene
            self.graphic.setScene(self.scene)
        else:
            self.scene.clear()
            self.scene.addItem(self.item)

    def log_and_dialog(self, msg, title, d_msg=None, type_=None):
        self.text_logs.append(msg)
        dlg = QMessageBox(self)
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        if not type_ or type_ == 'information':
            dlg.information(self, title, d_msg if d_msg else msg)
        elif type_ == 'critical':
            dlg.critical(self, title, d_msg if d_msg else msg)

    def lst_dir(self):
        for fn in listdir(self.current_folder):
            if not fn.startswith('.') and not \
                    isdir(join(self.current_folder, fn)) and not \
                    fn == 'p1-origin.jpg' and not fn == 'p1-net-res.jpg':
                yield fn

    def setup_model(self):
        root = self.model.invisibleRootItem()
        for t, fn in enumerate(self.lst_dir()):
            item = QStandardItem(fn)
            root.setChild(t, item)
            self.text_logs.append(f"[GD PH1-LOAD] L -> `{fn}`")

    def read_from_exist(self):
        open_folder_name = QFileDialog.getExistingDirectory(self, '打开一阶段缓存目录', join(CWD, 'temp'))
        if not open_folder_name or len(open_folder_name) == 0:
            return
        if not exists(join(open_folder_name, '.p1meta.txt')):
            self.log_and_dialog("[GD PH1-OPEN FOLDER] ERROR, No Meta File Detected!",
                                "[GD PH1]", "错误，没有检测到Meta信息。", type_='critical')
            return
        # 判断本次和之前是否一致
        if self.current_folder == open_folder_name:
            self.log_and_dialog("[GD PH1-OPEN FOLDER]", "[GD PH1]",
                                "错误，与上次打开的文件夹相同", type_='information')
            return
        self.text_logs.append(f"[GD PH1-OPEN FOLDER] `{open_folder_name}`")
        # 每次成功加载时清空路径
        self.model.clear()
        self.current_meta = join(open_folder_name, '.p1meta.txt')
        self.current_folder = open_folder_name
        self.text_logs.append("[GD PH1-OPEN FOLDER] SUCCESS, Folder Loaded!")
        # 检查路径下的文件并读取
        self.setup_model()

        # 将文件内容加载入右侧挡板
        first_val = self.model.index(0, 0)
        self.listView.setCurrentIndex(first_val)
        self.setup_img(first_val.data())

    def task_finished(self):
        self.wkt = None
        self.log_and_dialog(f"[GD UI-PhaseOne] Predict finished. Saved to folder `{self.current_phase_one.cwd}`.",
                            "Success", type_='information')
        # 将图像放到frame上
        self.model.clear()
        # 检查路径下的文件并读取
        self.setup_model()

        # 将文件内容加载入右侧挡板
        first_val = self.model.index(0, 0)
        self.listView.setCurrentIndex(first_val)
        self.setup_img(first_val.data())

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

    def open_file_handler(self):
        open_file_name, _ = QFileDialog.getOpenFileName(self, '打开乐谱图像', '', '*.png *.jpg *.jpeg')
        if open_file_name == '':
            self.text_logs.append(f"[GD UI-PhaseOne] [INFO] File not choose.")
            return
        self.fn_chooser.setText(open_file_name)
        self.text_logs.append(f"[GD UI-PhaseOne] File `{open_file_name}` selected.")

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:

        if a0.key() == Qt.Key_Up:
            if self.current_graphic != 1:
                return
            self.previous()
        elif a0.key() == Qt.Key_Down:
            if self.current_graphic != 1:
                return
            self.next()
        elif a0.modifiers() == Qt.ControlModifier and a0.key() == Qt.Key_Equal:
            self.zoom_graphic_out()
        elif a0.modifiers() == Qt.ControlModifier and a0.key() == Qt.Key_Minus:
            self.zoom_graphic_in()

    def predict(self):
        # 清空图像
        if self.wkt is not None:
            self.text_logs.append(f"[GD UI-PhaseOne] [ERROR] Task executing!")
            return
        if self.scene:
            self.scene.clear()
        fn = self.fn_chooser.text()
        if not exists(fn):
            self.text_logs.append(f"[GD UI-PhaseOne] [ERROR] File not exists!")
            return
        self.current_phase_one = PhaseOne(fn)
        self.current_folder = self.current_phase_one.cwd
        self.current_meta = join(self.current_folder, '.p1meta.txt')
        wk = WorkerThread(self.current_phase_one.run, parent=self)
        self.wkt = wk
        wk.trigger.connect(self.task_finished)
        wk.start()


def main():
    import sys
    app = QApplication(sys.argv)
    phase_one = PhaseOneWidget()
    phase_one.show()
    app.exec_()
