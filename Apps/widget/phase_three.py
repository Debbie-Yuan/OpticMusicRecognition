from os import listdir
from os.path import exists, join, isdir, splitext

from PIL import ImageQt
from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QFileDialog, QGraphicsScene, QGraphicsPixmapItem, QFileSystemModel, \
    QMessageBox, QAbstractItemView

from Apps.ui import P3Ui
from Apps.widget.commom import WorkerThread
from logic import PhaseThree
from models import CLS_NAME
from settings import CWD


class PhaseThreeWidget(QWidget, P3Ui):

    def __init__(self, parent=None):
        super(PhaseThreeWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.current_phase_three: [PhaseThree or None] = None
        self.scene = None
        self.wkt = None
        self.current_folder = None
        self.current_inner_folder = None
        self.current_files = None
        self.current_files_idx = 0
        self.current_classes = None
        self.current_meta = None
        self.item = None
        self.zoom_scale = 1
        self.percentage = 0
        self.connect()
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
        self.p1_predict.clicked.connect(self.predict)

    def lst_dir(self):
        if not self.current_inner_folder:
            return
        for fn in listdir(self.current_inner_folder):
            if not fn.startswith('.') and not \
                    isdir(join(self.current_inner_folder, fn)) and not \
                    fn.endswith('.txt') and 'p2-net' not in fn and 'p2-ori' not in fn:
                yield fn

    def load_res(self):
        if not self.current_inner_folder:
            return
        cls = [line.strip('\n') for line in open(join(self.current_inner_folder, 'p3res.txt'), 'r').readlines() if
               line != '\n']
        for cls_list in cls:
            yield tuple(int(k) for k in cls_list.split(' '))

    def setup_class_name_score(self):
        if len(self.current_files) <= 0:
            return
        self.class_browser.clear()
        for cls in self.current_classes[self.current_files_idx]:
            self.class_browser.append(f"{cls} -> {CLS_NAME[cls]}")

    def setup_file_details(self):
        p2_meta = self.current_meta
        p3_res = join(self.current_inner_folder, 'p3res.txt')
        if not exists(p2_meta) or not exists(p3_res):
            return
        p2_meta_content = open(p2_meta, 'r').read()
        p3_res_content = open(p3_res, 'r').read()
        self.text_browser_sd.clear()
        self.text_browser_sd.append(p2_meta_content)
        self.text_browser_ci.clear()
        self.text_browser_ci.append(p3_res_content)

    def tree_item_changed(self, a0: QModelIndex):
        abs_pth = join(self.current_folder, a0.data())
        if not isdir(abs_pth):
            return
        # 更新视图函数

        # 获取点击文件夹路径
        self.current_fn_label.setText(a0.data())
        self.current_inner_folder = join(self.current_folder, a0.data())
        self.current_meta = join(self.current_inner_folder, '.p2meta.txt')
        self.current_files = [i for i in self.lst_dir()]
        # 加载结果
        self.current_classes = [i for i in self.load_res()]
        if len(self.current_files) > 0:
            self.current_files_idx = 0
        else:
            return
        self.setup_img(self.current_files[self.current_files_idx])
        self.setup_label()
        self.setup_class_name_score()
        self.setup_file_details()

    def lst_inner_dir(self):
        for folder in listdir(self.current_folder):
            abs_pth = join(self.current_folder, folder)
            if isdir(abs_pth) and exists(join(abs_pth, 'p3res.txt')):
                yield folder

    def setup_label(self):
        _, folder_name = splitext(self.current_inner_folder)
        f_pth = join(folder_name, self.current_files[self.current_files_idx])
        self.current_fn_label.setText(f_pth)
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

    def task_finished(self):
        self.wkt = None
        self.text_logs.append(f"[GD UI-PhaseThree] Predict finished. Saved to folder `{self.current_phase_three.cwd}`.")
        self.change_model_info()
        self.percentage = 0
        self.progress_val.setText('已完成')

    def open_file_handler(self):
        open_file_name = QFileDialog.getExistingDirectory(self, '打开二阶段结果')
        if open_file_name == '':
            self.text_logs.append(f"[GD P3-OFH:199] [INFO] File not choose.")
            return
        if not exists(join(open_file_name, '.p1meta.txt')):
            self.log_and_dialog("[GD P3-OFH:202] Folder Format Incorrect.", 'Incorrect', type_='critical')
            return
        self.current_folder = open_file_name
        self.fn_chooser.setText(open_file_name)
        self.text_logs.append(f"[GD P3-OFH:206] File `{open_file_name}` selected.")

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
                                "[GD PH1]", "错误，没有检测到二阶段Meta信息或三阶段结果。", type_='critical')
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
        self.setup_class_name_score()

    def previous(self):
        if not self.current_files or len(self.current_files) == 0:
            return
        if self.current_files_idx <= 0:
            return
        self.current_files_idx -= 1
        self.setup_img(self.current_files[self.current_files_idx])
        self.setup_label()
        self.setup_class_name_score()

    def iadd(self, a, b, c):
        self.percentage += 100 * 1 / b
        self.progressBar.setValue(int(self.percentage))
        self.progressBar.update()
        self.progress_val.setText("{:.2f}".format(self.percentage) + '%')
        self.text_logs.append(c)

    def predict(self):
        if not self.current_folder or not exists(self.current_folder):
            self.log_and_dialog("[GD P3-PREDICT] Folder Not Found!", "Not Found", type_='critical')
            return
        if self.wkt is not None:
            return
        # 清楚状态
        if self.model:
            self.model.setRootPath(self.current_folder)
            self.treeView.update()
        if self.scene:
            self.scene.clear()

        # init
        self.current_meta = None
        self.current_files = None
        self.current_files_idx = 0
        self.current_inner_folder = None
        self.current_classes = None

        # 开始执行
        self.current_phase_three = PhaseThree(self.current_folder)
        wk = WorkerThread(self.current_phase_three.run, parent=self)
        self.wkt = wk
        wk.trigger.connect(self.task_finished)
        self.current_phase_three.iter_callback.connect(self.iadd)
        wk.start()
