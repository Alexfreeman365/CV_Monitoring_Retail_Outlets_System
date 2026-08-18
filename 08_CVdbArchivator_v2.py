from PyQt5.QtWidgets import (QApplication, QDialog, QPushButton, 
                             QLineEdit, QLabel, QWidget, QVBoxLayout, 
                             QDesktopWidget)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import uic
import pandas as pd
import sys
import os

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, cleanup_mei_folders
from utils.contacts import CONTACT_EMAIL, CONTACT_CARD
from utils.funcs_initializer_camconfig_getcamframe import load_camconfig, dt_slice_shape_df
import utils.db as db

import atexit
atexit.register(cleanup_mei_folders)


class ShowCams(QWidget):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super(ShowCams, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window

        self.setWindowTitle('Выберете камеру')
        lay = QVBoxLayout(self)

        camconfig = load_camconfig()
        cam_names = [cam['cam_name'] for cam in camconfig]

        for cam in cam_names:
            btn = QPushButton()
            btn.setText(cam)
            btn.released.connect(self.button_clicked)
            lay.addWidget(btn)

        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x()-292, centerPoint.y()-205, 0, 0)

    def button_clicked(self):
        clicked_button = self.sender()
        cam_name = clicked_button.text()
        self.main_window.le_cam_name.setText(cam_name)

        cam_shapes = db.read_shapes(cam_name, os.getcwd())
        first_day_all = cam_shapes.iloc[0]['origin_file_name'][:6]
        last_day_all = cam_shapes.iloc[-1]['origin_file_name'][:6]
        len_all = str(len(cam_shapes))

        self.main_window.lbl_first_full.setText(f'<FONT COLOR=#008000>{first_day_all}</FONT>')
        self.main_window.lbl_last_full.setText(f'<FONT COLOR=#008000>{last_day_all}</FONT>')
        self.main_window.lbl_len_full.setText(f'<FONT COLOR=#008000>{len_all}</FONT>')

        self.main_window.lbl_first_rem.setText(' ')
        self.main_window.lbl_last_rem.setText(' ')
        self.main_window.lbl_len_rem.setText(' ')
        self.main_window.lbl_first_arc.setText(' ')
        self.main_window.lbl_last_arc.setText(' ')
        self.main_window.lbl_len_arc.setText(' ')

        self.close()
        self.main_window.disable_enable_ui(True)


class EstimateThread(QThread):
    finished = pyqtSignal()
    first_day_rem = pyqtSignal(str)
    last_day_rem = pyqtSignal(str)
    len_rem = pyqtSignal(str)
    first_day_arc = pyqtSignal(str)
    last_day_arc = pyqtSignal(str)
    len_arc = pyqtSignal(str)
    output_message = pyqtSignal(str)

    def __init__(self, main_window, parent=None):
        super(EstimateThread, self).__init__(parent)
        self.main_window = main_window
        self.cam_name = self.main_window.le_cam_name.text()
        self.cutoff_day = self.main_window.le_cutoff_day.text()
        self.text_data_error = self.main_window.text_data_error

    def run(self):
        try:
            cam_name = self.cam_name
            cutoff_day = self.cutoff_day
            cam_shapes = db.read_shapes(cam_name, os.getcwd())
            cam_shapes = cam_shapes.sort_values('uid8')
            cam_shapes = cam_shapes.reset_index(drop=True)
            last_day_all = cam_shapes.iloc[-1]['origin_file_name'][:6]

            remaining_shapes = dt_slice_shape_df(cam_shapes, cutoff_day, last_day_all)
            first_day_rem = remaining_shapes.iloc[0]['origin_file_name'][:6]
            last_day_rem = remaining_shapes.iloc[-1]['origin_file_name'][:6]
            len_rem = str(len(remaining_shapes))

            self.first_day_rem.emit(first_day_rem)
            self.last_day_rem.emit(last_day_rem)
            self.len_rem.emit(len_rem)

            archive_shapes = cam_shapes.iloc[:remaining_shapes.index[0]]
            first_day_arc = archive_shapes.iloc[0]['origin_file_name'][:6]
            last_day_arc = archive_shapes.iloc[-1]['origin_file_name'][:6]
            len_arc = str(len(archive_shapes))

            self.first_day_arc.emit(first_day_arc)
            self.last_day_arc.emit(last_day_arc)
            self.len_arc.emit(len_arc)
            self.finished.emit()
        except:
            self.output_message.emit(self.text_data_error)
            self.finished.emit()


