import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QDialog,
                             QApplication,
                             QLineEdit, QRadioButton,
                             QPushButton, QProgressBar,
                             QLabel, QMessageBox, QCheckBox)
# Operating with the computer's file system
import os
# Deleting an entire branch of the file system along with the contents
import shutil

'''
class Ui_Dialog from Qt designer file. To get it, use this code:
cmd(PyCharm terminal): pyuic5.exe -x file.ui -o file.py
Additionally, in my case, I remove the use of the favicon, 
since in the end there will be only one file with the code.
Next, there will be a branching in the class UI: use this class or file.
It is better to develop with a UI file for speed. 
When the program is ready and there are no additional files other than the UI and the code itself, 
it is better to include the UI file in the main code. 
In order for the user to be able to use only one exe file.
'''

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(581, 542)
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:\\07_Development\\Pjs\\hiSampler\\Favicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWhatsThis("")
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 541, 501))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_7.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setText("")
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 4)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_5.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 4)
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
        self.gridLayout.addWidget(self.pb_wishes, 16, 0, 1, 3)
        self.label_1 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_92 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_92.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_92.setFont(font)
        self.label_92.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_92.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_92.setObjectName("label_92")
        self.gridLayout.addWidget(self.label_92, 12, 0, 1, 4)
        self.pb_choice = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_choice.setEnabled(True)
        self.pb_choice.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_choice.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_choice.setFont(font)
        self.pb_choice.setObjectName("pb_choice")
        self.gridLayout.addWidget(self.pb_choice, 13, 2, 1, 2)
        self.op_wishes_thanks = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.op_wishes_thanks.setFont(font)
        self.op_wishes_thanks.setMouseTracking(False)
        self.op_wishes_thanks.setText("")
        self.op_wishes_thanks.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.op_wishes_thanks.setWordWrap(True)
        self.op_wishes_thanks.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.op_wishes_thanks.setObjectName("op_wishes_thanks")
        self.gridLayout.addWidget(self.op_wishes_thanks, 15, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 4)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_4.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 4)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_9.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 10, 2, 1, 1)
        self.label_91 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_91.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_91.setFont(font)
        self.label_91.setAlignment(QtCore.Qt.AlignCenter)
        self.label_91.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_91.setObjectName("label_91")
        self.gridLayout.addWidget(self.label_91, 10, 3, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.op_sample_num = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.op_sample_num.setFont(font)
        self.op_sample_num.setMouseTracking(False)
        self.op_sample_num.setText("")
        self.op_sample_num.setAlignment(QtCore.Qt.AlignCenter)
        self.op_sample_num.setWordWrap(True)
        self.op_sample_num.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.op_sample_num.setObjectName("op_sample_num")
        self.gridLayout.addWidget(self.op_sample_num, 11, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.rb_over_5 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.rb_over_5.setEnabled(True)
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
        self.rb_over_5.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rb_over_5.setFont(font)
        self.rb_over_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rb_over_5.setChecked(False)
        self.rb_over_5.setAutoExclusive(True)
        self.rb_over_5.setObjectName("rb_over_5")
        self.gridLayout.addWidget(self.rb_over_5, 8, 2, 1, 1)
        self.rb_over_3 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.rb_over_3.setEnabled(True)
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
        self.rb_over_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rb_over_3.setFont(font)
        self.rb_over_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rb_over_3.setChecked(False)
        self.rb_over_3.setAutoExclusive(True)
        self.rb_over_3.setObjectName("rb_over_3")
        self.gridLayout.addWidget(self.rb_over_3, 8, 1, 1, 1)
        self.cb_move = QtWidgets.QCheckBox(self.gridLayoutWidget)
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
        self.cb_move.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_move.setFont(font)
        self.cb_move.setObjectName("cb_move")
        self.gridLayout.addWidget(self.cb_move, 13, 0, 1, 2)
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
        self.gridLayout.addWidget(self.pb_thanks, 16, 3, 1, 1)
        self.op_total_num = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.op_total_num.setFont(font)
        self.op_total_num.setMouseTracking(False)
        self.op_total_num.setText("")
        self.op_total_num.setAlignment(QtCore.Qt.AlignCenter)
        self.op_total_num.setWordWrap(True)
        self.op_total_num.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.op_total_num.setObjectName("op_total_num")
        self.gridLayout.addWidget(self.op_total_num, 11, 2, 1, 1)
        self.output = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.output.setFont(font)
        self.output.setMouseTracking(False)
        self.output.setText("")
        self.output.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.output.setWordWrap(True)
        self.output.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.output.setObjectName("output")
        self.gridLayout.addWidget(self.output, 14, 0, 1, 4)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_6.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 1)
        self.rb_over_10 = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.rb_over_10.setEnabled(True)
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
        self.rb_over_10.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.rb_over_10.setFont(font)
        self.rb_over_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rb_over_10.setCheckable(True)
        self.rb_over_10.setChecked(True)
        self.rb_over_10.setAutoRepeat(False)
        self.rb_over_10.setAutoExclusive(True)
        self.rb_over_10.setObjectName("rb_over_10")
        self.gridLayout.addWidget(self.rb_over_10, 8, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
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
        self.label_8.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 10, 0, 1, 2)
        self.pb_calculate = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pb_calculate.setEnabled(True)
        self.pb_calculate.setMinimumSize(QtCore.QSize(0, 0))
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
        self.pb_calculate.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pb_calculate.setFont(font)
        self.pb_calculate.setObjectName("pb_calculate")
        self.gridLayout.addWidget(self.pb_calculate, 11, 0, 1, 2)
        self.op_wishes_thanks.setBuddy(self.pb_wishes)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.rb_over_3, self.rb_over_5)
        Dialog.setTabOrder(self.rb_over_5, self.rb_over_10)
        Dialog.setTabOrder(self.rb_over_10, self.pb_calculate)
        Dialog.setTabOrder(self.pb_calculate, self.cb_move)
        Dialog.setTabOrder(self.cb_move, self.pb_choice)
        Dialog.setTabOrder(self.pb_choice, self.pb_wishes)
        Dialog.setTabOrder(self.pb_wishes, self.pb_thanks)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "hiSampler"))
        self.label_5.setText(_translate("Dialog", "- Выберите через какое количество нужны фотографии"))
        self.pb_wishes.setText(_translate("Dialog", "Пожелания"))
        self.label_1.setText(_translate("Dialog", "Программа для выборки фотографий"))
        self.label_92.setText(_translate("Dialog", "После нажатия \"Выбрать\" программа создаст рядом папку и скопирует в неё фотографии"))
        self.pb_choice.setText(_translate("Dialog", "Выбрать"))
        self.label_4.setText(_translate("Dialog", "- Поместите копию программы в папку c фотографиями"))
        self.label_9.setText(_translate("Dialog", "общее"))
        self.label_91.setText(_translate("Dialog", "выборка"))
        self.label_3.setText(_translate("Dialog", "Рецепт:"))
        self.rb_over_5.setText(_translate("Dialog", "5"))
        self.rb_over_3.setText(_translate("Dialog", "3"))
        self.cb_move.setText(_translate("Dialog", "С перемещением"))
        self.pb_thanks.setText(_translate("Dialog", "Спасибо!"))
        self.label_6.setText(_translate("Dialog", "через:"))
        self.rb_over_10.setText(_translate("Dialog", "10"))
        self.label_8.setText(_translate("Dialog", "Предварительный расчет:"))
        self.pb_calculate.setText(_translate("Dialog", "Рассчитать"))


