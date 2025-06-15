import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from funcs_initializer_camconfig_getcamframe import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(621, 841)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 581, 801))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
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
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_last_10_days_2.setFont(font)
        self.pb_last_10_days_2.setObjectName("pb_last_10_days_2")
        self.gridLayout.addWidget(self.pb_last_10_days_2, 16, 4, 1, 1)
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
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.pb_show_camconfig = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_show_camconfig.setEnabled(True)
        self.pb_show_camconfig.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_show_camconfig.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_show_camconfig.setFont(font)
        self.pb_show_camconfig.setObjectName("pb_show_camconfig")
        self.gridLayout.addWidget(self.pb_show_camconfig, 4, 2, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 5)
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
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 5)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_8.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 25, 0, 1, 2)
        self.le_hour_end = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_hour_end.setFont(font)
        self.le_hour_end.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_hour_end.setInputMask("")
        self.le_hour_end.setText("")
        self.le_hour_end.setObjectName("le_hour_end")
        self.gridLayout.addWidget(self.le_hour_end, 7, 3, 1, 1)
        self.pb_show_shape_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_show_shape_zone.setEnabled(True)
        self.pb_show_shape_zone.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_show_shape_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_show_shape_zone.setFont(font)
        self.pb_show_shape_zone.setObjectName("pb_show_shape_zone")
        self.gridLayout.addWidget(self.pb_show_shape_zone, 19, 2, 1, 3)
        self.le_cam_name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_cam_name.setFont(font)
        self.le_cam_name.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_cam_name.setInputMask("")
        self.le_cam_name.setText("")
        self.le_cam_name.setObjectName("le_cam_name")
        self.gridLayout.addWidget(self.le_cam_name, 4, 1, 1, 1)
        self.pb_hours_save = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_hours_save.setEnabled(True)
        self.pb_hours_save.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_hours_save.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_hours_save.setFont(font)
        self.pb_hours_save.setObjectName("pb_hours_save")
        self.gridLayout.addWidget(self.pb_hours_save, 7, 4, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_12.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 17, 0, 1, 5)
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
        self.gridLayout.addWidget(self.label_4, 10, 0, 1, 5)
        self.pb_show_register_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_show_register_zone.setEnabled(True)
        self.pb_show_register_zone.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_show_register_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_show_register_zone.setFont(font)
        self.pb_show_register_zone.setObjectName("pb_show_register_zone")
        self.gridLayout.addWidget(self.pb_show_register_zone, 25, 2, 1, 3)
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
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 5)
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
        self.gridLayout.addWidget(self.pb_thanks, 30, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 18, 0, 1, 5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 24, 0, 1, 5)
        self.le_hour_start = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_hour_start.setFont(font)
        self.le_hour_start.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_hour_start.setInputMask("")
        self.le_hour_start.setText("")
        self.le_hour_start.setObjectName("le_hour_start")
        self.gridLayout.addWidget(self.le_hour_start, 7, 1, 1, 1)
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
        self.gridLayout.addWidget(self.label_wishes_thanks, 29, 0, 1, 5)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 5)
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
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 5)
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
        self.gridLayout.addWidget(self.label_7, 19, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_10.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 7, 2, 1, 1)
        self.le_date_start = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_date_start.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_date_start.setFont(font)
        self.le_date_start.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_date_start.setText("")
        self.le_date_start.setMaxLength(12)
        self.le_date_start.setObjectName("le_date_start")
        self.gridLayout.addWidget(self.le_date_start, 13, 2, 1, 2)
        self.label_14 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_14.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 20, 0, 1, 1)
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
        self.gridLayout.addWidget(self.label_5, 13, 0, 1, 2)
        self.le_date_end = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_date_end.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_date_end.setFont(font)
        self.le_date_end.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_date_end.setText("")
        self.le_date_end.setMaxLength(12)
        self.le_date_end.setObjectName("le_date_end")
        self.gridLayout.addWidget(self.le_date_end, 16, 2, 1, 2)
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
        self.gridLayout.addWidget(self.label_out, 28, 0, 1, 5)
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
        self.gridLayout.addWidget(self.pb_wishes, 30, 0, 1, 4)
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
        self.gridLayout.addWidget(self.label_6, 16, 0, 1, 2)
        self.le_shape_zone_1 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_shape_zone_1.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_shape_zone_1.setFont(font)
        self.le_shape_zone_1.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_shape_zone_1.setText("")
        self.le_shape_zone_1.setObjectName("le_shape_zone_1")
        self.gridLayout.addWidget(self.le_shape_zone_1, 20, 1, 1, 3)
        self.label_16 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_16.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 22, 0, 1, 1)
        self.pb_set_shape_zone_1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_set_shape_zone_1.setEnabled(True)
        self.pb_set_shape_zone_1.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_set_shape_zone_1.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_set_shape_zone_1.setFont(font)
        self.pb_set_shape_zone_1.setObjectName("pb_set_shape_zone_1")
        self.gridLayout.addWidget(self.pb_set_shape_zone_1, 20, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_15.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 21, 0, 1, 1)
        self.pb_set_shape_zone_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_set_shape_zone_2.setEnabled(True)
        self.pb_set_shape_zone_2.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_set_shape_zone_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_set_shape_zone_2.setFont(font)
        self.pb_set_shape_zone_2.setObjectName("pb_set_shape_zone_2")
        self.gridLayout.addWidget(self.pb_set_shape_zone_2, 21, 4, 1, 1)
        self.le_shape_zone_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_shape_zone_3.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_shape_zone_3.setFont(font)
        self.le_shape_zone_3.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_shape_zone_3.setText("")
        self.le_shape_zone_3.setObjectName("le_shape_zone_3")
        self.gridLayout.addWidget(self.le_shape_zone_3, 22, 1, 1, 3)
        self.le_shape_zone_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_shape_zone_2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_shape_zone_2.setFont(font)
        self.le_shape_zone_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_shape_zone_2.setText("")
        self.le_shape_zone_2.setObjectName("le_shape_zone_2")
        self.gridLayout.addWidget(self.le_shape_zone_2, 21, 1, 1, 3)
        self.pb_save_register_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_save_register_zone.setEnabled(True)
        self.pb_save_register_zone.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_save_register_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_save_register_zone.setFont(font)
        self.pb_save_register_zone.setObjectName("pb_save_register_zone")
        self.gridLayout.addWidget(self.pb_save_register_zone, 27, 2, 1, 3)
        self.pb_set_register_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_set_register_zone.setEnabled(True)
        self.pb_set_register_zone.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_set_register_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_set_register_zone.setFont(font)
        self.pb_set_register_zone.setObjectName("pb_set_register_zone")
        self.gridLayout.addWidget(self.pb_set_register_zone, 26, 4, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_18.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 23, 0, 1, 2)
        self.le_register_zone = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.le_register_zone.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.le_register_zone.setFont(font)
        self.le_register_zone.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.le_register_zone.setText("")
        self.le_register_zone.setObjectName("le_register_zone")
        self.gridLayout.addWidget(self.le_register_zone, 26, 1, 1, 3)
        self.pb_save_shape_zone = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_save_shape_zone.setEnabled(True)
        self.pb_save_shape_zone.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_save_shape_zone.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_save_shape_zone.setFont(font)
        self.pb_save_shape_zone.setObjectName("pb_save_shape_zone")
        self.gridLayout.addWidget(self.pb_save_shape_zone, 23, 2, 1, 3)
        self.pb_set_shape_zone_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_set_shape_zone_3.setEnabled(True)
        self.pb_set_shape_zone_3.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_set_shape_zone_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_set_shape_zone_3.setFont(font)
        self.pb_set_shape_zone_3.setObjectName("pb_set_shape_zone_3")
        self.gridLayout.addWidget(self.pb_set_shape_zone_3, 22, 4, 1, 1)
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
        self.label_19 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_19.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 26, 0, 1, 1)
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
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_last_10_days_1.setFont(font)
        self.pb_last_10_days_1.setObjectName("pb_last_10_days_1")
        self.gridLayout.addWidget(self.pb_last_10_days_1, 13, 4, 1, 1)
        self.label_wishes_thanks.setBuddy(self.pb_wishes)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.le_cam_name, self.pb_show_camconfig)
        Dialog.setTabOrder(self.pb_show_camconfig, self.le_hour_start)
        Dialog.setTabOrder(self.le_hour_start, self.le_hour_end)
        Dialog.setTabOrder(self.le_hour_end, self.pb_hours_save)
        Dialog.setTabOrder(self.pb_hours_save, self.le_date_start)
        Dialog.setTabOrder(self.le_date_start, self.le_date_end)
        Dialog.setTabOrder(self.le_date_end, self.pb_show_shape_zone)
        Dialog.setTabOrder(self.pb_show_shape_zone, self.le_shape_zone_1)
        Dialog.setTabOrder(self.le_shape_zone_1, self.pb_set_shape_zone_1)
        Dialog.setTabOrder(self.pb_set_shape_zone_1, self.le_shape_zone_2)
        Dialog.setTabOrder(self.le_shape_zone_2, self.pb_set_shape_zone_2)
        Dialog.setTabOrder(self.pb_set_shape_zone_2, self.le_shape_zone_3)
        Dialog.setTabOrder(self.le_shape_zone_3, self.pb_set_shape_zone_3)
        Dialog.setTabOrder(self.pb_set_shape_zone_3, self.pb_save_shape_zone)
        Dialog.setTabOrder(self.pb_save_shape_zone, self.pb_show_register_zone)
        Dialog.setTabOrder(self.pb_show_register_zone, self.le_register_zone)
        Dialog.setTabOrder(self.le_register_zone, self.pb_set_register_zone)
        Dialog.setTabOrder(self.pb_set_register_zone, self.pb_save_register_zone)
        Dialog.setTabOrder(self.pb_save_register_zone, self.pb_wishes)
        Dialog.setTabOrder(self.pb_wishes, self.pb_thanks)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CVsetCam"))
        self.pb_last_10_days_2.setText(_translate("Dialog", "посл 10дн"))
        self.label_9.setText(_translate("Dialog", "Часы работы с"))
        self.pb_show_camconfig.setText(_translate("Dialog", "Показать сохраненные часы"))
        self.label_1.setText(_translate("Dialog", "Программа для настройки часов работы "))
        self.label_8.setText(_translate("Dialog", "Зона детекции у кассы:"))
        self.pb_show_shape_zone.setText(_translate("Dialog", "Показать сохраненную зону"))
        self.pb_hours_save.setText(_translate("Dialog", "Сохранить"))
        self.label_12.setText(_translate("Dialog", "промежуток времени для пересчета базы силуэтов в прошлом, если пусто, то в будущем"))
        self.label_4.setText(_translate("Dialog", "Промежуток времени для зон детекции (ггммддччмм):"))
        self.pb_show_register_zone.setText(_translate("Dialog", "Показать сохраненную зону"))
        self.label_3.setText(_translate("Dialog", "работает в корневой папке системы с базой данных CV и базой фотографий"))
        self.pb_thanks.setText(_translate("Dialog", "Спасибо!"))
        self.label_2.setText(_translate("Dialog", "и зон детекции торговой точки"))
        self.label_7.setText(_translate("Dialog", "Общая зона детекции:"))
        self.label_10.setText(_translate("Dialog", "до"))
        self.label_14.setText(_translate("Dialog", "y1 y2 x1 x2 обл 1"))
        self.label_5.setText(_translate("Dialog", "Нижняя граница (вкл): [ 231121 -"))
        self.pb_wishes.setText(_translate("Dialog", "Пожелания"))
        self.label_6.setText(_translate("Dialog", "Верхняя граница (вкл): - 240101 ]"))
        self.label_16.setText(_translate("Dialog", "если нужно обл 3"))
        self.pb_set_shape_zone_1.setText(_translate("Dialog", "задать"))
        self.label_15.setText(_translate("Dialog", "если нужно обл 2"))
        self.pb_set_shape_zone_2.setText(_translate("Dialog", "задать"))
        self.pb_save_register_zone.setText(_translate("Dialog", "Сохранить"))
        self.pb_set_register_zone.setText(_translate("Dialog", "задать"))
        self.label_18.setText(_translate("Dialog", "прямоугольник с левого верха до правого низа"))
        self.pb_save_shape_zone.setText(_translate("Dialog", "Сохранить"))
        self.pb_set_shape_zone_3.setText(_translate("Dialog", "задать"))
        self.pb_choose_cam.setText(_translate("Dialog", "Камера"))
        self.label_19.setText(_translate("Dialog", "y1 y2 x1 x2"))
        self.pb_last_10_days_1.setText(_translate("Dialog", "посл 10дн"))


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
        self.main_window.disable_enable_ui(True)


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


