from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QDesktopWidget, QApplication,
                             QCheckBox, QProgressBar, QGraphicsScene)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal, QPoint, QRect)
from PyQt5.QtGui import (QPainter, QPen, QBrush, QColor, QPixmap)
from PyQt5 import uic

import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import sys
import os
import shutil

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, cleanup_mei_folders
from utils.contacts import CONTACT_EMAIL, CONTACT_CARD
from utils.funcs_CV import get_coords_from_text, detection_zone_intersection
from utils.funcs_initializer_camconfig_getcamframe import dt_slice_shape_df
import utils.db as db

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
        self.main_window.le_date_start.setEnabled(True)
        self.main_window.le_date_end.setEnabled(True)
        self.main_window.pb_last_10_days_1.setEnabled(True)
        self.main_window.pb_last_10_days_2.setEnabled(True)
        self.main_window.progressBar.setValue(0)


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


class SetZoneWindow(QWidget):
    def __init__(self, main_window, parent=None, *args, **kwargs):
        super(SetZoneWindow, self).__init__(parent, *args, **kwargs)
        self.main_window = main_window
        self.cam_name = self.main_window.le_cam_name.text()
        date_start = self.main_window.le_date_start.text()
        date_end = self.main_window.le_date_end.text()
        self.scene = QGraphicsScene(self)

        self.setWindowTitle('Задать зону детекции')
        self.image = QLabel()

        lay = QVBoxLayout(self)
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
        def zone_intersections(df, zone_coords):
            df = df.copy()
            df['alarm_intersection'] = df['shape_location'].apply(
                lambda x: detection_zone_intersection(get_coords_from_text(x), zone_coords))
            return df[df['alarm_intersection'] == 1].iloc[:, 0:-1]

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
                    if db.shapes_exist(cam_name, os.getcwd()):
                        df_cam = db.read_shapes(cam_name, os.getcwd())

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
        def rectangle_on_shape(img, shape_location, star_position='right'):
            y1, y2, x1, x2 = shape_location
            draw = ImageDraw.Draw(img)

            if star_position == 'right':
                # yellow rectangle and star on the right
                draw.rectangle(((x1, y1), (x2, y2)), outline='#ffff14', width=3)
                draw.ellipse([(x2 - 20, y1 + 2), (x2 - 5, y1 + 17)], fill='#ffff14', outline='#ffff14')
                try:
                    font = ImageFont.truetype("arial.ttf", 12)
                    draw.text((x2 - 16, y1 + 3), "*", fill='#000000', font=font)
                except:
                    draw.text((x2 - 16, y1 + 3), "*", fill='#000000')
            else:
                # red rectangle and star on the left
                draw.rectangle(((x1, y1), (x2, y2)), outline='red', width=3)
                draw.ellipse([(x1 + 2, y1 + 2), (x1 + 17, y1 + 17)], fill='red', outline='red')
                try:
                    font = ImageFont.truetype("arial.ttf", 12)
                    draw.text((x1 + 6, y1 + 3), "*", fill='white', font=font)
                except:
                    draw.text((x1 + 6, y1 + 3), "*", fill='white')

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
                    if db.shapes_exist(cam_name, os.getcwd()):
                        df_cam = db.read_shapes(cam_name, os.getcwd())

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

        uic.loadUi(get_path('ui/04_CVdbViewer_gui_v1.ui'), self)

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint |
            Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint)

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
        email = f'<FONT COLOR=#b96902>{CONTACT_EMAIL}</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)

        # Button for donations

    def button_thanks_clicked(self):
        tel = f'<FONT COLOR=#b96902>{CONTACT_CARD}</FONT>'
        self.label_wishes_thanks.setText('Благодарность на карту Сбербанк: ' + tel + ' Алексей')


def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

if __name__ == '__main__':
    main()



