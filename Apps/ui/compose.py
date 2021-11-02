# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compose.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(677, 465)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(260, 190, 58, 16))
        self.label_5.setObjectName("label_5")
        self.title_le = QtWidgets.QLineEdit(Form)
        self.title_le.setGeometry(QtCore.QRect(310, 100, 231, 21))
        self.title_le.setText("")
        self.title_le.setObjectName("title_le")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(400, 160, 58, 16))
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(260, 100, 58, 16))
        self.label_2.setObjectName("label_2")
        self.author_le = QtWidgets.QLineEdit(Form)
        self.author_le.setGeometry(QtCore.QRect(310, 130, 231, 21))
        self.author_le.setObjectName("author_le")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(260, 160, 58, 16))
        self.label_3.setObjectName("label_3")
        self.speed_le = QtWidgets.QLineEdit(Form)
        self.speed_le.setGeometry(QtCore.QRect(310, 160, 81, 21))
        self.speed_le.setObjectName("speed_le")
        self.clef_le = QtWidgets.QLineEdit(Form)
        self.clef_le.setGeometry(QtCore.QRect(440, 160, 101, 21))
        self.clef_le.setObjectName("clef_le")
        self.ts_le = QtWidgets.QLineEdit(Form)
        self.ts_le.setGeometry(QtCore.QRect(310, 190, 81, 21))
        self.ts_le.setObjectName("ts_le")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(260, 130, 58, 16))
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(360, 60, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.open_folder_btn = QtWidgets.QPushButton(Form)
        self.open_folder_btn.setGeometry(QtCore.QRect(270, 240, 100, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-exit-to-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_folder_btn.setIcon(icon)
        self.open_folder_btn.setObjectName("open_folder_btn")
        self.export_btn = QtWidgets.QPushButton(Form)
        self.export_btn.setGeometry(QtCore.QRect(380, 240, 71, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-cursor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export_btn.setIcon(icon1)
        self.export_btn.setObjectName("export_btn")
        self.popopen_btn = QtWidgets.QPushButton(Form)
        self.popopen_btn.setGeometry(QtCore.QRect(460, 240, 71, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-window-restore.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.popopen_btn.setIcon(icon2)
        self.popopen_btn.setObjectName("popopen_btn")
        self.status_now = QtWidgets.QLabel(Form)
        self.status_now.setGeometry(QtCore.QRect(260, 280, 321, 20))
        self.status_now.setText("")
        self.status_now.setObjectName("status_now")
        self.text_logs = QtWidgets.QTextBrowser(Form)
        self.text_logs.setGeometry(QtCore.QRect(200, 310, 441, 111))
        self.text_logs.setObjectName("text_logs")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_5.setText(_translate("Form", "节奏型:"))
        self.label_4.setText(_translate("Form", "拍号:"))
        self.label_2.setText(_translate("Form", "标题:"))
        self.label_3.setText(_translate("Form", "拍速:"))
        self.clef_le.setPlaceholderText(_translate("Form", "g"))
        self.ts_le.setPlaceholderText(_translate("Form", "4/4"))
        self.label.setText(_translate("Form", "作者:"))
        self.label_6.setText(_translate("Form", "元信息编辑"))
        self.open_folder_btn.setText(_translate("Form", "打开文件夹"))
        self.export_btn.setText(_translate("Form", "导出"))
        self.popopen_btn.setText(_translate("Form", "打开"))