# First worker thread for collecting summary information about files in a selected time range
class EstimateThread(QThread):
    # Signals to the main UI thread
    # Signal that the thread has finished working
    finished = pyqtSignal()
    # Signal for messages output to the user
    output_message = pyqtSignal(str)
    total_num_message = pyqtSignal(str)
    sample_num_message = pyqtSignal(str)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(EstimateThread, self).__init__(parent)
        self.main_window = main_window
        self.cwd_path = self.main_window.cwd_path
        self.text_wait = self.main_window.text_wait
        self.text_success = self.main_window.text_success

    def run(self):
        # Function to get the entire range of days existing on the SD card
        def total_and_sample_num():
            step_of_frames = int
            if self.main_window.radioButton_over_3.isChecked():
                step_of_frames = 3
            if self.main_window.radioButton_over_5.isChecked():
                step_of_frames = 5
            if self.main_window.radioButton_over_10.isChecked():
                step_of_frames = 10

            img_names = [img for img in os.listdir(self.cwd_path) if img.endswith(('.jpg', '.png', 'jpeg'))]
            total_num = len(img_names)

            short_list_names = [img_names[i] for i in range(0, len(img_names), step_of_frames)]
            sample_num = len(short_list_names)
            return str(total_num), str(sample_num)

        # Starting thread execution in the try-except error handling construct
        try:
            # Sending a message to the user about the need to wait
            total_num, sample_num = total_and_sample_num()
            self.total_num_message.emit(total_num)
            self.sample_num_message.emit(sample_num)

        except:
            text_error = '<FONT COLOR=#f4320c>Проблемы с оценкой. ' \
                         'Возможно рядом с программой нет фотографий (.jpg, .png, .jpeg)</FONT>'
            self.output_message.emit(text_error)

        # A message to the main UI thread that this working thread has finished executing its code.
        self.finished.emit()