class ShowZoneWindow(QtWidgets.QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(ShowZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()

        self.setWindowTitle('Сохраненная зона детекции')
        self.image = QLabel()

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.image)

        camconfig = load_camconfig()
        imgs_path = self.main_window.ip_cam_data_paths_dict[self.cam_name]
        if (len(date_start) & len(date_end)) == 0:
            last_day = os.listdir(imgs_path)[-1]
            last_img = os.listdir(os.path.join(imgs_path, last_day))[0]
            img_path = os.path.join(imgs_path, last_day, last_img)
            self.coords = [cam_set[self.direction] for cam_set in camconfig if cam_set['cam_name'] == self.cam_name][0]
            self.coords = self.get_coords_from_text(str(self.coords))
        else:
            first_range_day = '20' + date_start[:6]
            images = os.listdir(os.path.join(imgs_path, first_range_day))
            first_range_img = [img for img in images if img[:len(date_start)] == date_start][0]
            img_path = os.path.join(imgs_path, first_range_day, first_range_img)
            df_cam = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{self.cam_name}_shapes_locs.csv'))
            df_cam_slice = self.dt_slice_shape_df(df_cam, date_start, date_end)
            if self.direction == 'shape_zone':
                self.coords = df_cam_slice.iloc[0]['shape_zone_coords']
            else:
                self.coords = df_cam_slice.iloc[0]['face_zone_coords']
            self.coords = self.get_coords_from_text(str(self.coords))

        self.pixmap = QPixmap(img_path)
        self.pixmap_small = self.pixmap.scaled(int(self.pixmap.width() / 1.5), int(self.pixmap.height() / 1.5))
        self.setGeometry(320, 200, 0, 0)
        self.setMinimumSize(int(self.pixmap_small.width()), int(self.pixmap_small.height()))

        self.setCoordsToEditLines()

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

    def dt_slice_shape_df(self, df_cam, dt_start, dt_end):
        df = df_cam.copy()
        dt_end_full = str(int(dt_end) + 1)
        df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
        return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.green, 2)
        painter.setPen(pen)
        br = QtGui.QBrush(QtGui.QColor(200, 10, 10, 40))
        painter.setBrush(br)
        painter.drawPixmap(QPoint(), self.pixmap_small)

        if len(self.coords) == 4:
            y1, y2, x1, x2 = self.coords
            y1, y2, x1, x2 = int(y1 / 1.5), int(y2 / 1.5), int(x1 / 1.5), int(x2 / 1.5)
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        if len(self.coords) == 3:
            coords_set = self.coords
            for coords in coords_set:
                y1, y2, x1, x2 = coords
                y1, y2, x1, x2 = int(y1 / 1.5), int(y2 / 1.5), int(x1 / 1.5), int(x2 / 1.5)
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)
        if len(self.coords) == 2:
            coords_set = self.coords
            for coords in coords_set:
                y1, y2, x1, x2 = coords
                y1, y2, x1, x2 = int(y1 / 1.5), int(y2 / 1.5), int(x1 / 1.5), int(x2 / 1.5)
                painter.drawRect(x1, y1, x2 - x1, y2 - y1)

    def setCoordsToEditLines(self):
        if self.direction == 'shape_zone':
            if len(self.coords) == 4:
                self.main_window.le_shape_zone_1.setText(str(self.coords))
            if len(self.coords) == 3:
                coords_set = self.coords
                self.main_window.le_shape_zone_1.setText(str(coords_set[0]))
                self.main_window.le_shape_zone_2.setText(str(coords_set[1]))
                self.main_window.le_shape_zone_3.setText(str(coords_set[2]))
            if len(self.coords) == 2:
                coords_set = self.coords
                self.main_window.le_shape_zone_1.setText(str(coords_set[0]))
                self.main_window.le_shape_zone_2.setText(str(coords_set[1]))
        if self.direction == 'face_zone':
            self.main_window.le_register_zone.setText(str(self.coords))


