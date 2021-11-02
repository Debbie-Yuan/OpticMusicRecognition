from os import listdir, system
from os.path import exists, join, isdir, splitext

from PIL import ImageQt
from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QFileSystemModel, \
    QMessageBox, QAbstractItemView

from Apps.ui import P2Ui
from Apps.widget.commom import WorkerThread
from logic import PhaseTwo
from settings import CWD


class PhaseTwoWidget(QWidget, P2Ui):

    def __init__(self, parent=None):
        super(PhaseTwoWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.current_phase_two: [PhaseTwo or None] = None
        self.scene = None
        self.wkt = None
        self.current_folder = None
        self.current_inner_folder = None
        self.current_files = None
        self.current_files_idx = 0
        self.current_meta = None
        self.item = None
        self.item_ori = None
        self.scene_ori = None
        self.current_graphic = 1
        self.zoom_scale = 1
        self.percentage = 0
        self.connect()
        self.progressBar.setVisible(False)
        self.model = QFileSystemModel()
        self.treeView.setModel(self.model)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setColumnWidth(0, 200)
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

    def log_and_dialog(self, msg, title, d_msg=None, type_=None):
        self.text_logs.append(msg)
        dlg = QMessageBox(self)
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        if not type_ or type_ == 'information':
            dlg.information(self, title, d_msg if d_msg else msg)
        elif type_ == 'critical':
            dlg.critical(self, title, d_msg if d_msg else msg)

    def connect(self):
        self.open_file.clicked.connect(self.open_file_handler)
        self.open_dir.clicked.connect(self.read_from_exist)
        self.treeView.clicked.connect(self.tree_item_changed)
        self.previous_btn.clicked.connect(self.previous)
        self.next_btn.clicked.connect(self.next)
        self.show_net_btn.clicked.connect(self.show_net)
        self.p1_predict.clicked.connect(self.predict)

    def show_net(self):
        if self.show_net_btn.text() == '显示网络结果':
            if not self.current_inner_folder:
                return
            inner_net_res_pth = join(self.current_inner_folder, 'p2-net-res.jpg')
            if not exists(inner_net_res_pth):
                self.log_and_dialog("[GD PH2-SN:114] Net Result File Does Not Exist!", 'Not Exist', type_='critical')
                return
            self.setup_img('p2-net-res.jpg')
            self.show_net_btn.setText("显示分割结果")
        else:
            if not self.current_files or len(self.current_files) <= 0:
                self.log_and_dialog("[GD PH2-SN:121] CANNOT Find Any Result From Current Folder!",
                                    'Not Exist', type_='critical')
                return
            self.setup_img(self.current_files[self.current_files_idx])
            self.show_net_btn.setText("显示网络结果")

    def lst_dir(self):
        if not self.current_inner_folder:
            return
        for fn in listdir(self.current_inner_folder):
            if not fn.startswith('.') and not \
                    isdir(join(self.current_inner_folder, fn)) and not \
                    fn.endswith('.txt') and 'p2-net' not in fn and 'p2-ori' not in fn:
                yield fn

    def tree_item_changed(self, a0: QModelIndex):
        print('enter_tree_item', a0.data())
        abs_pth = join(self.current_folder, a0.data())
        if not isdir(abs_pth):
            return
        self.folder_name.setText(a0.data())
        self.current_inner_folder = join(self.current_folder, a0.data())
        self.current_meta = join(self.current_inner_folder, '.p2meta.txt')
        self.current_files = [i for i in self.lst_dir()]
        if len(self.current_files) > 0:
            self.current_files_idx = 0
        else:
            return
        self.setup_img(self.current_files[self.current_files_idx])
        self.setup_label()
        self.setup_img_origin()

    def lst_inner_dir(self):
        for folder in listdir(self.current_folder):
            abs_pth = join(self.current_folder, folder)
            if isdir(abs_pth) and exists(join(abs_pth, '.p2meta.txt')):
                yield folder

    def setup_label(self):
        _, folder_name = splitext(self.current_inner_folder)
        f_pth = join(folder_name, self.current_files[self.current_files_idx])
        self.folder_name.setText(f_pth)
        self.text_logs.append(f"[GD PH2-SL] Lable Changed to `{f_pth}`.")

    def setup_img(self, fn, img_cnt=None):
        if fn:
            frame = QImage(join(self.current_inner_folder, fn))
            pix = QPixmap.fromImage(frame)
        elif img_cnt:
            pix = ImageQt.toqpixmap(img_cnt)
        else:
            return

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

    def setup_img_origin(self):
        if not self.current_inner_folder:
            return
        if len(self.current_files) <= 0:
            return
        origin = self.current_inner_folder + '.jpg'
        if not exists(origin):
            origin = join(self.current_inner_folder, 'p2-origin.jpg')

        if not exists(origin):
            self.log_and_dialog("[GD PH2-SIO:193] CANNOT FIND ORIGIN IMAGE!", 'No File', type_='critical')
            return
        pix = QPixmap.fromImage(QImage(origin))
        self.item_ori = QGraphicsPixmapItem(pix)
        self.item_ori.setScale(0.55)
        if self.scene_ori is None:
            scene = QGraphicsScene()
            scene.addItem(self.item_ori)
            self.scene_ori = scene
            self.graphic_origin.setScene(self.scene_ori)
        else:
            self.scene_ori.clear()
            self.scene_ori.addItem(self.item_ori)

    def task_finished(self):
        self.wkt = None
        self.text_logs.append(f"[GD UI-PhaseTwo] Predict finished. Saved to folder `{self.current_phase_two.cwd}`.")
        self.change_model_info()
        self.progressBar.setVisible(False)
        self.percentage = 0

    def open_file_handler(self):
        open_file_name = QFileDialog.getExistingDirectory(self, '打开一阶段结果')
        if open_file_name == '':
            self.text_logs.append(f"[GD UI-PhaseOne] [INFO] File not choose.")
            return
        if not exists(join(open_file_name, '.p1meta.txt')):
            self.log_and_dialog("[GD P2-OFH:236] Folder Format Incorrect.", 'Incorrect', type_='critical')
            return
        self.current_folder = open_file_name
        self.fn_chooser.setText(open_file_name)
        self.text_logs.append(f"[GD UI-PhaseOne] File `{open_file_name}` selected.")

    # 导出功能
    def export(self):
        if not self.current_folder:
            QMessageBox.information(self, "No Session", "请确保已经运行并产生结果。")
            return
        fn = QFileDialog.getExistingDirectory(self)
        if fn == '':
            QMessageBox.information(self, "INFO", "[GD UI-Main] [INFO] File not choose.")
            return
        ret = system(f"cp -r {self.current_folder} {fn}")
        if ret == 0:
            QMessageBox.information(self, "成功", "导出成功。")
        else:
            QMessageBox.information(self, "失败", "导出失败。")

    def change_model_info(self):
        dir = QDir(self.current_folder)
        dir.setFilter(QDir.Hidden | QDir.AllDirs | QDir.NoSymLinks)
        self.model.setRootPath(dir.path())
        self.treeView.setRootIndex(self.model.index(dir.path()))
        for t in range(1, self.model.columnCount()):
            self.treeView.hideColumn(t)

        # 从已存在的二阶段项目打开

    def read_from_exist(self):
        open_folder_name = QFileDialog.getExistingDirectory(self, '打开一阶段缓存目录', join(CWD, 'temp'))
        if not open_folder_name or len(open_folder_name) == 0:
            return
        if self.current_folder == open_folder_name:
            self.log_and_dialog("[GD PH1-OPEN FOLDER]", "[GD PH1]",
                                "错误，与上次打开的文件夹相同", type_='information')
            return
        self.current_folder = open_folder_name

        inner_folders = [i for i in self.lst_inner_dir()]
        if len(inner_folders) == 0:
            self.log_and_dialog("[GD PH1-OPEN FOLDER] ERROR, No Meta File Detected!",
                                "[GD PH1]", "错误，没有检测到二阶段Meta信息。", type_='critical')
            self.current_folder = None
            return
        # 判断本次和之前是否一致

        self.text_logs.append(f"[GD PH1-OPEN FOLDER] `{open_folder_name}`")
        # 每次成功加载时清空路径
        self.change_model_info()

    def next(self):
        if not self.current_files or len(self.current_files) == 0:
            return
        if self.current_files_idx >= len(self.current_files) - 1:
            return
        self.current_files_idx += 1
        self.setup_img(self.current_files[self.current_files_idx])
        self.setup_label()

    def previous(self):
        if not self.current_files or len(self.current_files) == 0:
            return
        if self.current_files_idx <= 0:
            return
        self.current_files_idx -= 1
        self.setup_img(self.current_files[self.current_files_idx])
        self.setup_label()

    def iadd(self, a, b, c):
        self.percentage += 100 * 1 / b
        self.progressBar.setValue(int(self.percentage))
        self.progressBar.update()
        self.text_logs.append(c)

    def predict(self):
        if not self.current_folder or not exists(self.current_folder):
            self.log_and_dialog("[GD P2-PREDICT] Folder Not Found!", "Not Found", type_='critical')
            return
        # 清楚状态
        if self.model:
            self.model.setRootPath(self.current_folder)
            self.treeView.update()
        if self.scene:
            self.scene.clear()
        if self.scene_ori:
            self.scene_ori.clear()
        self.show_net_btn.setText('显示网络结果')

        # init
        self.current_meta = None
        self.current_files = None
        self.current_files_idx = 0
        self.current_inner_folder = None

        # 开始执行
        self.current_phase_two = PhaseTwo(self.current_folder)
        wk = WorkerThread(self.current_phase_two.run, parent=self)
        self.wkt = wk
        wk.trigger.connect(self.task_finished)
        self.current_phase_two.iter_callback.connect(self.iadd)
        self.progressBar.setVisible(True)
        wk.start()