class LetsArchiveThread(QThread):
    finished = pyqtSignal()
    output_message = pyqtSignal(str)

    def __init__(self, main_window, parent=None):
        super(LetsArchiveThread, self).__init__(parent)
        self.main_window = main_window
        self.cam_name = self.main_window.le_cam_name.text()
        self.cutoff_day = self.main_window.le_cutoff_day.text()
        self.text_done = self.main_window.text_done
        self.text_data_error = self.main_window.text_data_error

    def run(self):
        try:
            cam_name = self.cam_name
            cutoff_day = self.cutoff_day
            cam_shapes = db.read_shapes(cam_name, os.getcwd())
            cam_shapes = cam_shapes.sort_values('uid8')
            cam_shapes = cam_shapes.reset_index(drop=True)
            last_day_all = cam_shapes.iloc[-1]['origin_file_name'][:6]

            remaining_shapes = dt_slice_shape_df(cam_shapes, cutoff_day, last_day_all)
            archive_shapes = cam_shapes.iloc[:remaining_shapes.index[0]]
            first_day_arc = archive_shapes.iloc[0]['origin_file_name'][:6]
            last_day_arc = archive_shapes.iloc[-1]['origin_file_name'][:6]

            arc_folder_name = f'{first_day_arc}_{last_day_arc}'
            arc_folder_path = os.path.join(os.getcwd(), 'db_shapes_archive', cam_name, arc_folder_name)

            if os.path.exists(os.path.join(os.getcwd(), 'db_shapes_archive')):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(), 'db_shapes_archive'))

            if os.path.exists(os.path.join(os.getcwd(), 'db_shapes_archive', cam_name)):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(), 'db_shapes_archive', cam_name))

            if os.path.exists(arc_folder_path):
                pass
            else:
                os.mkdir(arc_folder_path)

            archive_shapes.to_csv(os.path.join(arc_folder_path, f'{cam_name}_shapes_locs.csv'), index=False)
            db.write_shapes(cam_name, remaining_shapes, os.getcwd(), mode='replace')
            self.output_message.emit(self.text_done)
            self.finished.emit()
        except:
            self.output_message.emit(self.text_data_error)
            self.finished.emit()


