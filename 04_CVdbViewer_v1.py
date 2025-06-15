import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic, QtCore, QtGui, QtWidgets

import os
import shutil
import pickle
import pandas as pd
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(661, 761)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 623, 725))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_5.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.cb_at_cash_register = QtWidgets.QCheckBox(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_at_cash_register.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_at_cash_register.setFont(font)
        self.cb_at_cash_register.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_at_cash_register.setAutoFillBackground(False)
        self.cb_at_cash_register.setCheckable(True)
        self.cb_at_cash_register.setAutoExclusive(False)
        self.cb_at_cash_register.setTristate(False)
        self.cb_at_cash_register.setObjectName("cb_at_cash_register")
        self.gridLayout.addWidget(self.cb_at_cash_register, 13, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_7.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 11, 0, 1, 4)
        self.pb_set_certain_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_set_certain_zone.setEnabled(True)
        self.pb_set_certain_zone.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_set_certain_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_set_certain_zone.setFont(font)
        self.pb_set_certain_zone.setObjectName("pb_set_certain_zone")
        self.gridLayout.addWidget(self.pb_set_certain_zone, 14, 3, 1, 1)
        self.le_date_start = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_date_start.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_date_start.setFont(font)
        self.le_date_start.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_date_start.setText("")
        self.le_date_start.setMaxLength(12)
        self.le_date_start.setObjectName("le_date_start")
        self.gridLayout.addWidget(self.le_date_start, 8, 1, 1, 1)
        self.cb_shape_zone = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_shape_zone.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_shape_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_shape_zone.setFont(font)
        self.cb_shape_zone.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_shape_zone.setAutoFillBackground(False)
        self.cb_shape_zone.setObjectName("cb_shape_zone")
        self.gridLayout.addWidget(self.cb_shape_zone, 16, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 4)
        self.label_1 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_1.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 4)
        self.pb_last_10_days_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_last_10_days_1.setEnabled(True)
        self.pb_last_10_days_1.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_last_10_days_1.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pb_last_10_days_1.setFont(font)
        self.pb_last_10_days_1.setObjectName("pb_last_10_days_1")
        self.gridLayout.addWidget(self.pb_last_10_days_1, 8, 2, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 2, 1, 2)
        self.label_total = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(False)
        font.setWeight(50)
        self.label_total.setFont(font)
        self.label_total.setMouseTracking(False)
        self.label_total.setText("")
        self.label_total.setAlignment(QtCore.Qt.AlignCenter)
        self.label_total.setWordWrap(True)
        self.label_total.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_total.setObjectName("label_total")
        self.gridLayout.addWidget(self.label_total, 15, 1, 4, 3)
        self.cb_face_zone = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_face_zone.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_face_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_face_zone.setFont(font)
        self.cb_face_zone.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_face_zone.setAutoFillBackground(False)
        self.cb_face_zone.setObjectName("cb_face_zone")
        self.gridLayout.addWidget(self.cb_face_zone, 17, 0, 1, 1)
        self.le_certain_zone = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_certain_zone.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_certain_zone.setFont(font)
        self.le_certain_zone.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_certain_zone.setText("")
        self.le_certain_zone.setObjectName("le_certain_zone")
        self.gridLayout.addWidget(self.le_certain_zone, 14, 1, 1, 2)
        self.cb_shape_bbox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_shape_bbox.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_shape_bbox.setFont(font)
        self.cb_shape_bbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_shape_bbox.setAutoFillBackground(False)
        self.cb_shape_bbox.setChecked(True)
        self.cb_shape_bbox.setObjectName("cb_shape_bbox")
        self.gridLayout.addWidget(self.cb_shape_bbox, 15, 0, 1, 1)
        self.le_cam_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_cam_name.setFont(font)
        self.le_cam_name.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_cam_name.setInputMask("")
        self.le_cam_name.setText("")
        self.le_cam_name.setObjectName("le_cam_name")
        self.gridLayout.addWidget(self.le_cam_name, 4, 1, 1, 1)
        self.pb_last_10_days_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_last_10_days_2.setEnabled(True)
        self.pb_last_10_days_2.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_last_10_days_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pb_last_10_days_2.setFont(font)
        self.pb_last_10_days_2.setObjectName("pb_last_10_days_2")
        self.gridLayout.addWidget(self.pb_last_10_days_2, 9, 2, 1, 2)
        self.pb_thanks = QtWidgets.QPushButton(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(104, 104, 104))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(104, 104, 104))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.pb_thanks.setPalette(palette)
        self.pb_thanks.setObjectName("pb_thanks")
        self.gridLayout.addWidget(self.pb_thanks, 24, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 19, 0, 1, 4)
        self.pb_estimate = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_estimate.setEnabled(True)
        self.pb_estimate.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_estimate.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_estimate.setFont(font)
        self.pb_estimate.setObjectName("pb_estimate")
        self.gridLayout.addWidget(self.pb_estimate, 18, 0, 1, 1)
        self.label_wishes_thanks = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_wishes_thanks.setFont(font)
        self.label_wishes_thanks.setMouseTracking(False)
        self.label_wishes_thanks.setText("")
        self.label_wishes_thanks.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_wishes_thanks.setWordWrap(True)
        self.label_wishes_thanks.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_wishes_thanks.setObjectName("label_wishes_thanks")
        self.gridLayout.addWidget(self.label_wishes_thanks, 23, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 4)
        self.cb_certain_zone = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.cb_certain_zone.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_certain_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_certain_zone.setFont(font)
        self.cb_certain_zone.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_certain_zone.setAutoFillBackground(False)
        self.cb_certain_zone.setAutoExclusive(False)
        self.cb_certain_zone.setObjectName("cb_certain_zone")
        self.gridLayout.addWidget(self.cb_certain_zone, 14, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_4.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 4)
        self.le_date_end = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_date_end.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_date_end.setFont(font)
        self.le_date_end.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_date_end.setText("")
        self.le_date_end.setMaxLength(12)
        self.le_date_end.setObjectName("le_date_end")
        self.gridLayout.addWidget(self.le_date_end, 9, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 4)
        self.pb_choose_cam = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_choose_cam.setEnabled(True)
        self.pb_choose_cam.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_choose_cam.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_choose_cam.setFont(font)
        self.pb_choose_cam.setObjectName("pb_choose_cam")
        self.gridLayout.addWidget(self.pb_choose_cam, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_6.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 9, 0, 1, 1)
        self.label_out = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_out.setFont(font)
        self.label_out.setMouseTracking(False)
        self.label_out.setText("")
        self.label_out.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_out.setWordWrap(True)
        self.label_out.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_out.setObjectName("label_out")
        self.gridLayout.addWidget(self.label_out, 22, 0, 1, 4)
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 20, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_9.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 13, 1, 1, 2)
        self.pb_wishes = QtWidgets.QPushButton(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(104, 104, 104))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(104, 104, 104))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.pb_wishes.setPalette(palette)
        self.pb_wishes.setAutoExclusive(False)
        self.pb_wishes.setAutoDefault(True)
        self.pb_wishes.setObjectName("pb_wishes")
        self.gridLayout.addWidget(self.pb_wishes, 24, 0, 1, 3)
        self.pb_show_in_fold = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_show_in_fold.setEnabled(True)
        self.pb_show_in_fold.setMinimumSize(QtCore.QSize(0, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(83, 83, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.pb_show_in_fold.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_show_in_fold.setFont(font)
        self.pb_show_in_fold.setObjectName("pb_show_in_fold")
        self.gridLayout.addWidget(self.pb_show_in_fold, 20, 1, 1, 3)
        self.cb_general_det_aria = QtWidgets.QCheckBox(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_general_det_aria.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_general_det_aria.setFont(font)
        self.cb_general_det_aria.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_general_det_aria.setAutoFillBackground(False)
        self.cb_general_det_aria.setChecked(True)
        self.cb_general_det_aria.setObjectName("cb_general_det_aria")
        self.gridLayout.addWidget(self.cb_general_det_aria, 12, 0, 1, 1)
        self.cb_more_then_two = QtWidgets.QCheckBox(self.gridLayoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.cb_more_then_two.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_more_then_two.setFont(font)
        self.cb_more_then_two.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cb_more_then_two.setAutoFillBackground(False)
        self.cb_more_then_two.setChecked(True)
        self.cb_more_then_two.setObjectName("cb_more_then_two")
        self.gridLayout.addWidget(self.cb_more_then_two, 12, 1, 1, 2)
        self.label_wishes_thanks.setBuddy(self.pb_wishes)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pb_choose_cam, self.le_cam_name)
        Dialog.setTabOrder(self.le_cam_name, self.le_date_start)
        Dialog.setTabOrder(self.le_date_start, self.pb_last_10_days_1)
        Dialog.setTabOrder(self.pb_last_10_days_1, self.le_date_end)
        Dialog.setTabOrder(self.le_date_end, self.pb_last_10_days_2)
        Dialog.setTabOrder(self.pb_last_10_days_2, self.cb_general_det_aria)
        Dialog.setTabOrder(self.cb_general_det_aria, self.cb_more_then_two)
        Dialog.setTabOrder(self.cb_more_then_two, self.cb_at_cash_register)
        Dialog.setTabOrder(self.cb_at_cash_register, self.cb_certain_zone)
        Dialog.setTabOrder(self.cb_certain_zone, self.le_certain_zone)
        Dialog.setTabOrder(self.le_certain_zone, self.pb_set_certain_zone)
        Dialog.setTabOrder(self.pb_set_certain_zone, self.cb_shape_bbox)
        Dialog.setTabOrder(self.cb_shape_bbox, self.cb_shape_zone)
        Dialog.setTabOrder(self.cb_shape_zone, self.cb_face_zone)
        Dialog.setTabOrder(self.cb_face_zone, self.pb_estimate)
        Dialog.setTabOrder(self.pb_estimate, self.pb_show_in_fold)
        Dialog.setTabOrder(self.pb_show_in_fold, self.pb_wishes)
        Dialog.setTabOrder(self.pb_wishes, self.pb_thanks)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CVdbViewer"))
        self.label_5.setText(_translate("Dialog", "Нижняя граница (вкл): [ 231121 -"))
        self.cb_at_cash_register.setText(_translate("Dialog", "только у кассы"))
        self.label_7.setText(_translate("Dialog", "Показать обнаруженных людей на фотографиях:"))
        self.pb_set_certain_zone.setText(_translate("Dialog", "задать"))
        self.cb_shape_zone.setText(_translate("Dialog", "рамка общей зоны детекции"))
        self.label_3.setText(_translate("Dialog", "работает в корневой папке системы с базой данных CV и базой фотографий"))
        self.label_1.setText(_translate("Dialog", "Программа для визуализации работы "))
        self.pb_last_10_days_1.setText(_translate("Dialog", "последние 10 дней"))
        self.cb_face_zone.setText(_translate("Dialog", "рамка зоны детекции у кассы"))
        self.cb_shape_bbox.setText(_translate("Dialog", " рамка силуэта"))
        self.pb_last_10_days_2.setText(_translate("Dialog", "последние 10 дней"))
        self.pb_thanks.setText(_translate("Dialog", "Спасибо!"))
        self.pb_estimate.setText(_translate("Dialog", "Оценить количество"))
        self.cb_certain_zone.setText(_translate("Dialog", "только в заданной зоне"))
        self.label_4.setText(_translate("Dialog", "Задать промежуток времени (ггммддччмм):"))
        self.label_2.setText(_translate("Dialog", "системы CV на фотографиях"))
        self.pb_choose_cam.setText(_translate("Dialog", "Камера"))
        self.label_6.setText(_translate("Dialog", "Верхняя граница (вкл): - 240101 ]"))
        self.label_9.setText(_translate("Dialog", "y1, y2, x1, x2"))
        self.pb_wishes.setText(_translate("Dialog", "Пожелания"))
        self.pb_show_in_fold.setText(_translate("Dialog", "Показать в папке imgs_cvdb"))
        self.cb_general_det_aria.setText(_translate("Dialog", "только в общей зоне детекции"))
        self.cb_more_then_two.setText(_translate("Dialog", "    от двух (продавец +)"))


class ShowCams(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super(ShowCams, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window

        self.setWindowTitle('Выберете камеру')
        lay = QtWidgets.QVBoxLayout(self)
        for cam in self.main_window.cam_names:
            btn = QPushButton()
            btn.setText(cam)
            btn.released.connect(self.button_clicked)
            lay.addWidget(btn)

        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-292, centerPoint.y()-205, 0, 0)

    def button_clicked(self):
        clicked_button = self.sender()
        self.main_window.le_cam_name.setText(clicked_button.text())
        self.close()
        self.main_window.le_date_start.setEnabled(True)
        self.main_window.le_date_end.setEnabled(True)
        self.main_window.pb_last_10_days_1.setEnabled(True)
        self.main_window.pb_last_10_days_2.setEnabled(True)
        self.main_window.progressBar.setValue(0)


class Showlast10days(QtWidgets.QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(Showlast10days, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()

        self.setWindowTitle('Выберете день')
        lay = QtWidgets.QVBoxLayout(self)
        imgs_path = self.main_window.ip_cam_data_paths_dict[self.cam_name]
        days = [day[2:] for day in os.listdir(imgs_path)][-10:]

        for day in days:
            btn = QPushButton()
            btn.setText(day)
            btn.released.connect(self.button_clicked)
            lay.addWidget(btn)

        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()+158, centerPoint.y()-40, 0, 0)

    def button_clicked(self):
        clicked_button = self.sender()
        if self.direction == 'start':
            self.main_window.le_date_start.setText(clicked_button.text())
        else:
            self.main_window.le_date_end.setText(clicked_button.text())
        self.close()


class SetZoneWindow(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super(SetZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()
        self.scene = QtWidgets.QGraphicsScene(self)

        self.setWindowTitle('Задать зону детекции')
        self.image = QLabel()

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.image)

        imgs_path = self.main_window.ip_cam_data_paths_dict[self.cam_name]
        first_range_day = '20' + date_start[:6]
        images = os.listdir(os.path.join(imgs_path, first_range_day))
        first_range_img = [img for img in images if img[:len(date_start)] == date_start][0]
        img_path = os.path.join(imgs_path, first_range_day, first_range_img)

        self.pixmap = QPixmap(img_path)
        self.pixmap_small = self.pixmap.scaled(int(self.pixmap.width() / 1.5), int(self.pixmap.height() / 1.5))
        self.setGeometry(320, 200, 0, 0)
        self.setMinimumSize(int(self.pixmap_small.width()), int(self.pixmap_small.height()))

        self.begin, self.destination = QPoint(), QPoint()

    def load_camconfig(self):
        camconfig = []
        if os.path.exists(os.path.join(os.getcwd(), 'db', 'camconfig.csv')):
            camconfig = pd.read_csv(os.path.join(os.getcwd(), 'db', 'camconfig.csv'))
            camconfig = camconfig.to_dict(orient='records')
        return camconfig

    def save_camconfig(self, camconfig):
        camconfig = pd.DataFrame(camconfig)
        camconfig.to_csv(os.path.join(os.getcwd(), 'db', 'camconfig.csv'), index=False)

    def get_coords_from_text(self, coords):
        if len(coords.split(',')) == 4:
            # Single zone coords
            dirty_list = coords[1:-1].split(',')
            ymin = int(dirty_list[0])
            ymax = int(dirty_list[1][1:])
            xmin = int(dirty_list[2][1:])
            xmax = int(dirty_list[3][1:])
            return ymin, ymax, xmin, xmax

        if len(coords.split(',')) == 8:
            # Double zone coords
            l0 = coords.split(')')[0][2:].split(',')
            t0 = tuple(np.array(l0, dtype='int'))
            l1 = coords.split(')')[1][3:].split(',')
            t1 = tuple(np.array(l1, dtype='int'))
            return [t0, t1]

        if len(coords.split(',')) == 12:
            # Triple zone coords
            l0 = coords.split(')')[0][2:].split(',')
            t0 = tuple(np.array(l0, dtype='int'))
            l1 = coords.split(')')[1][3:].split(',')
            t1 = tuple(np.array(l1, dtype='int'))
            l2 = coords.split(')')[2][3:].split(',')
            t2 = tuple(np.array(l2, dtype='int'))
            return [t0, t1, t2]

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.yellow, 2)
        painter.setPen(pen)
        br = QtGui.QBrush(QtGui.QColor(200, 10, 10, 40))
        painter.setBrush(br)
        painter.drawPixmap(QPoint(), self.pixmap_small)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.drawRect(rect.normalized())

        x1 = int(self.begin.x() * 1.5)
        y1 = int(self.begin.y() * 1.5)
        x2 = int(self.destination.x() * 1.5)
        y2 = int(self.destination.y() * 1.5)
        coords = (y1, y2, x1, x2)
        if sum(coords) != 0:
            self.main_window.le_certain_zone.setText(str(coords))

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pixmap_small)
            painter.drawRect(rect.normalized())
            self.begin, self.destination = QPoint, QPoint
            self.update()
        self.close()
        self.main_window.cb_certain_zone.setCheckState(True)


class EstimateThread(QThread):
    # Signals to the main UI thread
    # Signal that the thread has finished working
    finished = pyqtSignal()
    # Signal for messages output to the user
    output_message = pyqtSignal(str)
    total_num_message = pyqtSignal(str)
    enable_disable_ui = pyqtSignal(bool)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(EstimateThread, self).__init__(parent)
        self.main_window = main_window

    def run(self):
        def dt_slice_shape_df(df_cam, dt_start, dt_end):
            df = df_cam.copy()
            dt_end_full = str(int(dt_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            return df[(df['dt'] >= dt_start) & (df['dt'] <= dt_end_full)]

        def get_coords_from_text(coords):
            if len(coords.split(',')) == 4:
                # Single zone coords
                dirty_list = coords[1:-1].split(',')
                ymin = int(dirty_list[0])
                ymax = int(dirty_list[1][1:])
                xmin = int(dirty_list[2][1:])
                xmax = int(dirty_list[3][1:])
                return ymin, ymax, xmin, xmax

            if len(coords.split(',')) == 8:
                # Double zone coords
                l0 = coords.split(')')[0][2:].split(',')
                t0 = tuple(np.array(l0, dtype='int'))
                l1 = coords.split(')')[1][3:].split(',')
                t1 = tuple(np.array(l1, dtype='int'))
                return [t0, t1]

            if len(coords.split(',')) == 12:
                # Triple zone coords
                l0 = coords.split(')')[0][2:].split(',')
                t0 = tuple(np.array(l0, dtype='int'))
                l1 = coords.split(')')[1][3:].split(',')
                t1 = tuple(np.array(l1, dtype='int'))
                l2 = coords.split(')')[2][3:].split(',')
                t2 = tuple(np.array(l2, dtype='int'))
                return [t0, t1, t2]

        def zone_intersections(df, zone_coords):
            df = df.copy()
            df['alarm_intersection'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), zone_coords))
            return df[df['alarm_intersection'] == 1].iloc[:, 0:-1]

        def detection_zone_intersection(shape_location, zone_coords):
            if len(str(zone_coords).split(',')) == 4:
                # Single_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                if type(zone_coords) == tuple:
                    y1, y2, x1, x2 = zone_coords
                else:
                    y1, y2, x1, x2 = get_coords_from_text(zone_coords)

                dx = min(xmax, x2) - max(xmin, x1)
                dy = min(ymax, y2) - max(ymin, y1)

                if (dx >= 0) and (dy >= 0):
                    return 1
                else:
                    return 0

            if len(str(zone_coords).split(',')) == 8:
                # Double_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
                y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]

                dx0 = min(xmax, x02) - max(xmin, x01)
                dy0 = min(ymax, y02) - max(ymin, y01)
                dx1 = min(xmax, x12) - max(xmin, x11)
                dy1 = min(ymax, y12) - max(ymin, y11)

                if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)):
                    return 1
                else:
                    return 0

            if len(str(zone_coords).split(',')) == 12:
                # Triple_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
                y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]
                y21, y22, x21, x22 = get_coords_from_text(zone_coords)[2]

                dx0 = min(xmax, x02) - max(xmin, x01)
                dy0 = min(ymax, y02) - max(ymin, y01)
                dx1 = min(xmax, x12) - max(xmin, x11)
                dy1 = min(ymax, y12) - max(ymin, y11)
                dx2 = min(xmax, x22) - max(xmin, x21)
                dy2 = min(ymax, y22) - max(ymin, y21)

                if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)) | ((dx2 >= 0) and (dy2 >= 0)):
                    return 1
                else:
                    return 0

        ip_cam_data_paths_dict = self.main_window.ip_cam_data_paths_dict
        cam_names = self.main_window.cam_names
        cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.date_start
        date_end = self.main_window.date_end

        if cam_name not in cam_names:
            self.total_num_message.emit(self.main_window.text_error)
            self.output_message.emit(self.main_window.text_error_cam)
        else:
            if (len(date_start) & len(date_end)) == 0:
                self.total_num_message.emit(self.main_window.text_error)
                self.output_message.emit(self.main_window.text_error_date)
            else:
                first_photo_day = os.listdir(ip_cam_data_paths_dict[cam_name])[0]
                last_photo_day = os.listdir(ip_cam_data_paths_dict[cam_name])[-1]
                range_day_start = '20' + date_start[:6]
                range_day_end = '20' + date_end[:6]

                if not (range_day_start >= first_photo_day) & (last_photo_day >= range_day_end):
                    self.total_num_message.emit(self.main_window.text_error)
                    self.output_message.emit(self.main_window.text_error_bad_range)
                else:
                    self.enable_disable_ui.emit(False)
                    df_cam = pd.DataFrame()
                    if os.path.exists(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv')):
                        df_cam = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'))

                    slice_df = dt_slice_shape_df(df_cam, date_start, date_end)

                    if self.main_window.cb_general_det_aria.isChecked():
                        slice_df = slice_df[slice_df['shape_zone'] == 1]
                        df_ones = slice_df.drop_duplicates('origin_file_name')
                        total_num = len(df_ones)

                        if self.main_window.cb_more_then_two.isChecked():
                            df_mto = slice_df[slice_df.duplicated(subset='origin_file_name', keep=False)]
                            df_mto_ones = df_mto.drop_duplicates('origin_file_name')
                            total_num = len(df_mto_ones)
                            if self.main_window.cb_at_cash_register.isChecked():
                                df_mto_reg = df_mto[df_mto['face_zone'] == 1]
                                df_mto_ones_reg = df_mto_reg.drop_duplicates('origin_file_name')
                                total_num = len(df_mto_ones_reg)

                        if not self.main_window.cb_more_then_two.isChecked():
                            if self.main_window.cb_at_cash_register.isChecked():
                                slice_df_reg = slice_df[slice_df['face_zone'] == 1]
                                df_ones_reg = slice_df_reg.drop_duplicates('origin_file_name')
                                total_num = len(df_ones_reg)

                    else:
                        df_ones = slice_df.drop_duplicates('origin_file_name')
                        total_num = len(df_ones)

                        if self.main_window.cb_more_then_two.isChecked():
                            df_mto = slice_df[slice_df.duplicated(subset='origin_file_name', keep=False)]
                            df_mto_ones = df_mto.drop_duplicates('origin_file_name')
                            total_num = len(df_mto_ones)
                            if self.main_window.cb_at_cash_register.isChecked():
                                df_mto_reg = df_mto[df_mto['face_zone'] == 1]
                                df_mto_ones_reg = df_mto_reg.drop_duplicates('origin_file_name')
                                total_num = len(df_mto_ones_reg)

                        if not self.main_window.cb_more_then_two.isChecked():
                            if self.main_window.cb_at_cash_register.isChecked():
                                slice_df_reg = slice_df[slice_df['face_zone'] == 1]
                                df_ones_reg = slice_df_reg.drop_duplicates('origin_file_name')
                                total_num = len(df_ones_reg)

                    if self.main_window.cb_certain_zone.isChecked():
                        zone_coords = self.main_window.le_certain_zone.text()
                        slice_df_cert = zone_intersections(slice_df, zone_coords)
                        df_ones_cert = slice_df_cert.drop_duplicates('origin_file_name')
                        total_num = len(df_ones_cert)

                    self.total_num_message.emit(str(total_num))
                    self.enable_disable_ui.emit(True)
        self.finished.emit()


class ParseThread(QThread):
    finished = pyqtSignal()
    total_num_message = pyqtSignal(str)
    output_message = pyqtSignal(str)
    enable_disable_ui = pyqtSignal(bool)
    progress_bar_start = pyqtSignal(int)
    progress_bar_process = pyqtSignal(int)

    def __init__(self, main_window, parent=None):
        super(ParseThread, self).__init__(parent)
        self.main_window = main_window

    def run(self):
        def dt_slice_shape_df(df_cam, dt_start, dt_end):
            df = df_cam.copy()
            dt_end_full = str(int(dt_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]

        def get_coords_from_text(coords):
            if len(coords.split(',')) == 4:
                # Single zone coords
                dirty_list = coords[1:-1].split(',')
                ymin = int(dirty_list[0])
                ymax = int(dirty_list[1][1:])
                xmin = int(dirty_list[2][1:])
                xmax = int(dirty_list[3][1:])
                return ymin, ymax, xmin, xmax

            if len(coords.split(',')) == 8:
                # Double zone coords
                l0 = coords.split(')')[0][2:].split(',')
                t0 = tuple(np.array(l0, dtype='int'))
                l1 = coords.split(')')[1][3:].split(',')
                t1 = tuple(np.array(l1, dtype='int'))
                return [t0, t1]

            if len(coords.split(',')) == 12:
                # Triple zone coords
                l0 = coords.split(')')[0][2:].split(',')
                t0 = tuple(np.array(l0, dtype='int'))
                l1 = coords.split(')')[1][3:].split(',')
                t1 = tuple(np.array(l1, dtype='int'))
                l2 = coords.split(')')[2][3:].split(',')
                t2 = tuple(np.array(l2, dtype='int'))
                return [t0, t1, t2]

        def rectangle_on_shape(img, shape_location):
            y1, y2, x1, x2 = shape_location
            draw = ImageDraw.Draw(img)
            return draw.rectangle(((x1, y1), (x2, y2)), outline='#ffff14', width=3)

        def show_zone(img, zone_coords):
            if len(zone_coords) == 4:
                y1, y2, x1, x2 = zone_coords
                draw = ImageDraw.Draw(img)
                draw.rectangle(((x1, y1), (x2, y2)), outline='#01ff07', width=2)
            if len(zone_coords) == 3:
                coords_set = zone_coords
                for coords in coords_set:
                    y1, y2, x1, x2 = coords
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(((x1, y1), (x2, y2)), outline='#01ff07', width=2)
            if len(zone_coords) == 2:
                coords_set = zone_coords
                for coords in coords_set:
                    y1, y2, x1, x2 = coords
                    draw = ImageDraw.Draw(img)
                    draw.rectangle(((x1, y1), (x2, y2)), outline='#01ff07', width=2)

        def zone_intersections(df, zone_coords):
            df = df.copy()
            df['alarm_intersection'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), zone_coords))
            return df[df['alarm_intersection'] == 1].iloc[:, 0:-1]

        def detection_zone_intersection(shape_location, zone_coords):
            if len(str(zone_coords).split(',')) == 4:
                # Single_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                if type(zone_coords) == tuple:
                    y1, y2, x1, x2 = zone_coords
                else:
                    y1, y2, x1, x2 = get_coords_from_text(zone_coords)

                dx = min(xmax, x2) - max(xmin, x1)
                dy = min(ymax, y2) - max(ymin, y1)

                if (dx >= 0) and (dy >= 0):
                    return 1
                else:
                    return 0

            if len(str(zone_coords).split(',')) == 8:
                # Double_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
                y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]

                dx0 = min(xmax, x02) - max(xmin, x01)
                dy0 = min(ymax, y02) - max(ymin, y01)
                dx1 = min(xmax, x12) - max(xmin, x11)
                dy1 = min(ymax, y12) - max(ymin, y11)

                if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)):
                    return 1
                else:
                    return 0

            if len(str(zone_coords).split(',')) == 12:
                # Triple_zone_intersection
                ymin, ymax, xmin, xmax = shape_location

                y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
                y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]
                y21, y22, x21, x22 = get_coords_from_text(zone_coords)[2]

                dx0 = min(xmax, x02) - max(xmin, x01)
                dy0 = min(ymax, y02) - max(ymin, y01)
                dx1 = min(xmax, x12) - max(xmin, x11)
                dy1 = min(ymax, y12) - max(ymin, y11)
                dx2 = min(xmax, x22) - max(xmin, x21)
                dy2 = min(ymax, y22) - max(ymin, y21)

                if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)) | ((dx2 >= 0) and (dy2 >= 0)):
                    return 1
                else:
                    return 0

        def get_rectangled_images(df_dt, rectangle_status, shape_zone_status, face_zone_status):
            df = df_dt.copy()
            df_ones = df.drop_duplicates('origin_file_name')
            df_mto = df[df.duplicated(subset='origin_file_name', keep=False)]
            self.progress_bar_start.emit(len(df_ones))
            for i, row in df_ones.iterrows():
                if row['origin_file_name'] in df_mto['origin_file_name'].values:
                    one_frame_shapes = df_mto[df_mto['origin_file_name'] == row['origin_file_name']]
                    images_path = ip_cam_data_paths_dict[cam_name]
                    image_name = row['origin_file_name']
                    day = '20' + image_name[:6]
                    try:
                        img = Image.open(os.path.join(images_path, day, image_name))
                        if rectangle_status:
                            for ii, rrow in one_frame_shapes.iterrows():
                                rectangle_on_shape(img, get_coords_from_text(rrow['shape_location']))
                        if shape_zone_status:
                            zone_coords = rrow['shape_zone_coords']
                            if self.main_window.cb_certain_zone.isChecked():
                                zone_coords = self.main_window.le_certain_zone.text()
                            for ii, rrow in one_frame_shapes.iterrows():
                                show_zone(img, get_coords_from_text(zone_coords))
                        if face_zone_status:
                            for ii, rrow in one_frame_shapes.iterrows():
                                show_zone(img, get_coords_from_text(rrow['face_zone_coords']))
                        img.save(os.path.join(os.getcwd(), r'imgs_cvdb', image_name), 'JPEG')
                    except:
                        print('Problem with: ', image_name, cam_name)
                        continue
                else:
                    images_path = ip_cam_data_paths_dict[cam_name]
                    image_name = row['origin_file_name']
                    day = '20' + image_name[:6]
                    try:
                        img = Image.open(os.path.join(images_path, day, image_name))
                        if rectangle_status:
                            rectangle_on_shape(img, get_coords_from_text(row['shape_location']))
                        if shape_zone_status:
                            zone_coords = row['shape_zone_coords']
                            if self.main_window.cb_certain_zone.isChecked():
                                zone_coords = self.main_window.le_certain_zone.text()
                            show_zone(img, get_coords_from_text(zone_coords))
                        if face_zone_status:
                            show_zone(img, get_coords_from_text(row['face_zone_coords']))
                        img.save(os.path.join(os.getcwd(), r'imgs_cvdb', image_name), 'JPEG')
                    except:
                        print('Problem with: ', image_name, cam_name)
                        continue
                count_progress = self.main_window.progressBar.value() + 1
                self.progress_bar_process.emit(count_progress)

        ip_cam_data_paths_dict = self.main_window.ip_cam_data_paths_dict
        cam_names = self.main_window.cam_names
        cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.date_start
        date_end = self.main_window.date_end
        text_wait = self.main_window.text_wait
        text_done = self.main_window.text_done

        if cam_name not in cam_names:
            self.total_num_message.emit(self.main_window.text_error)
            self.output_message.emit(self.main_window.text_error_cam)
        else:
            if (len(date_start) & len(date_end)) == 0:
                self.output_message.emit(self.main_window.text_error_date)
            else:
                first_photo_day = os.listdir(ip_cam_data_paths_dict[cam_name])[0]
                last_photo_day = os.listdir(ip_cam_data_paths_dict[cam_name])[-1]
                range_day_start = '20' + date_start[:6]
                range_day_end = '20' + date_end[:6]

                if not (range_day_start >= first_photo_day) & (last_photo_day >= range_day_end):
                    self.total_num_message.emit(self.main_window.text_error)
                    self.output_message.emit(self.main_window.text_error_bad_range)
                else:
                    self.enable_disable_ui.emit(False)
                    self.main_window.pb_choose_cam.setEnabled(False)
                    self.main_window.le_cam_name.setEnabled(False)

                    # self.output_message.emit(text_wait)

                    df_cam = pd.DataFrame()
                    if os.path.exists(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv')):
                        df_cam = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'))

                    total_df = dt_slice_shape_df(df_cam, date_start, date_end)

                    if self.main_window.cb_general_det_aria.isChecked():
                        total_df = total_df[total_df['shape_zone'] == 1]

                        if self.main_window.cb_more_then_two.isChecked():
                            total_df = total_df[total_df.duplicated(subset='origin_file_name', keep=False)]
                            if self.main_window.cb_at_cash_register.isChecked():
                                total_df = total_df[total_df['face_zone'] == 1]

                        if not self.main_window.cb_more_then_two.isChecked():
                            if self.main_window.cb_at_cash_register.isChecked():
                                total_df = total_df[total_df['face_zone'] == 1]
                    else:
                        if self.main_window.cb_more_then_two.isChecked():
                            total_df = total_df[total_df.duplicated(subset='origin_file_name', keep=False)]
                            if self.main_window.cb_at_cash_register.isChecked():
                                total_df = total_df[total_df['face_zone'] == 1]

                        if not self.main_window.cb_more_then_two.isChecked():
                            if self.main_window.cb_at_cash_register.isChecked():
                                total_df = total_df[total_df['face_zone'] == 1]

                    if self.main_window.cb_certain_zone.isChecked():
                        zone_coords = self.main_window.le_certain_zone.text()
                        total_df = zone_intersections(total_df, zone_coords)

                    if os.path.exists(os.path.join(os.getcwd(), r'imgs_cvdb')):
                        shutil.rmtree(os.path.join(os.getcwd(), r'imgs_cvdb'))
                        os.mkdir(os.path.join(os.getcwd(), r'imgs_cvdb'))
                    else:
                        os.mkdir(os.path.join(os.getcwd(), r'imgs_cvdb'))

                    rectangle_status = self.main_window.cb_shape_bbox.isChecked()
                    shape_zone_status = self.main_window.cb_shape_zone.isChecked()
                    face_zone_status = self.main_window.cb_face_zone.isChecked()
                    get_rectangled_images(total_df, rectangle_status, shape_zone_status, face_zone_status)
                    # self.output_message.emit(text_done)
                    self.main_window.pb_choose_cam.setEnabled(True)
                    self.main_window.le_cam_name.setEnabled(True)
                    self.enable_disable_ui.emit(True)
        self.finished.emit()


class UI(QDialog):
    def __init__(self):
        super(UI, self).__init__()
        self.worker = None
        self.thread = None
        self.worker_2 = None
        self.thread_2 = None
        self.ShowCams = None
        self.Showlast10days = None
        self.SetZoneWindow = None

        # Loading the user interface
        # If you use UI code, activate it
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # If you use UI file, activate it
        #uic.loadUi(os.path.join(os.getcwd(), 'CVdbViewer_v2_GUI.ui'), self)

        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)

        self.pb_choose_cam = self.findChild(QPushButton, 'pb_choose_cam')
        self.le_cam_name = self.findChild(QLineEdit, 'le_cam_name')
        self.le_date_start = self.findChild(QLineEdit, 'le_date_start')
        self.le_date_end = self.findChild(QLineEdit, 'le_date_end')
        self.pb_last_10_days_1 = self.findChild(QPushButton, 'pb_last_10_days_1')
        self.pb_last_10_days_2 = self.findChild(QPushButton, 'pb_last_10_days_2')

        self.cb_general_det_aria = self.findChild(QCheckBox, 'cb_general_det_aria')
        self.cb_more_then_two = self.findChild(QCheckBox, 'cb_more_then_two')
        self.cb_at_cash_register = self.findChild(QCheckBox, 'cb_at_cash_register')
        self.cb_certain_zone = self.findChild(QCheckBox, 'cb_certain_zone')
        self.le_certain_zone = self.findChild(QLineEdit, 'le_certain_zone')
        self.pb_set_certain_zone = self.findChild(QPushButton, 'pb_set_certain_zone')
        self.cb_shape_bbox = self.findChild(QCheckBox, 'cb_shape_bbox')
        self.cb_shape_zone = self.findChild(QCheckBox, 'cb_shape_zone')
        self.cb_face_zone = self.findChild(QCheckBox, 'cb_face_zone')

        self.pb_estimate = self.findChild(QPushButton, 'pb_estimate')
        self.label_total = self.findChild(QLabel, 'label_total')
        self.pb_show_in_fold = self.findChild(QPushButton, 'pb_show_in_fold')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')

        self.label_out = self.findChild(QLabel, 'label_out')
        self.label_wishes_thanks = self.findChild(QLabel, 'label_wishes_thanks')

        self.pb_wishes = self.findChild(QPushButton, 'pb_wishes')
        self.pb_thanks = self.findChild(QPushButton, 'pb_thanks')

        # Variables initialization
        self.date_start = ''
        self.date_end = ''
        self.text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
        self.text_error = '<FONT COLOR=#f4320c>Ошибка</FONT>'
        self.text_data_error = '<FONT COLOR=#f4320c>' \
                               'Проверьте имеются ли данные для выбранной камеры (фото, база)</FONT>'
        self.text_error_date = '<FONT COLOR=#f4320c>Задайте промежуток времени</FONT>'
        self.text_error_cam = '<FONT COLOR=#f4320c>Фотографий для этой камеры нет</FONT>'
        self.text_error_bad_range = '<FONT COLOR=#f4320c>Фотографий для этого промежутка времени нет</FONT>'
        self.text_done = '<FONT COLOR=#008000>Выполнено!</FONT>'

        # Connecting button signals to their slots (functions)
        self.pb_choose_cam.clicked.connect(self.pb_choose_cam_clicked)
        self.pb_last_10_days_1.clicked.connect(self.pb_last_10_days_1_clicked)
        self.pb_last_10_days_2.clicked.connect(self.pb_last_10_days_2_clicked)

        self.cb_general_det_aria.clicked.connect(self.exceptional_choice_clicked)
        self.cb_more_then_two.clicked.connect(self.exceptional_choice_clicked)
        self.cb_at_cash_register.clicked.connect(self.exceptional_choice_clicked)
        self.cb_certain_zone.clicked.connect(self.exceptional_choice_clicked)
        self.pb_set_certain_zone.clicked.connect(self.pb_set_certain_zone_clicked)

        self.pb_estimate.clicked.connect(self.pb_estimate_clicked)
        self.pb_show_in_fold.clicked.connect(self.pb_show_in_fold_clicked)

        self.pb_wishes.clicked.connect(self.button_wishes_clicked)
        self.pb_thanks.clicked.connect(self.button_thanks_clicked)

        self.ip_cam_data_paths_dict, self.cam_names = self.initializer()
        self.disable_enable_ui(False)
        self.show()

    def initializer(self):
        def data_condition(item):
            return (len(str(item).split('_')) > 1) & (str(item).split('_')[-1] in ['images', 'photos'])

        media_path = os.path.join(os.getcwd(), 'cams_media')
        ip_cam_data_folders = [item for item in os.listdir(media_path) if data_condition(item)]
        ip_cam_data_folders = sorted(ip_cam_data_folders, reverse=True)
        ip_cam_data_paths = [os.path.join(media_path, item) for item in ip_cam_data_folders]
        cam_names = ['_'.join(str(item).split('_')[:-1]) for item in ip_cam_data_folders]
        ip_cam_data_paths_dict = dict(zip(cam_names, ip_cam_data_paths))
        return ip_cam_data_paths_dict, cam_names

    def pb_choose_cam_clicked(self):
        self.le_date_start.setText('')
        self.le_date_end.setText('')
        self.le_certain_zone.setText('')
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.ShowCams = ShowCams(main_window=self)
        self.ShowCams.show()

    def pb_last_10_days_1_clicked(self):
        try:
            self.Showlast10days = Showlast10days('start', main_window=self)
            self.Showlast10days.show()
        except:
            self.label_out.setText(self.text_data_error)

    def pb_last_10_days_2_clicked(self):
        try:
            self.Showlast10days = Showlast10days('end', main_window=self)
            self.Showlast10days.show()
            self.disable_enable_ui(True)
        except:
            self.label_out.setText(self.text_data_error)

    def exceptional_choice_clicked(self):
        if self.cb_certain_zone.isChecked():
            self.cb_general_det_aria.setCheckState(False)
            self.cb_more_then_two.setCheckState(False)
            self.cb_at_cash_register.setCheckState(False)

        if self.cb_general_det_aria.isChecked() | self.cb_more_then_two.isChecked() | self.cb_at_cash_register.isChecked():
            self.cb_certain_zone.setCheckState(False)

    def pb_set_certain_zone_clicked(self):
        #try:
            self.SetZoneWindow = SetZoneWindow(main_window=self)
            self.SetZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        #except:
            #self.label_out.setText(self.text_data_error)

    def sending_total_num_message(self, text_total):
        text_total = f'<FONT COLOR=#008000>{text_total}</FONT>'
        self.label_total.setText(text_total)
        self.label_wishes_thanks.setText(' ')

    def run_EstimateThread(self):
        # Step 1: Create a QThread object
        self.thread = QThread()
        # Step 2: Create a worker object
        self.worker = EstimateThread(main_window=self)
        # Step 3: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 4: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.enable_disable_ui.connect(self.disable_enable_ui)
        self.worker.output_message.connect(self.sending_output_message)
        self.worker.total_num_message.connect(self.sending_total_num_message)
        # Step 5: Start the thread
        self.thread.start()

    def pb_estimate_clicked(self):
        self.date_start = self.le_date_start.text()
        self.date_end = self.le_date_end.text()
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.progressBar.setValue(0)
        self.run_EstimateThread()

    def disable_enable_ui(self, signal):
        self.le_date_start.setEnabled(signal)
        self.le_date_end.setEnabled(signal)
        self.pb_last_10_days_1.setEnabled(signal)
        self.pb_last_10_days_2.setEnabled(signal)
        self.cb_general_det_aria.setEnabled(signal)
        self.cb_more_then_two.setEnabled(signal)
        self.cb_at_cash_register.setEnabled(signal)
        self.cb_certain_zone.setEnabled(signal)
        self.le_certain_zone.setEnabled(signal)
        self.pb_set_certain_zone.setEnabled(signal)
        self.cb_shape_bbox.setEnabled(signal)
        self.cb_shape_zone.setEnabled(signal)
        self.cb_face_zone.setEnabled(signal)
        self.pb_estimate.setEnabled(signal)
        self.pb_show_in_fold.setEnabled(signal)

    def sending_output_message(self, message):
        self.label_out.setText(message)
        self.label_wishes_thanks.setText(' ')

    def set_progress_bar_start(self, progress_days_max):
        self.progressBar.setMaximum(progress_days_max)
        self.progressBar.setValue(0)

    def set_progress_bar_process(self, value_videos):
        self.progressBar.setValue(value_videos)

    def run_ParseThread(self):
        self.thread_2 = QThread()
        self.worker_2 = ParseThread(main_window=self)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.enable_disable_ui.connect(self.disable_enable_ui)
        self.worker_2.progress_bar_start.connect(self.set_progress_bar_start)
        self.worker_2.progress_bar_process.connect(self.set_progress_bar_process)
        self.worker_2.total_num_message.connect(self.sending_total_num_message)
        self.worker_2.output_message.connect(self.sending_output_message)
        self.thread_2.start()

    def pb_show_in_fold_clicked(self):
        self.date_start = self.le_date_start.text()
        self.date_end = self.le_date_end.text()
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.run_ParseThread()

        # Feedback button

    def button_wishes_clicked(self):
        email = '<FONT COLOR=#b96902>videonabexp@gmail.com</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)

        # Button for donations

    def button_thanks_clicked(self):
        tel = '<FONT COLOR=#b96902>5469 5400 2720 6935</FONT>'
        self.label_wishes_thanks.setText('Благодарность на карту Сбербанк: ' + tel + ' Алексей')


def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

if __name__ == '__main__':
    main()