# Second worker thread for download a video from the selected time range
class ParseThread(QThread):
    # Signals to the main UI thread (Similar and detailed in the first work thread)
    finished = pyqtSignal()
    output_message = pyqtSignal(str)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(ParseThread, self).__init__(parent)
        self.main_window = main_window
        self.cwd_path = self.main_window.cwd_path
        self.text_wait = self.main_window.text_wait
        self.text_done = self.main_window.text_done

    def run(self):
        def choice():
            step_of_frames = int
            if self.main_window.radioButton_over_3.isChecked():
                step_of_frames = 3
            if self.main_window.radioButton_over_5.isChecked():
                step_of_frames = 5
            if self.main_window.radioButton_over_10.isChecked():
                step_of_frames = 10

            img_names = [img for img in os.listdir(self.cwd_path) if img.endswith(('.jpg', '.png', 'jpeg'))]
            img_num = len(img_names)

            short_list_names = [img_names[i] for i in range(0, len(img_names), step_of_frames)]
            new_folder_name = os.path.basename(self.cwd_path) + f'_x{step_of_frames}'

            if os.path.exists(os.path.join(self.cwd_path, new_folder_name)):
                shutil.rmtree(os.path.join(self.cwd_path, new_folder_name))
                if len(short_list_names) != 0:
                    os.mkdir(os.path.join(self.cwd_path, new_folder_name))
            else:
                if len(short_list_names) != 0:
                    os.mkdir(os.path.join(self.cwd_path, new_folder_name))

            if self.main_window.checkBox_move.isChecked():
                for img_name in short_list_names:
                    src_path = os.path.join(self.cwd_path, img_name)
                    dist_path = os.path.join(self.cwd_path, new_folder_name, img_name)
                    shutil.move(src_path, dist_path)

            else:
                for img_name in short_list_names:
                    src_path = os.path.join(self.cwd_path, img_name)
                    dist_path = os.path.join(self.cwd_path, new_folder_name, img_name)
                    shutil.copyfile(src_path, dist_path)
            return img_num

        try:
            # Sending a message to the user about the need to wait
            self.output_message.emit(self.text_wait)
            # Getting a list of existing days on the SD card
            img_num = choice()
            if img_num == 0:
                text_error = '<FONT COLOR=#f4320c>Проблемы с выборкой. ' \
                             'Возможно рядом с программой нет фотографий (.jpg, .png, .jpeg)</FONT>'
                self.output_message.emit(text_error)
            else:
                self.output_message.emit(self.text_done)
        except:
            text_error = '<FONT COLOR=#f4320c>Проблемы с выборкой. ' \
                         'Возможно рядом с программой нет фотографий (.jpg, .png, .jpeg)</FONT>'
            self.output_message.emit(text_error)
        # A message to the main UI thread that this working thread has finished executing its code.
        self.finished.emit()


