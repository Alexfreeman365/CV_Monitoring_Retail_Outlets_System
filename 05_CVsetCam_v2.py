from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QDesktopWidget, QApplication)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal, QPoint, QRect)
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap)
from PyQt5 import uic
import sys
import os
import pandas as pd

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, cleanup_mei_folders
from utils.contacts import CONTACT_EMAIL, CONTACT_CARD

from utils.funcs_initializer_camconfig_getcamframe import *
import utils.db as db
from utils.funcs_CV import detection_zone_intersection, get_coords_from_text
from utils.funcs_vis_count_noseller_time import short_name, update_visitors


import atexit
atexit.register(cleanup_mei_folders)


class ShowCams(QWidget):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super(ShowCams, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window

        self.setWindowTitle('Выберете камеру')
        lay = QVBoxLayout(self)
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


class Showlast10days(QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(Showlast10days, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()

        self.setWindowTitle('Выберете день')
        lay = QVBoxLayout(self)
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


class ShowZoneWindow(QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(ShowZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()
        self.cwd_path = os.getcwd() # r'L:\Active_pjs\RG' # os.getcwd()

        self.setWindowTitle('Сохраненная зона детекции')
        self.image = QLabel()

        lay = QVBoxLayout(self)
        lay.addWidget(self.image)

        camconfig = load_camconfig(self.cwd_path)
        imgs_path = self.main_window.ip_cam_data_paths_dict[self.cam_name]
        if (len(date_start) & len(date_end)) == 0:
            last_day = os.listdir(imgs_path)[-1]
            last_img = os.listdir(os.path.join(imgs_path, last_day))[0]
            img_path = os.path.join(imgs_path, last_day, last_img)
            self.coords = [cam_set[self.direction] for cam_set in camconfig if cam_set['cam_name'] == self.cam_name][0]
            self.coords = get_coords_from_text(str(self.coords))
        else:
            first_range_day = '20' + date_start[:6]
            images = os.listdir(os.path.join(imgs_path, first_range_day))
            first_range_img = [img for img in images if img[:len(date_start)] == date_start][0]
            img_path = os.path.join(imgs_path, first_range_day, first_range_img)
            df_cam = db.read_shapes(self.cam_name, self.cwd_path)
            df_cam_slice = dt_slice_shape_df(df_cam, date_start, date_end)
            if self.direction == 'shape_zone':
                self.coords = df_cam_slice.iloc[0]['shape_zone_coords']
            else:
                self.coords = df_cam_slice.iloc[0]['face_zone_coords']
            self.coords = get_coords_from_text(str(self.coords))

        self.pixmap = QPixmap(img_path)
        self.pixmap_small = self.pixmap.scaled(int(self.pixmap.width() / 1.5), int(self.pixmap.height() / 1.5))
        self.setGeometry(320, 200, 0, 0)
        self.setMinimumSize(int(self.pixmap_small.width()), int(self.pixmap_small.height()))

        self.setCoordsToEditLines()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.green, 2)
        painter.setPen(pen)
        br = QBrush(QColor(200, 10, 10, 40))
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
                # convert numpy types to plain int
                coords_tuple = tuple(int(c) for c in self.coords)
                self.main_window.le_shape_zone_1.setText(str(coords_tuple))
            if len(self.coords) == 3:
                coords_set = self.coords
                self.main_window.le_shape_zone_1.setText(str(tuple(int(c) for c in coords_set[0])))
                self.main_window.le_shape_zone_2.setText(str(tuple(int(c) for c in coords_set[1])))
                self.main_window.le_shape_zone_3.setText(str(tuple(int(c) for c in coords_set[2])))
            if len(self.coords) == 2:
                coords_set = self.coords
                self.main_window.le_shape_zone_1.setText(str(tuple(int(c) for c in coords_set[0])))
                self.main_window.le_shape_zone_2.setText(str(tuple(int(c) for c in coords_set[1])))
        if self.direction == 'face_zone':
            coords_tuple = tuple(int(c) for c in self.coords)
            self.main_window.le_register_zone.setText(str(coords_tuple))


class SetZoneWindow(QWidget):
    def __init__(self, direction, main_window, parent=None, *args, **kwargs):
        super(SetZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.direction = direction
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()

        self.setWindowTitle('Задать зону детекции')
        self.image = QLabel()

        lay = QVBoxLayout(self)
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

    def paint_existing_zone(self, pixmap_small, text):
        coords = get_coords_from_text(text)
        y1, y2, x1, x2 = coords
        y1, y2, x1, x2 = int(y1 / 1.5), int(y2 / 1.5), int(x1 / 1.5), int(x2 / 1.5)
        painterInstance = QPainter(pixmap_small)
        pen = QPen(Qt.yellow, 2)
        painterInstance.setPen(pen)
        br = QBrush(QColor(200, 10, 10, 40))
        painterInstance.setBrush(br)
        painterInstance.drawRect(x1, y1, x2 - x1, y2 - y1)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.yellow, 2)
        painter.setPen(pen)
        br = QBrush(QColor(200, 10, 10, 40))
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
        self.cwd_path = os.getcwd() # r'L:\Active_pjs\RG' # os.getcwd()

    def run(self):
        def change_camconfig_shape_zone(cam_name, shape_zone_coords):
            camconfig = load_camconfig(self.cwd_path)
            [cam_set.update(shape_zone=shape_zone_coords) for cam_set in camconfig if cam_set['cam_name'] == cam_name]
            save_camconfig(camconfig)

        def change_camconfig_face_zone(cam_name, face_zone_coords):
            camconfig = load_camconfig(self.cwd_path)
            [cam_set.update(face_zone=face_zone_coords) for cam_set in camconfig if cam_set['cam_name'] == cam_name]
            save_camconfig(camconfig)

        def change_df_cam_shape_zone(cam_name, shape_zone_coords):
            date_start = self.main_window.le_date_start.text()
            date_end = self.main_window.le_date_end.text()
            df_cam = db.read_shapes(cam_name, self.cwd_path)
            df = df_cam.copy()
            dt_end_full = str(int(date_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'shape_zone'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), shape_zone_coords))
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'shape_zone_coords'] = shape_zone_coords
            df = df.iloc[:, 0:-1]
            db.write_shapes(cam_name, df, self.cwd_path, mode='replace')

        def change_df_cam_face_zone(cam_name, face_zone_coords):
            date_start = self.main_window.le_date_start.text()
            date_end = self.main_window.le_date_end.text()
            df_cam = db.read_shapes(cam_name, self.cwd_path)
            df = df_cam.copy()
            dt_end_full = str(int(date_end) + 1)
            df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'face_zone'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), face_zone_coords))
            df.loc[(df['dt'] >= date_start) & (df['dt'] < dt_end_full), 'face_zone_coords'] = face_zone_coords
            df = df.iloc[:, 0:-1]
            db.write_shapes(cam_name, df, self.cwd_path, mode='replace')

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

        cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()
        text_wait = self.main_window.text_wait
        text_saved_successfully = self.main_window.text_saved_successfully

        self.output_message.emit(text_wait)
        if self.direction == 'shape_zone':
            set_shape_coords(date_start, date_end)
            if (len(date_start) & len(date_end)) != 0:
                if db.visitors_exist(short_name(cam_name), self.cwd_path):
                    update_visitors(cam_name, date_start, date_end, cwd_path=self.cwd_path)
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

        uic.loadUi(get_path('ui/05_CVsetCam_gui_v1.ui'), self)

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint |
            Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint)

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
        self.cwd_path = os.getcwd() # r'L:\Active_pjs\RG' # os.getcwd()

        self.ip_cam_data_paths_dict, self.cam_names = initializer(self.cwd_path)
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
            camconfig = load_camconfig(self.cwd_path)
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
                camconfig = load_camconfig(self.cwd_path)
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
            self.label_out.setText(self.text_data_error)
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



