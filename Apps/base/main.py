import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from qtpy import QtCore

from Apps.base.ui_functions import UIFunctionsMixin
from Apps.base.ui_main import Ui_MainWindow
from Apps.widget import MainWidget, PhaseOneWidget, PhaseThreeWidget
from Apps.widget import PhaseTwoWidget
from Apps.widget.compose_widget import ComposeWidget


class MainWindow(QMainWindow, UIFunctionsMixin):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.ui = Ui_MainWindow()
        self.main_page_widget = MainWidget()
        self.phase_one_widget = PhaseOneWidget()
        self.phase_two_widget = PhaseTwoWidget()
        self.phase_three_widget = PhaseThreeWidget()
        self.compose = ComposeWidget()
        self.ui.setupUi(self)
        self.ui.stackedWidget.addWidget(self.main_page_widget)
        self.ui.stackedWidget.addWidget(self.phase_one_widget)
        self.ui.stackedWidget.addWidget(self.phase_two_widget)
        self.ui.stackedWidget.addWidget(self.phase_three_widget)
        self.ui.stackedWidget.addWidget(self.compose)

        # PRINT ==> SYSTEM

        ########################################################################
        # START - WINDOW ATTRIBUTES
        ########################################################################

        # REMOVE ==> STANDARD TITLE BAR
        self.removeTitleBar(True)
        # ==> END ##

        # SET ==> WINDOW TITLE
        self.setWindowTitle('OMR System')
        self.labelTitle('Optical Musical Recognition System')
        self.labelDescription('~')
        # ==> END ##

        # WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # self.enableMaximumSize(self, 500, 720)
        # ==> END ##

        # ==> CREATE MENUS

        # ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: self.toggleMenu(220, True))
        # ==> END ##

        # ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        self.addNewMenu("STAGE", "btn_stage", "url(:/16x16/icons/16x16/cil-home.png)", True)
        self.addNewMenu("PHASE #1", "btn_phase_one", "url(:/16x16/icons/16x16/cil-battery-0.png)", True)
        self.addNewMenu("PHASE #2", "btn_phase_two", "url(:/16x16/icons/16x16/cil-battery-3.png)", True)
        self.addNewMenu("PHASE #3", "btn_phase_three", "url(:/16x16/icons/16x16/cil-battery-5.png)",
                        True)
        self.addNewMenu("COMPOSE", "btn_compose", "url(:/16x16/icons/16x16/cil-check-circle.png)", True)
        self.addNewMenu("SETTINGS", "btn_productPyQt5", "url(:/16x16/icons/16x16/cil-equalizer.png)",
                        False)
        # ==> END ##

        # START MENU => SELECTION
        self.selectStandardMenu("btn_stage")
        # self.selectStandardMenu(self, "btn_phase_one")
        # self.selectStandardMenu(self, "btn_phase_two")
        # self.selectStandardMenu(self, "btn_phase_three")
        # self.selectStandardMenu(self, "btn_compose")
        # ==> END ##

        # ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.main_page_widget)
        # ==> END ##

        # USER ICON ==> SHOW HIDE
        self.userIcon("WM", "", True)

        # ==> END ##

        # ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if self.returStatus() == 1:
                self.maximize_restore()

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        # ==> END ##

        # ==> LOAD DEFINITIONS
        ########################################################################
        self.uiDefinitions()
        # ==> END ##

        ########################################################################
        # END - WINDOW ATTRIBUTES

        ########################################################################
        #                                                                      #
        # START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- ##
        #                                                                      #
        # ==> USER CODES BELLOW                                              ##
        ########################################################################

        # ==> QTableWidget RARAMETERS
        ########################################################################
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # ==> END ##

        ########################################################################
        #                                                                      #
        # END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- ##
        #                                                                      #

        # SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        # ==> END ##

    def _soft_close(self):
        if self.main_page_widget.current_task is not None:
            qm_res = QMessageBox.question(self, "Close", "Are you sure to close the app, since there "
                                                         "are backgrounds threads running?")
            if qm_res == QMessageBox.Yes:
                self.main_page_widget.current_task.stop()
                for task in self.main_page_widget.current_phases:
                    task.leave()
            else:
                return

            # 检测线程是否关闭
            while not self.main_page_widget.current_task.finished:
                # TODO
                pass

        else:
            self.close()

    ########################################################################
    # MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_stage":
            self.ui.stackedWidget.setCurrentWidget(self.main_page_widget)
            self.resetStyle("btn_stage")
            self.labelPage("STAGE")
            btnWidget.setStyleSheet(self.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_phase_one":
            self.ui.stackedWidget.setCurrentWidget(self.phase_one_widget)
            self.resetStyle("btn_phase_one")
            self.labelPage("PHASE ONE")
            btnWidget.setStyleSheet(self.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_phase_two":
            self.ui.stackedWidget.setCurrentWidget(self.phase_two_widget)
            self.resetStyle("btn_phase_two")
            self.labelPage("PHASE TWO")
            btnWidget.setStyleSheet(self.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_phase_three":
            self.ui.stackedWidget.setCurrentWidget(self.phase_three_widget)
            self.resetStyle("btn_phase_three")
            self.labelPage("PHASE THREE")
            btnWidget.setStyleSheet(self.selectMenu(btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_compose":
            self.ui.stackedWidget.setCurrentWidget(self.compose)
            self.resetStyle("btn_compose")
            self.labelPage("COMPOSE")
            btnWidget.setStyleSheet(self.selectMenu(btnWidget.styleSheet()))

    # ==> END ##

    ########################################################################
    # START ==> APP EVENTS
    ########################################################################

    # EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    # ==> END ##

    # EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')

    # ==> END ##

    # EVENT ==> KEY PRESSED
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))

    # ==> END ##

    # EVENT ==> RESIZE EVENT
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))


def run():
    app = QApplication(sys.argv)
    QCoreApplication.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles)
    app.setStyleSheet(u"/* LINE EDIT */\n"
                      "QLineEdit {\n"
                      "	background-color: rgb(27, 29, 35);\n"
                      "	border-radius: 5px;\n"
                      "	border: 2px solid rgb(27, 29, 35);\n"
                      "	padding-left: 10px;\n"
                      "}\n"
                      "QLineEdit:hover {\n"
                      "	border: 2px solid rgb(64, 71, 88);\n"
                      "}\n"
                      "QLineEdit:focus {\n"
                      "	border: 2px solid rgb(91, 101, 124);\n"
                      "}\n"
                      "\n"
                      "/* SCROLL BARS */\n"
                      "QScrollBar:horizontal {\n"
                      "    border: none;\n"
                      "    background: rgb(52, 59, 72);\n"
                      "    height: 14px;\n"
                      "    margin: 0px 21px 0 21px;\n"
                      "	border-radius: 0px;\n"
                      "}\n"
                      "QScrollBar::handle:horizontal {\n"
                      "    background: rgb(85, 170, 255);\n"
                      "    min-width: 25px;\n"
                      "	border-radius: 7px\n"
                      "}\n"
                      "QScrollBar::add-line:horizontal {\n"
                      "    border: none;\n"
                      "    background: rgb(55, 63, 77);\n"
                      "    width: 20px;\n"
                      "	border-top-right-radius: 7px;\n"
                      "    border-bottom-right-radius: 7px;\n"
                      "    subcontrol-position: right;\n"
                      "    subcontrol-origin: margin;\n"
                      "}\n"
                      "QScrollBar::sub-line:horizontal {\n"
                      "    border: none;\n"
                      "    background: rgb(55, 63, 77);\n"
                      "    width: 20px;\n"
                      ""
                      "	border-top-left-radius: 7px;\n"
                      "    border-bottom-left-radius: 7px;\n"
                      "    subcontrol-position: left;\n"
                      "    subcontrol-origin: margin;\n"
                      "}\n"
                      "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
                      "{\n"
                      "     background: none;\n"
                      "}\n"
                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
                      "{\n"
                      "     background: none;\n"
                      "}\n"
                      " QScrollBar:vertical {\n"
                      "	border: none;\n"
                      "    background: rgb(52, 59, 72);\n"
                      "    width: 14px;\n"
                      "    margin: 21px 0 21px 0;\n"
                      "	border-radius: 0px;\n"
                      " }\n"
                      " QScrollBar::handle:vertical {	\n"
                      "	background: rgb(85, 170, 255);\n"
                      "    min-height: 25px;\n"
                      "	border-radius: 7px\n"
                      " }\n"
                      " QScrollBar::add-line:vertical {\n"
                      "     border: none;\n"
                      "    background: rgb(55, 63, 77);\n"
                      "     height: 20px;\n"
                      "	border-bottom-left-radius: 7px;\n"
                      "    border-bottom-right-radius: 7px;\n"
                      "     subcontrol-position: bottom;\n"
                      "     subcontrol-origin: margin;\n"
                      " }\n"
                      " QScrollBar::sub-line:vertical {\n"
                      "	border: none;\n"
                      "    background: rgb(55, 63"
                      ", 77);\n"
                      "     height: 20px;\n"
                      "	border-top-left-radius: 7px;\n"
                      "    border-top-right-radius: 7px;\n"
                      "     subcontrol-position: top;\n"
                      "     subcontrol-origin: margin;\n"
                      " }\n"
                      " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                      "     background: none;\n"
                      " }\n"
                      "\n"
                      " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                      "     background: none;\n"
                      " }\n"
                      "\n"
                      "/* CHECKBOX */\n"
                      "QCheckBox::indicator {\n"
                      "    border: 3px solid rgb(52, 59, 72);\n"
                      "	width: 15px;\n"
                      "	height: 15px;\n"
                      "	border-radius: 10px;\n"
                      "    background: rgb(44, 49, 60);\n"
                      "}\n"
                      "QCheckBox::indicator:hover {\n"
                      "    border: 3px solid rgb(58, 66, 81);\n"
                      "}\n"
                      "QCheckBox::indicator:checked {\n"
                      "    background: 3px solid rgb(52, 59, 72);\n"
                      "	border: 3px solid rgb(52, 59, 72);	\n"
                      "	background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
                      "}\n"
                      "\n"
                      "/* RADIO BUTTON */\n"
                      "QRadioButton::indicator {\n"
                      "    border: 3px solid rgb(52, 59, 72);\n"
                      "	width: 15px;\n"
                      "	height: 15px;\n"
                      "	border-radius"
                      ": 10px;\n"
                      "    background: rgb(44, 49, 60);\n"
                      "}\n"
                      "QRadioButton::indicator:hover {\n"
                      "    border: 3px solid rgb(58, 66, 81);\n"
                      "}\n"
                      "QRadioButton::indicator:checked {\n"
                      "    background: 3px solid rgb(94, 106, 130);\n"
                      "	border: 3px solid rgb(52, 59, 72);	\n"
                      "}\n"
                      "\n"
                      "/* COMBOBOX */\n"
                      "QComboBox{\n"
                      "	background-color: rgb(27, 29, 35);\n"
                      "	border-radius: 5px;\n"
                      "	border: 2px solid rgb(27, 29, 35);\n"
                      "	padding: 5px;\n"
                      "	padding-left: 10px;\n"
                      "}\n"
                      "QComboBox:hover{\n"
                      "	border: 2px solid rgb(64, 71, 88);\n"
                      "}\n"
                      "QComboBox::drop-down {\n"
                      "	subcontrol-origin: padding;\n"
                      "	subcontrol-position: top right;\n"
                      "	width: 25px; \n"
                      "	border-left-width: 3px;\n"
                      "	border-left-color: rgba(39, 44, 54, 150);\n"
                      "	border-left-style: solid;\n"
                      "	border-top-right-radius: 3px;\n"
                      "	border-bottom-right-radius: 3px;	\n"
                      "	background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
                      "	background-position: center;\n"
                      "	background-repeat: no-reperat;\n"
                      " }\n"
                      "QComboBox QAbstractItemView {\n"
                      "	color: rgb("
                      "85, 170, 255);	\n"
                      "	background-color: rgb(27, 29, 35);\n"
                      "	padding: 10px;\n"
                      "	selection-background-color: rgb(39, 44, 54);\n"
                      "}\n"
                      "\n"
                      "/* SLIDERS */\n"
                      "QSlider::groove:horizontal {\n"
                      "    border-radius: 9px;\n"
                      "    height: 18px;\n"
                      "	margin: 0px;\n"
                      "	background-color: rgb(52, 59, 72);\n"
                      "}\n"
                      "QSlider::groove:horizontal:hover {\n"
                      "	background-color: rgb(55, 62, 76);\n"
                      "}\n"
                      "QSlider::handle:horizontal {\n"
                      "    background-color: rgb(85, 170, 255);\n"
                      "    border: none;\n"
                      "    height: 18px;\n"
                      "    width: 18px;\n"
                      "    margin: 0px;\n"
                      "	border-radius: 9px;\n"
                      "}\n"
                      "QSlider::handle:horizontal:hover {\n"
                      "    background-color: rgb(105, 180, 255);\n"
                      "}\n"
                      "QSlider::handle:horizontal:pressed {\n"
                      "    background-color: rgb(65, 130, 195);\n"
                      "}\n"
                      "\n"
                      "QSlider::groove:vertical {\n"
                      "    border-radius: 9px;\n"
                      "    width: 18px;\n"
                      "    margin: 0px;\n"
                      "	background-color: rgb(52, 59, 72);\n"
                      "}\n"
                      "QSlider::groove:vertical:hover {\n"
                      "	background-color: rgb(55, 62, 76);\n"
                      "}\n"
                      "QSlider::handle:verti"
                      "cal {\n"
                      "    background-color: rgb(85, 170, 255);\n"
                      "	border: none;\n"
                      "    height: 18px;\n"
                      "    width: 18px;\n"
                      "    margin: 0px;\n"
                      "	border-radius: 9px;\n"
                      "}\n"
                      "QSlider::handle:vertical:hover {\n"
                      "    background-color: rgb(105, 180, 255);\n"
                      "}\n"
                      "QSlider::handle:vertical:pressed {\n"
                      "    background-color: rgb(65, 130, 195);\n"
                      "}\n"
                      "\n"
                      "")
    font_out_scope = QFont()
    font_out_scope.setFamily(u"Segoe UI")
    font_out_scope.setPointSize(12)
    font_out_scope.setBold(False)
    font_out_scope.setWeight(75)
    app.setFont(font_out_scope)
    QtGui.QFontDatabase.addApplicationFont(
        '/Users/daipeiyuan/developer/PyCharm/graduation_design/Apps/base/fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont(
        '/Users/daipeiyuan/developer/PyCharm/graduation_design/Apps/base/fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