class UI(QDialog):
    def __init__(self):
        super(UI, self).__init__()
        self.worker = None
        self.thread = None
        self.worker_2 = None
        self.thread_2 = None
        self.ShowCams = None

        uic.loadUi(get_path('ui/08_CVdbArchivator_gui_v1.ui'), self)

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint |
            Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint)

        self.pb_choose_cam = self.findChild(QPushButton, 'pb_choose_cam')
        self.le_cam_name = self.findChild(QLineEdit, 'le_cam_name')
        self.lbl_first_full = self.findChild(QLabel, 'lbl_first_full')
        self.lbl_last_full = self.findChild(QLabel, 'lbl_last_full')
        self.lbl_len_full = self.findChild(QLabel, 'lbl_len_full')

        self.le_cutoff_day = self.findChild(QLineEdit, 'le_cutoff_day')
        self.pb_estimate = self.findChild(QPushButton, 'pb_estimate')

        self.lbl_first_rem = self.findChild(QLabel, 'lbl_first_rem')
        self.lbl_last_rem = self.findChild(QLabel, 'lbl_last_rem')
        self.lbl_len_rem = self.findChild(QLabel, 'lbl_len_rem')

        self.lbl_first_arc = self.findChild(QLabel, 'lbl_first_arc')
        self.lbl_last_arc = self.findChild(QLabel, 'lbl_last_arc')
        self.lbl_len_arc = self.findChild(QLabel, 'lbl_len_arc')
        self.pb_lets_archive = self.findChild(QPushButton, 'pb_lets_archive')

        self.label_out = self.findChild(QLabel, 'label_out')
        self.label_wishes_thanks = self.findChild(QLabel, 'label_wishes_thanks')

        self.pb_wishes = self.findChild(QPushButton, 'pb_wishes')
        self.pb_thanks = self.findChild(QPushButton, 'pb_thanks')

        # Variables initialization
        self.text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
        self.text_error = '<FONT COLOR=#f4320c>Ошибка</FONT>'
        self.text_data_error = '<FONT COLOR=#f4320c>Проверьте входит ли введенный день в текущую базу</FONT>'
        self.text_done = '<FONT COLOR=#008000>Выполнено!</FONT>'

        # Connecting button signals to their slots (functions)
        self.pb_choose_cam.clicked.connect(self.pb_choose_cam_clicked)
        self.pb_estimate.clicked.connect(self.pb_estimate_clicked)
        self.pb_lets_archive.clicked.connect(self.pb_lets_archive_clicked)

        self.pb_wishes.clicked.connect(self.button_wishes_clicked)
        self.pb_thanks.clicked.connect(self.button_thanks_clicked)

        self.disable_enable_ui(False)
        self.show()

    def disable_enable_ui(self, signal):
        self.le_cam_name.setEnabled(signal)
        self.le_cutoff_day.setEnabled(signal)
        self.pb_estimate.setEnabled(signal)
        self.pb_lets_archive.setEnabled(signal)

    def pb_choose_cam_clicked(self):
        self.le_cam_name.setText('')
        self.le_cutoff_day.setText('')
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.ShowCams = ShowCams(main_window=self)
        self.ShowCams.show()

    def sending_first_day_rem(self, message):
        self.lbl_first_rem.setText(f'<FONT COLOR=#008000>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_last_day_rem(self, message):
        self.lbl_last_rem.setText(f'<FONT COLOR=#008000>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_len_rem(self, message):
        self.lbl_len_rem.setText(f'<FONT COLOR=#008000>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_first_day_arc(self, message):
        self.lbl_first_arc.setText(f'<FONT COLOR=#b96902>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_last_day_arc(self, message):
        self.lbl_last_arc.setText(f'<FONT COLOR=#b96902>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_len_arc(self, message):
        self.lbl_len_arc.setText(f'<FONT COLOR=#b96902>{message}</FONT>')
        self.label_out.setText(' ')
        self.label_wishes_thanks.setText(' ')

    def sending_output_message(self, message):
        self.label_out.setText(message)
        self.label_wishes_thanks.setText(' ')

    def run_EstimateThread(self):
        self.thread = QThread()
        self.worker = EstimateThread(main_window=self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.first_day_rem.connect(self.sending_first_day_rem)
        self.worker.last_day_rem.connect(self.sending_last_day_rem)
        self.worker.len_rem.connect(self.sending_len_rem)
        self.worker.first_day_arc.connect(self.sending_first_day_arc)
        self.worker.last_day_arc.connect(self.sending_last_day_arc)
        self.worker.len_arc.connect(self.sending_len_arc)
        self.worker.output_message.connect(self.sending_output_message)
        self.thread.start()

    def pb_estimate_clicked(self):
        self.run_EstimateThread()

    def run_LetsArchiveThread(self):
        self.thread_2 = QThread()
        self.worker_2 = LetsArchiveThread(main_window=self)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.output_message.connect(self.sending_output_message)
        self.thread_2.start()

    def pb_lets_archive_clicked(self):
        self.run_LetsArchiveThread()

    def button_wishes_clicked(self):
        email = f'<FONT COLOR=#b96902>{CONTACT_EMAIL}</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)
        self.label_out.setText('')

    def button_thanks_clicked(self):
        tel = f'<FONT COLOR=#b96902>{CONTACT_CARD}</FONT>'
        self.label_wishes_thanks.setText('Благодарность на карту Сбербанк: ' + tel + ' Алексей')
        self.label_out.setText('')


def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

if __name__ == '__main__':
    main()