class SetZoneWindow(QtWidgets.QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(SetZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()

        self.setWindowTitle('Задать зону детекции')
        self.image = QLabel()

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.image)

        imgs_path = self.main_window.ip_cam_data_paths_dict[self.cam_name]
        if (len(date_start) & len(date_end)) == 0:
            last_day = os.listdir(imgs_path)[-1]
            last_img = os.listdir(os.path.join(imgs_path, last_day))[0]
            img_path = os.path.join(imgs_path, last_day, last_img)
        else:
            first_range_day = '20' + date_start[:6]
            images = os.listdir(os.path.join(imgs_path, first_range_day))
            first_range_img = [img for img in images if img[:len(date_start)] == date_start][0]
            img_path = os.path.join(imgs_path, first_range_day, first_range_img)

        self.pixmap = QPixmap(img_path)
        self.pixmap_small = self.pixmap.scaled(int(self.pixmap.width() / 1.5), int(self.pixmap.height() / 1.5))
        if self.direction in ['shapes_1', 'shapes_2', 'shapes_3']:
            if len(self.main_window.le_shape_zone_1.text()) != 0:
                text_1 = self.main_window.le_shape_zone_1.text()
                self.paint_existing_zone(self.pixmap_small, text_1)
            if len(self.main_window.le_shape_zone_2.text()) != 0:
                text_2 = self.main_window.le_shape_zone_2.text()
                self.paint_existing_zone(self.pixmap_small, text_2)
            if len(self.main_window.le_shape_zone_3.text()) != 0:
                text_3 = self.main_window.le_shape_zone_3.text()
                self.paint_existing_zone(self.pixmap_small, text_3)
        else:
            if len(self.main_window.le_register_zone.text()) != 0:
                text = self.main_window.le_register_zone.text()
                self.paint_existing_zone(self.pixmap_small, text)

        self.setGeometry(320, 200, 0, 0)
        self.setMinimumSize(int(self.pixmap_small.width()), int(self.pixmap_small.height()))

        self.begin, self.destination = QPoint(), QPoint()

        self.directions_dict = {
            'shapes_1': self.main_window.le_shape_zone_1,
            'shapes_2': self.main_window.le_shape_zone_2,
            'shapes_3': self.main_window.le_shape_zone_3,
            'register': self.main_window.le_register_zone
        }

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

    def paint_existing_zone(self, pixmap_small, text):
        coords = self.get_coords_from_text(text)
        y1, y2, x1, x2 = coords
        y1, y2, x1, x2 = int(y1 / 1.5), int(y2 / 1.5), int(x1 / 1.5), int(x2 / 1.5)
        painterInstance = QPainter(pixmap_small)
        pen = QPen(Qt.yellow, 2)
        painterInstance.setPen(pen)
        br = QtGui.QBrush(QtGui.QColor(200, 10, 10, 40))
        painterInstance.setBrush(br)
        painterInstance.drawRect(x1, y1, x2 - x1, y2 - y1)

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
            self.directions_dict[self.direction].setText(str(coords))

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


class SaveRecalculateThread(QThread):
    finished = pyqtSignal()
    output_message = pyqtSignal(str)

    def __init__(self, direction, main_window, parent=None):
        super(SaveRecalculateThread, self).__init__(parent)
        self.main_window = main_window
        self.direction = direction

    def run(self):
        def change_camconfig_shape_zone(cam_name, shape_zone_coords):
            camconfig = load_camconfig()
            [cam_set.update(shape_zone=shape_zone_coords) for cam_set in camconfig if cam_set['cam_name'] == cam_name]
            save_camconfig(camconfig)

        def change_camconfig_face_zone(cam_name, face_zone_coords):
            camconfig = load_camconfig()
            [cam_set.update(face_zone=face_zone_coords) for cam_set in camconfig if cam_set['cam_name'] == cam_name]
            save_camconfig(camconfig)

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

        def change_df_cam_shape_zone(cam_name, shape_zone_coords):
            date_start = self.main_window.le_date_start.text()
            date_end = self.main_window.le_date_end.text()
            df_cam = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'))
            df = df_cam.copy()
            dt_end_full = str(int(date_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'shape_zone'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), shape_zone_coords))
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'shape_zone_coords'] = shape_zone_coords
            df = df.iloc[:, 0:-1]
            df.to_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'), index=False)

        def change_df_cam_face_zone(cam_name, face_zone_coords):
            date_start = self.main_window.le_date_start.text()
            date_end = self.main_window.le_date_end.text()
            df_cam = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'))
            df = df_cam.copy()
            dt_end_full = str(int(date_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'face_zone'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), face_zone_coords))
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'face_zone_coords'] = face_zone_coords
            df = df.iloc[:, 0:-1]
            df.to_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'), index=False)

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

        def set_shape_coords(date_start, date_end):
            coords_list = []
            if len(self.main_window.le_shape_zone_1.text()) != 0:
                coords1 = get_coords_from_text(self.main_window.le_shape_zone_1.text())
                coords_list.append(coords1)
            if len(self.main_window.le_shape_zone_2.text()) != 0:
                coords2 = get_coords_from_text(self.main_window.le_shape_zone_2.text())
                coords_list.append(coords2)
            if len(self.main_window.le_shape_zone_3.text()) != 0:
                coords3 = get_coords_from_text(self.main_window.le_shape_zone_3.text())
                coords_list.append(coords3)
            if len(coords_list) != 0:
                if (len(date_start) & len(date_end)) == 0:
                    if len(coords_list) == 1:
                        change_camconfig_shape_zone(cam_name, str(coords_list[0]))
                    else:
                        change_camconfig_shape_zone(cam_name, str(coords_list))
                else:
                    if len(coords_list) == 1:
                        change_df_cam_shape_zone(cam_name, str(coords_list[0]))
                    else:
                        change_df_cam_shape_zone(cam_name, str(coords_list))

        def set_register_coords(date_start, date_end):
            if len(self.main_window.le_register_zone.text()) != 0:
                coords = self.main_window.le_register_zone.text()
                if (len(date_start) & len(date_end)) == 0:
                    change_camconfig_face_zone(cam_name, coords)
                else:
                    change_df_cam_face_zone(cam_name, coords)

        def base_columns_hours(cam_name):
            camconfig = load_camconfig()
            cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
            hour_start = int(cam_set['work_hours'].split(',')[0][1:])
            hour_end = int(cam_set['work_hours'].split(',')[1][:-1])
            int_hours = np.arange(hour_start, hour_end)
            cols = [str(hour) for hour in int_hours]
            cols.insert(0, 'date')
            cols.append('sum')
            cols.append('s')
            return cols, hour_start, hour_end

        def short_name(name):
            if name[-1].isdigit():
                name = name[:-1]
            return name

        def visitors_counting(cam_name, new_shapes, date, mean_threshold, window_next, step_of_frames=1):
            columns, hour_start, hour_end = base_columns_hours(cam_name)
            if len(new_shapes) != 0:
                new_shapes = new_shapes[new_shapes['cam_name'] == cam_name]
                shapes = new_shapes[new_shapes['shape_zone'] == 1]
                if len(shapes) != 0:
                    column = ['origin_file_name', 'cam_name']
                    shapes = shapes[column].copy()

                    shapes['date'] = shapes['origin_file_name'].apply(lambda x: int(x[0:6])).astype('str')
                    shapes['hour'] = shapes['origin_file_name'].apply(lambda x: int(x[6:8])).astype('str')

                    # Combining people into groups according to their frames and counting them
                    df_mto = shapes[shapes.duplicated(subset='origin_file_name', keep=False)]
                    df_mto_gr = (df_mto[df_mto.duplicated(subset='origin_file_name', keep=False)]
                                 .groupby('origin_file_name')['date'].count())
                    df_mto_gr = pd.DataFrame(df_mto_gr)
                    df_mto_gr.columns = ['people_num']

                    # Connecting group frames with single ones
                    df_ones = shapes.drop_duplicates(
                        subset='origin_file_name').set_index('origin_file_name')
                    df_pc = df_ones.join(df_mto_gr)
                    df_pc = df_pc.fillna(1)
                    df_pc.reset_index(inplace=True)
                    df_pc['people_num'] = df_pc['people_num'].astype('int')

                    # Creating a sample of frames according to the time step
                    if step_of_frames > 1:
                        df_pc = df_pc.copy().iloc[range(0, len(df_pc), step_of_frames)]

                    # Creating a quantitative shift to count the change
                    # in the number of people from frame to frame
                    df_pc['people_lag'] = df_pc['people_num'].shift(1)
                    df_pc = df_pc.fillna(1)
                    df_pc['people_lag'] = df_pc['people_lag'].astype('int')

                    df_pc = df_pc.fillna(1)
                    df_pc['people_diff'] = df_pc['people_num'] - df_pc['people_lag']
                    df_pc.loc[df_pc['people_diff'] < 0, 'people_diff'] = 0

                    def custom_rolling_mean(data, mean_threshold, window_next):
                        window = 1
                        result = []
                        for i in range(len(data)):
                            if i < window:
                                mean = 1
                            else:
                                start = max(i - window, 0)
                                end = i
                                mean = sum(data[start:end]) / (end - start)
                                if mean <= mean_threshold:
                                    window = 1
                                else:
                                    window = window_next
                            result.append(mean)
                        result = result[1:]
                        result.append(1)
                        return result

                    df_pc['people_num_rol'] = custom_rolling_mean(
                        df_pc['people_num'], mean_threshold, window_next)
                    df_pc['people_lag_rol'] = custom_rolling_mean(
                        df_pc['people_lag'], mean_threshold, window_next)

                    df_pc = df_pc.fillna(1)
                    df_pc['people_diff_rol'] = df_pc['people_num_rol'] - df_pc['people_lag_rol']
                    df_pc.loc[df_pc['people_diff_rol'] < 0, 'people_diff_rol'] = 0

                    visitors = pd.pivot_table(
                        df_pc, values='people_diff_rol', index='date',
                        columns='hour', aggfunc='sum', fill_value=0).reset_index()
                    visitors.iloc[:, 1:12] = round(visitors.iloc[:, 1:12])
                    visitors['sum'] = visitors.iloc[:, 1:12].sum(axis=1)
                    visitors['s'] = 'auto'
                    visitors.columns.name = None
                    visitors['date'] = pd.to_datetime(visitors['date'], format='%y%m%d')

                    if len(visitors.columns) < len(columns):
                        visitors = pd.DataFrame(visitors, columns=columns).fillna(0)

                    int_columns = {c: 'int' for c in visitors.columns[1:-1]}
                    visitors = visitors.astype(int_columns)
                    visitors['date'] = visitors['date'].astype('str')

                else:
                    hour_zero_values = np.zeros((1, hour_end - hour_start + 1), dtype=int)
                    visitors = pd.DataFrame(hour_zero_values, columns=columns[1:-1])
                    visitors['date'] = datetime.strptime(date, '%y%m%d')
                    visitors['date'] = visitors['date'].astype('str')
                    visitors['s'] = 'auto'
                    visitors = visitors[columns]
            else:
                hour_zero_values = np.zeros((1, hour_end - hour_start + 1), dtype=int)
                visitors = pd.DataFrame(hour_zero_values, columns=columns[1:-1])
                visitors['date'] = datetime.strptime(date, '%y%m%d')
                visitors['date'] = visitors['date'].astype('str')
                visitors['s'] = 'auto'
                visitors = visitors[columns]

            return visitors

        def dt_slice_shape_df(df_cam, dt_start, dt_end):
            df = df_cam.copy()
            dt_end_full = str(int(dt_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]

        def dt_slice_visitors(visitors, dt_start, dt_end):
            df_visitors = visitors.copy()
            dt_end_full = str(int(dt_end) + 1)
            df_visitors['dt'] = df_visitors['date'].apply(lambda x: ''.join(str(x)[2:].split('-')))
            return df_visitors[(df_visitors['dt'] >= dt_start) & (df_visitors['dt'] < dt_end_full)].iloc[:, 0:-1]

        def update_visitors(cam_name, date_start, date_end):
            if not cam_name[-1].isdigit() or cam_name[-1] == '1':
                # visitors_counting algorithm works only with days
                day_start = date_start[:6]
                day_end = date_end[:6]

                camconfig = load_camconfig()
                cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
                cur_params = tuple(map(int, cam_set['vis_count_alg'].strip('()').split(', ')))
                mean_threshold, window_next = cur_params

                cam_shapes = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{cam_name}_shapes_locs.csv'))
                slice_cam_shapes = dt_slice_shape_df(cam_shapes, day_start, day_end)

                new_cam_visitors = pd.DataFrame()
                slice_days = slice_cam_shapes['origin_file_name'].apply(lambda x: x[:6]).unique()
                for day in slice_days:
                    day_shapes = dt_slice_shape_df(slice_cam_shapes, day, day)
                    day_shapes['cam_name'] = cam_name
                    day_visitors = visitors_counting(cam_name, day_shapes, day, mean_threshold, window_next)
                    new_cam_visitors = pd.concat([new_cam_visitors, day_visitors])

                cam_visitors = pd.read_csv(os.path.join(os.getcwd(), 'db', f'{short_name(cam_name)}_visitors.csv'))
                cam_visitors = cam_visitors.sort_values('date')
                cam_visitors = cam_visitors.reset_index(drop=True)

                if len(new_cam_visitors) != 0:
                    cam_visitors.set_index('date', inplace=True)
                    new_cam_visitors.set_index('date', inplace=True)
                    auto_cam_visitors = cam_visitors[cam_visitors['s'] != 'real'].copy()
                    auto_cam_visitors.update(new_cam_visitors)
                    cam_visitors.update(auto_cam_visitors)
                    cam_visitors.reset_index(inplace=True)
                    cam_visitors.to_csv(
                        os.path.join(os.getcwd(), 'db', f'{short_name(cam_name)}_visitors.csv'), index=False)
                else:
                    hour_start = int(cam_set['work_hours'].strip('()').split(', ')[0])
                    hour_end = int(cam_set['work_hours'].strip('()').split(', ')[1])
                    dt_date_start = datetime.strptime(day_start, '%y%m%d')
                    dt_date_end = datetime.strptime(day_end, '%y%m%d')

                    dt_delta = dt_date_end - dt_date_start
                    dt_days_range = []
                    for i in range(dt_delta.days + 1):
                        dt_day = dt_date_start + timedelta(days=i)
                        dt_days_range.append(dt_day)

                    zero_date = pd.DataFrame({'date': dt_days_range})
                    zero_hours_sum = pd.DataFrame(np.zeros((len(dt_days_range), hour_end - hour_start + 1), dtype=int),
                                                  columns=cam_visitors.columns[1:-1])
                    zero_visitors = pd.concat([zero_date, zero_hours_sum], axis=1)
                    zero_visitors['date'] = zero_visitors['date'].astype('str')
                    zero_visitors['s'] = 'auto'

                    cam_visitors.set_index('date', inplace=True)
                    zero_visitors.set_index('date', inplace=True)
                    auto_cam_visitors = cam_visitors[cam_visitors['s'] != 'real'].copy()
                    auto_cam_visitors.update(zero_visitors)
                    cam_visitors.update(auto_cam_visitors)
                    cam_visitors.reset_index(inplace=True)
                    cam_visitors.to_csv(
                        os.path.join(os.getcwd(), 'db', f'{short_name(cam_name)}_visitors.csv'), index=False)

        cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()
        text_wait = self.main_window.text_wait
        text_saved_successfully = self.main_window.text_saved_successfully

        self.output_message.emit(text_wait)
        if self.direction == 'shape_zone':
            set_shape_coords(date_start, date_end)
            if (len(date_start) & len(date_end)) != 0:
                if os.path.exists(os.path.join(os.getcwd(), 'db', f'{short_name(cam_name)}_visitors.csv')):
                    update_visitors(cam_name, date_start, date_end)
        else:
            set_register_coords(date_start, date_end)
        self.output_message.emit(text_saved_successfully)

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
        self.ShowZoneWindow = None
        self.SetZoneWindow = None

        # Loading the user interface
        # If you use UI code, activate it
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # If you use UI file, activate it
        # uic.loadUi(os.path.join(os.getcwd(), '05_CVsetCam_gui_v1.ui'), self)

        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)

        self.pb_choose_cam = self.findChild(QPushButton, 'pb_choose_cam')
        self.le_cam_name = self.findChild(QLineEdit, 'le_cam_name')
        self.pb_show_camconfig = self.findChild(QPushButton, 'pb_show_camconfig')
        self.le_hour_start = self.findChild(QLineEdit, 'le_hour_start')
        self.le_hour_end = self.findChild(QLineEdit, 'le_hour_end')
        self.pb_hours_save = self.findChild(QPushButton, 'pb_hours_save')

        self.le_date_start = self.findChild(QLineEdit, 'le_date_start')
        self.le_date_end = self.findChild(QLineEdit, 'le_date_end')
        self.pb_last_10_days_1 = self.findChild(QPushButton, 'pb_last_10_days_1')
        self.pb_last_10_days_2 = self.findChild(QPushButton, 'pb_last_10_days_2')

        self.pb_show_shape_zone = self.findChild(QPushButton, 'pb_show_shape_zone')
        self.le_shape_zone_1 = self.findChild(QLineEdit, 'le_shape_zone_1')
        self.pb_set_shape_zone_1 = self.findChild(QPushButton, 'pb_set_shape_zone_1')
        self.le_shape_zone_2 = self.findChild(QLineEdit, 'le_shape_zone_2')
        self.pb_set_shape_zone_2 = self.findChild(QPushButton, 'pb_set_shape_zone_2')
        self.le_shape_zone_3 = self.findChild(QLineEdit, 'le_shape_zone_3')
        self.pb_set_shape_zone_3 = self.findChild(QPushButton, 'pb_set_shape_zone_3')
        self.pb_save_shape_zone = self.findChild(QPushButton, 'pb_save_shape_zone')

        self.pb_show_register_zone = self.findChild(QPushButton, 'pb_show_register_zone')
        self.le_register_zone = self.findChild(QLineEdit, 'le_register_zone')
        self.pb_set_register_zone = self.findChild(QPushButton, 'pb_set_register_zone')
        self.pb_save_register_zone = self.findChild(QPushButton, 'pb_save_register_zone')

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
        self.text_saved_successfully = '<FONT COLOR=#008000>Сохранено успешно</FONT>'


        # Connecting button signals to their slots (functions)
        self.pb_choose_cam.clicked.connect(self.pb_choose_cam_clicked)
        self.pb_show_camconfig.clicked.connect(self.pb_show_camconfig_clicked)
        self.pb_hours_save.clicked.connect(self.pb_hours_save_clicked)
        self.pb_last_10_days_1.clicked.connect(self.pb_last_10_days_1_clicked)
        self.pb_last_10_days_2.clicked.connect(self.pb_last_10_days_2_clicked)

        self.pb_show_shape_zone.clicked.connect(self.pb_show_shape_zone_clicked)
        self.pb_set_shape_zone_1.clicked.connect(self.pb_set_shape_zone_1_clicked)
        self.pb_set_shape_zone_2.clicked.connect(self.pb_set_shape_zone_2_clicked)
        self.pb_set_shape_zone_3.clicked.connect(self.pb_set_shape_zone_3_clicked)
        self.pb_save_shape_zone.clicked.connect(self.pb_save_shape_zone_clicked)

        self.pb_show_register_zone.clicked.connect(self.pb_show_register_zone_clicked)
        self.pb_set_register_zone.clicked.connect(self.pb_set_register_zone_clicked)
        self.pb_save_register_zone.clicked.connect(self.pb_save_register_zone_clicked)

        self.pb_wishes.clicked.connect(self.button_wishes_clicked)
        self.pb_thanks.clicked.connect(self.button_thanks_clicked)

        self.ip_cam_data_paths_dict, self.cam_names = initializer()
        self.disable_enable_ui(False)
        self.show()

    def disable_enable_ui(self, signal):
        self.le_cam_name.setEnabled(signal)
        self.pb_show_camconfig.setEnabled(signal)
        self.le_hour_start.setEnabled(signal)
        self.le_hour_end.setEnabled(signal)
        self.pb_hours_save.setEnabled(signal)
        self.le_date_start.setEnabled(signal)
        self.pb_last_10_days_1.setEnabled(signal)
        self.le_date_end.setEnabled(signal)
        self.pb_last_10_days_2.setEnabled(signal)
        self.pb_show_shape_zone.setEnabled(signal)
        self.le_shape_zone_1.setEnabled(signal)
        self.pb_set_shape_zone_1.setEnabled(signal)
        self.le_shape_zone_2.setEnabled(signal)
        self.pb_set_shape_zone_2.setEnabled(signal)
        self.le_shape_zone_3.setEnabled(signal)
        self.pb_set_shape_zone_3.setEnabled(signal)
        self.pb_save_shape_zone.setEnabled(signal)
        self.pb_show_register_zone.setEnabled(signal)
        self.le_register_zone.setEnabled(signal)
        self.pb_set_register_zone.setEnabled(signal)
        self.pb_save_register_zone.setEnabled(signal)

    def pb_choose_cam_clicked(self):
        self.le_hour_start.setText('')
        self.le_hour_end.setText('')
        self.le_date_start.setText('')
        self.le_date_end.setText('')
        self.le_shape_zone_1.setText('')
        self.le_shape_zone_2.setText('')
        self.le_shape_zone_3.setText('')
        self.le_register_zone.setText('')
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.ShowCams = ShowCams(main_window=self)
        self.ShowCams.show()

    def pb_show_camconfig_clicked(self):
        try:
            cam_name = self.le_cam_name.text()
            camconfig = load_camconfig()
            work_hours = [cam_set['work_hours'] for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
            start_hour = work_hours.split(',')[0][1:]
            end_hour = work_hours.split(',')[1][1:-1]
            self.le_hour_start.setText(start_hour)
            self.le_hour_end.setText(end_hour)
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_hours_save_clicked(self):
        try:
            cam_name = self.le_cam_name.text()
            start_hour = self.le_hour_start.text()
            end_hour = self.le_hour_end.text()
            if (len(start_hour) & len(end_hour)) != 0:
                work_hours = int(start_hour), int(end_hour)
                camconfig = load_camconfig()
                [cam_set.update(work_hours=work_hours) for cam_set in camconfig if cam_set['cam_name'] == cam_name]
                save_camconfig(camconfig)
                self.label_wishes_thanks.setText('')
                self.label_out.setText(self.text_saved_successfully)
        except:
            self.label_out.setText(self.text_data_error)

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
        except:
            self.label_out.setText(self.text_data_error)

    def pb_show_shape_zone_clicked(self):
        try:
            self.ShowZoneWindow = ShowZoneWindow('shape_zone', main_window=self)
            self.ShowZoneWindow.show()
            self.label_out.setText('')
        except:
            self.label_out.setText(self.text_data_range)
        self.label_wishes_thanks.setText('')

    def pb_set_shape_zone_1_clicked(self):
        try:
            self.SetZoneWindow = SetZoneWindow('shapes_1', main_window=self)
            self.SetZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_set_shape_zone_2_clicked(self):
        try:
            self.SetZoneWindow = SetZoneWindow('shapes_2', main_window=self)
            self.SetZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_set_shape_zone_3_clicked(self):
        try:
            self.SetZoneWindow = SetZoneWindow('shapes_3', main_window=self)
            self.SetZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def sending_output_message(self, message):
        self.label_out.setText(message)
        self.label_wishes_thanks.setText(' ')

    def run_SaveRecalculateThread(self, direction):
        self.thread_2 = QThread()
        self.worker_2 = SaveRecalculateThread(direction, main_window=self)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.output_message.connect(self.sending_output_message)
        self.thread_2.start()

    def pb_save_shape_zone_clicked(self):
        try:
            self.run_SaveRecalculateThread('shape_zone')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_show_register_zone_clicked(self):
        try:
            self.ShowZoneWindow = ShowZoneWindow('face_zone', main_window=self)
            self.ShowZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_set_register_zone_clicked(self):
        try:
            self.SetZoneWindow = SetZoneWindow('register', main_window=self)
            self.SetZoneWindow.show()
            self.label_out.setText('')
            self.label_wishes_thanks.setText('')
        except:
            self.label_out.setText(self.text_data_error)

    def pb_save_register_zone_clicked(self):
        try:
            self.run_SaveRecalculateThread('face_zone')
        except:
            self.label_out.setText(self.text_data_error)

    def button_wishes_clicked(self):
        email = '<FONT COLOR=#b96902>videonabexp@gmail.com</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)
        self.label_out.setText('')

    def button_thanks_clicked(self):
        tel = '<FONT COLOR=#b96902>5469 5400 2720 6935</FONT>'
        self.label_wishes_thanks.setText('Благодарность на карту Сбербанк: ' + tel + ' Алексей')
        self.label_out.setText('')

def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

if __name__ == '__main__':
    main()