# Declaring the class of the main UI thread
class UI(QDialog):
    def __init__(self):
        super(UI, self).__init__()
        # Variables for working classes and their threads
        self.worker = None
        self.thread = None
        self.worker_2 = None
        self.thread_2 = None

        # Loading the user interface
        # If you use UI code, activate it
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


        # If you use UI file, activate it
        #uic.loadUi(os.path.join(os.getcwd(), '1_hiSampler_v1_GUI.ui'), self)

        self.text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
        self.text_success = '<FONT COLOR=#008000>Успешно</FONT>'
        self.text_error = '<FONT COLOR=#f4320c>Ошибка</FONT>'
        self.text_done = '<FONT COLOR=#008000>Выполнено!</FONT>'

        # Removing the windows hint button of the window,
        # which is formed by default in Qt designer and adding 'Minimize' btn
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)

        # Define UI widgets
        self.label_total_num = self.findChild(QLabel, 'op_total_num')
        self.label_sample_num = self.findChild(QLabel, 'op_sample_num')
        self.label_output = self.findChild(QLabel, 'output')
        self.label_wishes_thanks = self.findChild(QLabel, 'op_wishes_thanks')
        self.pushButton_calculate = self.findChild(QPushButton, 'pb_calculate')
        self.pushButton_choice = self.findChild(QPushButton, 'pb_choice')
        self.pushButton_wishes = self.findChild(QPushButton, 'pb_wishes')
        self.pushButton_thanks = self.findChild(QPushButton, 'pb_thanks')

        self.radioButton_over_3 = self.findChild(QRadioButton, 'rb_over_3')
        self.radioButton_over_5 = self.findChild(QRadioButton, 'rb_over_5')
        self.radioButton_over_10 = self.findChild(QRadioButton, 'rb_over_10')

        self.checkBox_move = self.findChild(QCheckBox, 'cb_move')


        # Variables initialization
        self.cwd_path = os.getcwd()

        # Connecting button signals to their slots (functions)
        self.pushButton_calculate.clicked.connect(self.button_calculate_clicked)
        self.pushButton_choice.clicked.connect(self.button_choice_clicked)

        self.pushButton_wishes.clicked.connect(self.button_wishes_clicked)
        self.pushButton_thanks.clicked.connect(self.button_thanks_clicked)

        # Show the app
        self.show()

    def sending_output_message_estimate(self, message):
        self.label_output.setText(message)
        self.label_wishes_thanks.setText(' ')

    def sending_total_num_message_estimate(self, message):
        text = f'<FONT COLOR=#b96902>{message}</FONT>'
        self.label_total_num.setText(text)
        self.label_wishes_thanks.setText(' ')

    def sending_sample_num_message_estimate(self, message):
        text = f'<FONT COLOR=#008000>{message}</FONT>'
        self.label_sample_num.setText(text)
        self.label_wishes_thanks.setText(' ')

    # The function of starting the first working thread
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
        self.worker.output_message.connect(self.sending_output_message_estimate)
        self.worker.total_num_message.connect(self.sending_total_num_message_estimate)
        self.worker.sample_num_message.connect(self.sending_sample_num_message_estimate)
        # Step 5: Start the thread
        self.thread.start()

    def button_calculate_clicked(self):
        self.label_output.setText('')
        self.label_wishes_thanks.setText('')
        self.run_EstimateThread()

    def sending_output_message_parser(self, message):
        self.label_output.setText(message)
        self.label_wishes_thanks.setText(' ')

    # The function of starting the second working thread
    def run_ParseThread(self):
        self.thread_2 = QThread()
        self.worker_2 = ParseThread(main_window=self)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.output_message.connect(self.sending_output_message_parser)
        self.thread_2.start()

    # Processing the button click to start the second working thread
    def button_choice_clicked(self):
        self.label_wishes_thanks.setText('')
        self.run_ParseThread()

    # Feedback button
    def button_wishes_clicked(self):
        email = '<FONT COLOR=#b96902>videonabexp@gmail.com</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)

    # Button for donations
    def button_thanks_clicked(self):
        tel = '<FONT COLOR=#b96902>5469 5400 2720 6935</FONT>'
        thanks_text = 'Благодарность на карту Сбербанк: '
        self.label_wishes_thanks.setText(thanks_text + tel + ' Алексей')


def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()


if __name__ == '__main__':
    main()
