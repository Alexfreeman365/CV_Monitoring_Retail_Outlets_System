import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import (QDialog,
                             QApplication,
                             QLineEdit, QRadioButton,
                             QPushButton, QProgressBar,
                             QLabel, QMessageBox)
import os
import time
from datetime import datetime, timedelta
import pickle
import ftplib
import traceback

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, log_event, cleanup_mei_folders, get_app_name
from utils.contacts import CONTACT_EMAIL, CONTACT_CARD

import atexit
atexit.register(cleanup_mei_folders)


# This working thread was created after
# the application was ready to handle an unexpected error.
# The first version of the program handled well
# one of the options of the user error in the IP address:
# either in the subnet or in the device number.
# But if the user makes a mistake in both options,
# then the program needed time to perform all attempts to connect to the wrong address.
# It takes a little time during which the UI is frozen.
# This is a fast part of the program, but in order not to freeze the interface during an error,
# it was decided to allocate it to a separate thread.
class GetDays(QThread):
    # Signals to the main UI thread (Similar and detailed in the first work thread)
    finished = pyqtSignal()
    status_message = pyqtSignal(str)
    message = pyqtSignal(str)
    enable_disable_ui = pyqtSignal(bool)
    start_enable_ui = pyqtSignal(bool)
    days_message = pyqtSignal(list)
    cameras_message = pyqtSignal(list)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(GetDays, self).__init__(parent)
        self.main_window = main_window
        self.ftp_host = self.main_window.ftp_host
        self.ftp_user = self.main_window.ftp_user
        self.ftp_pas = self.main_window.ftp_pas
        self.cam_name = self.main_window.cam_name
        self.days = []
        self.dd = ''
        self.cameras = []

        self.text_wait = self.main_window.text_wait
        self.text_success = self.main_window.text_success
        self.text_error = self.main_window.text_error
        self.text_getdays_problem = self.main_window.text_getdays_problem

    def run(self):
        def get_days_dd():
            try:
                ftp = ftplib.FTP(self.ftp_host, timeout=30)
                ftp.login(self.ftp_user, self.ftp_pas)
                days = [day.split('/')[-1] for day in ftp.nlst(self.cam_name)
                        if day.split('/')[-1].replace('-', '').isdigit()]
                dd = '-' if days and len(days[0].replace('-', '')) != len(days[0]) else ''
                return [day.replace('-', '') for day in days], dd
            except Exception as e:
                return [], ''

        try:
            self.enable_disable_ui.emit(False)
            self.message.emit(self.text_wait)
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pas)
            self.status_message.emit(self.text_success)

            self.cameras = ftp.nlst()
            if self.cameras[0] == '.':
                path = self.cameras[-1]
                self.cameras = [i for i in ftp.nlst(path) if i not in ['.', '..', 'System Volume Information']]
            self.cameras_message.emit(self.cameras)

            if len(self.main_window.lineEdit_cam_name.text()) == 0:
                text_choose_camera = '<FONT COLOR=#008000>' \
                                     'Выберите камеру в списке под кнопкой «[Камеры]» ' \
                                     'и введите её название без кавычек в поле «Камера»</FONT>'
                self.message.emit(text_choose_camera)
                self.enable_disable_ui.emit(True)
            else:
                self.days, self.dd = get_days_dd()
                if len(self.days) == 0:
                    text_empty = '<FONT COLOR=#b96902>Для этой камеры медиафайлов еще нет</FONT>'
                    self.message.emit(text_empty)
                    self.enable_disable_ui.emit(True)
                else:
                    text_first_day = '<FONT COLOR=#008000>{}</FONT>'.format(self.days[0])
                    text_last_day = '<FONT COLOR=#008000>{}</FONT>'.format(self.days[-1])
                    text_day_amount = '<FONT COLOR=#008000>{}</FONT>'.format(str(len(self.days)))
                    text_day_range = ('Первый_день:' + text_first_day + ' Последний_день:' +
                                      text_last_day + ' Дни:' + text_day_amount)
                    self.message.emit(text_day_range)
                    self.days_message.emit(self.days)
                    self.enable_disable_ui.emit(True)



        except:
            self.start_enable_ui.emit(True)
            self.status_message.emit(self.text_error)
            self.message.emit(self.text_getdays_problem)
        self.finished.emit()


# First worker thread for collecting summary information about files in a selected time range
class EstimateThread(QThread):
    # Signals to the main UI thread
    # Signal that the thread has finished working
    finished = pyqtSignal()
    # Signal for messages output to the user
    message = pyqtSignal(str)
    # Signal for setting the progress bar to the initial state
    progress_days_start = pyqtSignal(int)
    # Signal for setting the progress bar intermediate states
    progress_days_process = pyqtSignal(int)
    # Signal to enable and disable UI to prevent unauthorized actions
    enable_disable_ui = pyqtSignal(bool)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(EstimateThread, self).__init__(parent)
        self.main_window = main_window
        self.ftp_host = self.main_window.ftp_host
        self.ftp_user = self.main_window.ftp_user
        self.ftp_pas = self.main_window.ftp_pas
        self.cam_name = self.main_window.cam_name

        self.day_start = self.main_window.day_start
        self.day_end = self.main_window.day_end
        self.ftr_from = self.main_window.ftr_from
        self.ftr_to = self.main_window.ftr_to
        self.str_from = self.main_window.str_from
        self.str_to = self.main_window.str_to
        self.output_dir = self.main_window.output_dir
        self.days = []
        self.dd = ''
        self.day_folders = []
        self.range_days_num = 0
        self.files_num = 0
        self.day_files_size = 0
        self.text_range_days_num = ''
        self.text_files_num = ''
        self.text_day_files_size = ''
        self.text_total = ''

        self.text_wait = self.main_window.text_wait

    def run(self):
        # Function to get the entire range of days existing on the SD card
        def get_days_dd():
            try:
                ftp = ftplib.FTP(self.ftp_host, timeout=30)
                ftp.login(self.ftp_user, self.ftp_pas)
                days = [day.split('/')[-1] for day in ftp.nlst(self.cam_name)
                        if day.split('/')[-1].replace('-', '').isdigit()]
                dd = '-' if days and len(days[0].replace('-', '')) != len(days[0]) else ''
                return [day.replace('-', '') for day in days], dd
            except Exception as e:
                return [], ''

        def get_day_folders(day):
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pas)
            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:]))
            return [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]

        # Formation of a custom time range: a condition for the first hour range
        def time_condition_ftr(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            time_condition = ((self.ftr_from <= video_time_start) & (video_time_end <= self.ftr_to))
            return time_condition

        def image_time_condition_ftr(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            time_condition = ((self.ftr_from <= image_time) & (image_time <= self.ftr_to))
            return time_condition

        # Formation of a custom time range: a condition for the second hour range
        def time_condition_str(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= video_time_start) & (video_time_end <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def image_time_condition_str(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= image_time) & (image_time <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def alarm_condition(link):
            video_status = link.split('/')[-1].split('_')[0][0]
            condition = video_status == 'A'
            return condition

        def get_last_pc_day():
            image_last_pc_day = '0'
            video_last_pc_day = '0'

            file_type_images = '_photos'
            file_type_record = '_videos'

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_images)
                if os.path.exists(image_path):
                    image_last_pc_day = os.listdir(image_path)[-1]

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_record)
                if os.path.exists(video_path):
                    video_last_pc_day = os.listdir(video_path)[-1]

            if image_last_pc_day <= self.days[0]:
                image_last_pc_day = self.days[0]
            if video_last_pc_day <= self.days[0]:
                video_last_pc_day = self.days[0]

            return image_last_pc_day, video_last_pc_day

        # Getting summary information about the video in the selected time range
        def get_summary(image_day_start, video_day_start, image_day_end, video_day_end):
            # Pass through all days included in the selected range
            self.progress_days_start.emit(len(self.days))
            for day in self.days:
                # Defining folders for this day
                day_folders = get_day_folders(day)
                day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                day_image_folders = [folder for folder in day_folders if folder[0] == 'i']

                if self.main_window.radioButton_images.isChecked():
                    if image_day_start <= day <= image_day_end:
                        ftp = ftplib.FTP(self.ftp_host)
                        ftp.login(self.ftp_user, self.ftp_pas)
                        for folder in day_image_folders:
                            folder_files_links = []
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if image_time_condition_ftr(link) | image_time_condition_str(link):
                                    ftp.voidcmd('TYPE I')
                                    self.day_files_size += ftp.size(path + '/' + file)
                                    folder_files_links.append(link)
                            self.files_num += len(folder_files_links)

                if self.main_window.radioButton_alarm.isChecked():
                    if video_day_start <= day <= video_day_end:
                        ftp = ftplib.FTP(self.ftp_host)
                        ftp.login(self.ftp_user, self.ftp_pas)
                        for folder in day_video_folders:
                            folder_files_links = []
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if time_condition_ftr(link) | time_condition_str(link) & alarm_condition(link):
                                    ftp.voidcmd('TYPE I')
                                    self.day_files_size += ftp.size(path + '/' + file)
                                    folder_files_links.append(link)
                            self.files_num += len(folder_files_links)

                # Setting the progress bar execution sequence
                value_days = self.main_window.progressBar_total.value() + 1
                self.progress_days_process.emit(value_days)
            self.progress_days_process.emit(len(self.days))
            # Returns the number of videos and their size in the time range selected by the user
            return self.files_num, round(self.day_files_size / 1024 / 1024)

        # Starting thread execution in the try-except error handling construct
        try:
            # Disable UI to prevent unauthorized actions
            self.enable_disable_ui.emit(False)
            # Sending a message to the user about the need to wait
            self.message.emit(self.text_wait)
            # Getting a list of existing days on the SD card
            self.days, self.dd = get_days_dd()

            if self.main_window.radioButton_refresh.isChecked():
                image_day_start, video_day_start = get_last_pc_day()
                image_day_end, video_day_end = self.days[-1], self.days[-1]

                if self.main_window.radioButton_images.isChecked():
                    self.range_days_num = self.days.index(image_day_end) - self.days.index(image_day_start) + 1
                else:
                    self.range_days_num = self.days.index(video_day_end) - self.days.index(video_day_start) + 1

            else:
                image_day_start, video_day_start = self.day_start, self.day_start
                image_day_end, video_day_end = self.day_end, self.day_end
                # Getting the number of days in the selected range by the user
                self.range_days_num = self.days.index(self.day_end) - self.days.index(self.day_start) + 1

            # Setting the progress bar for days to the initial state
            self.progress_days_start.emit(self.range_days_num)
            # Calculating and sending summary information about the selected time range to the user
            self.files_num, self.day_files_size = get_summary(image_day_start, video_day_start,
                                                                image_day_end, video_day_end)
            text_days_num = '<FONT COLOR=#008000>{}</FONT>'.format(self.range_days_num)
            text_files_num = '<FONT COLOR=#008000>{}</FONT>'.format(self.files_num)
            text_size = '<FONT COLOR=#008000>{}Mb</FONT>'.format(self.day_files_size)
            text_time = '<FONT COLOR=#008000>~{}min</FONT>'.format(self.day_files_size // 46)
            text_total = ('Дни:' + text_days_num + ' Кол-во:' + text_files_num + ' Размер:' + text_size +
                          ' Время_скачивания:' + text_time)
            self.message.emit(text_total)
            # Enable UI
            self.enable_disable_ui.emit(True)
        except:
            self.enable_disable_ui.emit(True)
            text_error = '<FONT COLOR=#f4320c>Проблемы с оценкой. ' \
                         'Попробуйте проверить ваш промежуток времени.</FONT>'
            self.message.emit(text_error)
        # A message to the main UI thread that this working thread has finished executing its code.
        self.finished.emit()


# Second worker thread for download a video from the selected time range
class ParseThread(QThread):
    # Signals to the main UI thread (Similar and detailed in the first work thread)
    finished = pyqtSignal()
    progress_videos_start = pyqtSignal(int)
    progress_videos_process = pyqtSignal(int)
    progress_days_start = pyqtSignal(int)
    progress_days_process = pyqtSignal(int)
    message = pyqtSignal(str)
    enable_disable_ui = pyqtSignal(bool)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(ParseThread, self).__init__(parent)
        self.main_window = main_window
        self.ftp_host = self.main_window.ftp_host
        self.ftp_user = self.main_window.ftp_user
        self.ftp_pas = self.main_window.ftp_pas
        self.cam_name = self.main_window.cam_name

        self.day_start = self.main_window.day_start
        self.day_end = self.main_window.day_end
        self.ftr_from = self.main_window.ftr_from
        self.ftr_to = self.main_window.ftr_to
        self.str_from = self.main_window.str_from
        self.str_to = self.main_window.str_to
        self.output_dir = self.main_window.output_dir
        self.days = []
        self.dd = ''
        self.image_links_dict = {}
        self.video_links_dict = {}
        self.with_deletion_status = self.main_window.radioButton_with_deletion.isChecked()

        self.text_wait = self.main_window.text_wait
        self.text_done = self.main_window.text_done
        self.max_retries = 100 # Maximum number of reconnection attempts
        self.app_name = get_app_name()

    def run(self):
        def get_days_dd():
            try:
                ftp = ftplib.FTP(self.ftp_host, timeout=30)
                ftp.login(self.ftp_user, self.ftp_pas)
                days = [day.split('/')[-1] for day in ftp.nlst(self.cam_name)
                        if day.split('/')[-1].replace('-', '').isdigit()]
                dd = '-' if days and len(days[0].replace('-', '')) != len(days[0]) else ''
                return [day.replace('-', '') for day in days], dd
            except Exception as e:
                return [], ''

        def get_day_folders(day):
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pas)
            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:]))
            return [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]

        # Formation of a custom time range: a condition for the first hour range
        def time_condition_ftr(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            time_condition = ((self.ftr_from <= video_time_start) & (video_time_end <= self.ftr_to))
            return time_condition

        def image_time_condition_ftr(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            time_condition = ((self.ftr_from <= image_time) & (image_time <= self.ftr_to))
            return time_condition

        # Formation of a custom time range: a condition for the second hour range
        def time_condition_str(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= video_time_start) & (video_time_end <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def image_time_condition_str(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= image_time) & (image_time <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def alarm_condition(link):
            video_status = link.split('/')[-1].split('_')[0][0]
            condition = video_status == 'A'
            return condition

        def get_last_pc_day():
            image_last_pc_day = '0'
            video_last_pc_day = '0'

            file_type_images = '_photos'
            file_type_record = '_videos'

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_images)
                if os.path.exists(image_path):
                    image_last_pc_day = os.listdir(image_path)[-1]

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_record)
                if os.path.exists(video_path):
                    video_last_pc_day = os.listdir(video_path)[-1]

            if image_last_pc_day <= self.days[0]:
                image_last_pc_day = self.days[0]
            if video_last_pc_day <= self.days[0]:
                video_last_pc_day = self.days[0]

            return image_last_pc_day, video_last_pc_day

        # A function for getting a dictionary in which the keys are days
        # from the user's time range,
        # and the values are lists of links to videos for each day.
        # The process of getting information from a html page
        # is described in the first working thread.
        def get_video_links(image_day_start, video_day_start, image_day_end, video_day_end):
            for day in self.days:
                day_image_links = []
                day_video_links = []

                if self.main_window.radioButton_images.isChecked():
                    if image_day_start <= day <= image_day_end:
                        ftp = ftplib.FTP(self.ftp_host)
                        ftp.login(self.ftp_user, self.ftp_pas)
                        day_folders = get_day_folders(day)
                        day_image_folders = [folder for folder in day_folders if folder[0] == 'i']
                        for folder in day_image_folders:
                            folder_files_links = []
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if image_time_condition_ftr(link) | image_time_condition_str(link):
                                    file_size = ftp.size(link)
                                    if file_size > 0:
                                        folder_files_links.append(link)
                            day_image_links += folder_files_links
                        if len(day_image_links) > 0:
                            self.image_links_dict[day] = day_image_links

                if self.main_window.radioButton_alarm.isChecked():
                    if video_day_start <= day <= video_day_end:
                        ftp = ftplib.FTP(self.ftp_host)
                        ftp.login(self.ftp_user, self.ftp_pas)
                        day_folders = get_day_folders(day)
                        day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                        for folder in day_video_folders:
                            folder_files_links = []
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if time_condition_ftr(link) | time_condition_str(link) & alarm_condition(link):
                                    file_size = ftp.size(link)
                                    if file_size > 0:
                                        folder_files_links.append(link)
                            day_video_links += folder_files_links
                        if len(day_video_links) > 0:
                            self.video_links_dict[day] = day_video_links
            return self.image_links_dict, self.video_links_dict

        def get_last_day_filenames():
            image_last_pc_day_filenames = []
            video_last_pc_day_filenames = []

            file_type_images = '_photos'
            file_type_record = '_videos'

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_images)
                if os.path.exists(image_path):
                    try:
                        last_day = os.listdir(image_path)[-1]
                        if os.path.exists(os.path.join(image_path, last_day)):
                            image_last_pc_day_filenames = os.listdir(os.path.join(image_path, last_day))
                    except:
                        pass

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, self.cam_name.split('/')[-1] + file_type_record)
                if os.path.exists(video_path):
                    try:
                        last_day = os.listdir(video_path)[-1]
                        if os.path.exists(os.path.join(video_path, last_day)):
                            video_last_pc_day_filenames = os.listdir(os.path.join(video_path, last_day))
                    except:
                        pass

            return image_last_pc_day_filenames, video_last_pc_day_filenames

        def download_files(ftp, file_type, image_last_pc_day_filenames,
                           video_last_pc_day_filenames, day, links, deletion):
            for link in links:
                try:
                    # Getting a title for a future video
                    file_line = link.split('/')[-1]
                    # Moving the video status to the end of the title for
                    # the correct sorting of files by the operating system.
                    file_title = file_line.split('.')[0]
                    file_extension = file_line.split('.')[1]
                    file_status = file_line[0]
                    if file_type in ['_images', '_photos']:
                        file_name = file_title[1:] + '.' + file_extension
                        if file_name not in image_last_pc_day_filenames:
                            with open(os.path.join(self.main_window.output_dir, self.cam_name.split('/')[-1] + file_type,
                                                   day, file_name), 'wb') as file:
                                ftp.retrbinary(f"RETR {link}", file.write)
                        if self.with_deletion_status and deletion:
                            ftp.delete(link)

                    if file_type in ['_videos', '_videos']:
                        file_name = file_title[1:] + '_' + file_status + '.' + file_extension
                        if file_name not in video_last_pc_day_filenames:
                            with open(os.path.join(self.main_window.output_dir, self.cam_name.split('/')[-1] + file_type,
                                                   day, file_name), 'wb') as file:
                                ftp.retrbinary(f"RETR {link}", file.write)
                        if self.with_deletion_status and deletion:
                            ftp.delete(link)
                    # Updating the progress bar for videos
                    count_progress = self.main_window.progressBar_videos.value() + 1
                    self.progress_videos_process.emit(count_progress)
                except (ftplib.error_temp, ftplib.error_perm) as e:
                    # If the connection fails, reconnect
                    log_event(os.getcwd(), self.app_name, self.cam_name, e)
                    time.sleep(5)
                    ftp = ftplib.FTP(self.ftp_host, timeout=30)
                    ftp.login(self.ftp_user, self.ftp_pas)
                    continue  # Try again for the current file
                except Exception as e:
                    log_event(os.getcwd(), self.app_name, self.cam_name, e)
                    continue  # Skipping the problematic file

        # A function that downloads videos from the received dictionary
        # from the previous function with the creation of a file structure.
        def download_series(links_dict_):
            # Creating a folder with the name of the camera's IP address.

            if links_dict_ == self.image_links_dict:
                file_type = '_photos'

                if os.path.exists(self.main_window.output_dir + self.cam_name.split('/')[-1] + file_type):
                    pass
                else:
                    if len(self.image_links_dict) != 0:
                        os.mkdir(self.main_window.output_dir + self.cam_name.split('/')[-1] + file_type)
            else:
                file_type = '_videos'

                if os.path.exists(self.main_window.output_dir + self.cam_name.split('/')[-1] + file_type):
                    pass
                else:
                    if len(self.video_links_dict) != 0:
                        os.mkdir(self.main_window.output_dir + self.cam_name.split('/')[-1] + file_type)

            image_last_pc_day_filenames, video_last_pc_day_filenames = get_last_day_filenames()

            # A passage for each day from the dictionary to get links to the video
            self.progress_days_start.emit(len(links_dict_))
            self.progress_videos_start.emit(10)
            for day in links_dict_.keys():
                ftp = ftplib.FTP(self.ftp_host)
                ftp.login(self.ftp_user, self.ftp_pas)
                # Creating a folder with the name of the day.
                if os.path.exists(os.path.join(self.main_window.output_dir, self.cam_name.split('/')[-1] + file_type, day)):
                    pass  # shutil.rmtree(self.output_dir + day)
                else:
                    os.mkdir(os.path.join(self.main_window.output_dir, self.cam_name.split('/')[-1] + file_type, day))

                # Getting a list of links for the current day
                links = links_dict_[day]
                # Determining the number of links and
                # setting the initial state of the progress bar for the videos
                self.progress_videos_start.emit(len(links))

                download_files(ftp, file_type, image_last_pc_day_filenames,
                               video_last_pc_day_filenames, day, links, deletion=False)

                day_path = os.path.join(self.main_window.output_dir, self.cam_name.split('/')[-1] + file_type, day)
                for file in os.listdir(day_path):
                    file_size = os.path.getsize(os.path.join(day_path, file))
                    if file_size == 0:
                        os.remove(os.path.join(day_path, file))

                image_last_pc_day_filenames, video_last_pc_day_filenames = get_last_day_filenames()

                download_files(ftp, file_type, image_last_pc_day_filenames,
                               video_last_pc_day_filenames, day, links, deletion=True)

                if (file_type in ['_images', '_photos']) & self.with_deletion_status:
                    try:
                        ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'images')
                    except:
                        pass

                if (file_type in ['_videos', '_videos']) & self.with_deletion_status:
                    try:
                        ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'record')
                    except:
                        pass

                if self.with_deletion_status:
                    try:
                        ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])))
                    except:
                        pass

                    try:
                        ftp.rmd(self.cam_name)
                    except:
                        pass


                # Updating the progress bar for days
                value_days = self.main_window.progressBar_days.value() + 1
                self.progress_days_process.emit(value_days)

            # Improving the user interface.
            # When there are no videos in the selected time range,
            # the progress bar looks like a constant cycle.
            # To avoid this, the progress bar is reset and set to the maximum position.
            self.progress_videos_start.emit(10)
            self.progress_videos_process.emit(10)
            self.progress_days_start.emit(10)
            self.progress_days_process.emit(10)

        def downloading_pipeline(text, mode='main'):
            try:
                # Disable UI to prevent unauthorized actions
                self.enable_disable_ui.emit(False)
                # Sending a message to the user about the need to wait
                self.message.emit(text)
                # Getting a list of existing days on the SD card
                self.days, self.dd = get_days_dd()

                if mode == 'main':
                    if self.main_window.radioButton_refresh.isChecked():
                        image_day_start, video_day_start = get_last_pc_day()
                        image_day_end, video_day_end = self.days[-1], self.days[-1]

                        if self.main_window.radioButton_images.isChecked():
                            range_days_num = self.days.index(image_day_end) - self.days.index(image_day_start) + 1
                        else:
                            range_days_num = self.days.index(video_day_end) - self.days.index(video_day_start) + 1

                    else:
                        image_day_start, video_day_start = self.day_start, self.day_start
                        image_day_end, video_day_end = self.day_end, self.day_end
                        # Getting the number of days in the selected range by the user
                        range_days_num = self.days.index(self.day_end) - self.days.index(self.day_start) + 1

                    self.progress_days_start.emit(range_days_num)
                    self.image_links_dict, self.video_links_dict = get_video_links(image_day_start, video_day_start,
                                                                                   image_day_end, video_day_end)
                    if len(self.image_links_dict) != 0:
                        download_series(self.image_links_dict)
                    if len(self.video_links_dict) != 0:
                        download_series(self.video_links_dict)

                    self.message.emit(self.text_done)
                    self.enable_disable_ui.emit(True)

                elif mode == 'auto':
                    if len(self.days) != 0:
                        image_day_start, video_day_start = get_last_pc_day()
                        image_day_end, video_day_end = self.days[-1], self.days[-1]

                        if self.main_window.radioButton_images.isChecked():
                            range_days_num = (self.days.index(image_day_end) -
                                              self.days.index(image_day_start) + 1)
                        else:
                            range_days_num = (self.days.index(video_day_end) -
                                              self.days.index(video_day_start) + 1)

                        self.progress_days_start.emit(range_days_num)
                        self.image_links_dict, self.video_links_dict = {}, {}
                        self.image_links_dict, self.video_links_dict = get_video_links(image_day_start, video_day_start,
                                                                             image_day_end, video_day_end)
                        if len(self.image_links_dict) != 0:
                            download_series(self.image_links_dict)
                        if len(self.video_links_dict) != 0:
                            download_series(self.video_links_dict)

                        self.progress_days_start.emit(10)
                        self.progress_videos_start.emit(10)
                self.enable_disable_ui.emit(True)
            except Exception as e:
                raise  # Passing an exception for processing to the attempt_download

        def downloading_pipeline_error():
            self.enable_disable_ui.emit(True)
            text_error = '<FONT COLOR=#f4320c>Проблемы с соединением или выбранным промежутком времени.</FONT>'
            self.message.emit(text_error)

        def attempt_download(text_wait, mode):
            for attempt in range(self.max_retries):
                try:
                    downloading_pipeline(text_wait, mode=mode)
                    return True
                except (ftplib.error_temp, ftplib.error_perm):
                    downloading_pipeline_error()
                    log_event(os.getcwd(), self.app_name, self.cam_name, f'Reconnect attempt: {attempt}')
                    if attempt < self.max_retries - 1:
                        time.sleep(5)  # Pause before trying again
                        continue
                    return False
                except Exception:
                    log_event(os.getcwd(), self.app_name, self.cam_name, traceback.format_exc())
                    return False

        # The main execution cycle
        success = attempt_download(self.text_wait, mode='main')

        if self.main_window.radioButton_auto.isChecked():
            self.ftr_from = self.main_window.ftr_from
            self.ftr_to = self.main_window.ftr_to
            while self.main_window.radioButton_auto.isChecked():
                try:
                    # Sending a message to the user about the need to wait
                    text_wait = '<FONT COLOR=#02a8ab>-=:АВТО_ОБНОВЛЕНИЕ_АРХИВА:=-</FONT>'

                    if not success:
                        time.sleep(10)  # Extended pause in case of an error
                    success = attempt_download(text_wait, mode='auto')

                except:
                    self.enable_disable_ui.emit(True)
                    text_error = '<FONT COLOR=#f4320c>Проблемы со скачиванием. ' \
                                 'Попробуйте проверить ваш промежуток времени.</FONT>'
                    self.message.emit(text_error)

                self.ftr_from = (datetime.now() - timedelta(hours=0, minutes=20)).strftime("%H%M%S")
                self.str_from = (datetime.now() - timedelta(hours=0, minutes=20)).strftime("%H%M%S")
                time.sleep(5)

        self.finished.emit()


class DeleteThread(QThread):
    # Signals to the main UI thread
    # Signal that the thread has finished working
    finished = pyqtSignal()
    # Signal for messages output to the user
    message = pyqtSignal(str)
    # Signal for setting the progress bar to the initial state
    progress_days_start = pyqtSignal(int)
    # Signal for setting the progress bar intermediate states
    progress_days_process = pyqtSignal(int)
    # Signal to enable and disable UI to prevent unauthorized actions
    enable_disable_ui = pyqtSignal(bool)

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(DeleteThread, self).__init__(parent)
        self.main_window = main_window
        self.ftp_host = self.main_window.ftp_host
        self.ftp_user = self.main_window.ftp_user
        self.ftp_pas = self.main_window.ftp_pas
        self.cam_name = self.main_window.cam_name

        self.day_start = self.main_window.day_start
        self.day_end = self.main_window.day_end
        self.ftr_from = self.main_window.ftr_from
        self.ftr_to = self.main_window.ftr_to
        self.str_from = self.main_window.str_from
        self.str_to = self.main_window.str_to
        self.output_dir = self.main_window.output_dir
        self.days = []
        self.dd = ''
        self.day_folders = []
        self.range_days_num = 0

        self.text_wait = self.main_window.text_wait
        self.text_done = self.main_window.text_done

    def run(self):
        # Function to get the entire range of days existing on the SD card
        def get_days_dd():
            try:
                ftp = ftplib.FTP(self.ftp_host, timeout=30)
                ftp.login(self.ftp_user, self.ftp_pas)
                days = [day.split('/')[-1] for day in ftp.nlst(self.cam_name)
                        if day.split('/')[-1].replace('-', '').isdigit()]
                dd = '-' if days and len(days[0].replace('-', '')) != len(days[0]) else ''
                return [day.replace('-', '') for day in days], dd
            except Exception as e:
                return [], ''

        def get_day_folders(day):
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pas)
            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:]))
            return [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]

        # Formation of a custom time range: a condition for the first hour range
        def time_condition_ftr(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            time_condition = ((self.ftr_from <= video_time_start) & (video_time_end <= self.ftr_to))
            return time_condition

        def image_time_condition_ftr(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            time_condition = ((self.ftr_from <= image_time) & (image_time <= self.ftr_to))
            return time_condition

        # Formation of a custom time range: a condition for the second hour range
        def time_condition_str(link):
            video_time_start = link.split('/')[-1].split('_')[1]
            video_time_end = link.split('/')[-1].split('_')[2].split('.')[0]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= video_time_start) & (video_time_end <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def image_time_condition_str(link):
            image_time = link.split('/')[-1].split('.')[0][7:13]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= image_time) & (image_time <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def alarm_condition(link):
            video_status = link.split('/')[-1].split('_')[0][0]
            condition = video_status == 'A'
            return condition

        # Getting summary information about the video in the selected time range
        def delete_from_ftp(image_day_start, video_day_start, image_day_end, video_day_end):
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pas)
            # Pass through all days included in the selected range
            self.progress_days_start.emit(len(self.days))
            for day in self.days:
                # Defining folders for this day
                day_folders = get_day_folders(day)
                day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                day_image_folders = [folder for folder in day_folders if folder[0] == 'i']

                if self.main_window.radioButton_images.isChecked():
                    if image_day_start <= day <= image_day_end:
                        for folder in day_image_folders:
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if image_time_condition_ftr(link) | image_time_condition_str(link):
                                    ftp.delete(link)

                if self.main_window.radioButton_alarm.isChecked():
                    if video_day_start <= day <= video_day_end:
                        for folder in day_video_folders:
                            path = self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                            file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                            for file in file_names:
                                link = path + '/' + file
                                if time_condition_ftr(link) | time_condition_str(link) & alarm_condition(link):
                                    ftp.voidcmd('TYPE I')
                                    ftp.delete(link)

                try:
                    ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'images')
                except:
                    pass

                try:
                    ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'record')
                except:
                    pass

                try:
                    ftp.rmd(self.cam_name + '/' + f'{self.dd}'.join((day[:4], day[4:6], day[6:])))
                except:
                    pass

                try:
                    ftp.rmd(self.cam_name)
                except:
                    pass

                # Setting the progress bar execution sequence
                value_days = self.main_window.progressBar_total.value() + 1
                self.progress_days_process.emit(value_days)
            self.progress_days_process.emit(len(self.days))

        # Starting thread execution in the try-except error handling construct
        try:
            # Disable UI to prevent unauthorized actions
            self.enable_disable_ui.emit(False)
            # Sending a message to the user about the need to wait
            self.message.emit(self.text_wait)
            # Getting a list of existing days on the SD card
            self.days, self.dd = get_days_dd()

            if self.main_window.radioButton_refresh.isChecked():
                image_day_start, video_day_start = self.days[0], self.days[0]
                image_day_end, video_day_end = self.days[-1], self.days[-1]

                if self.main_window.radioButton_images.isChecked():
                    self.range_days_num = self.days.index(image_day_end) - self.days.index(image_day_start) + 1
                else:
                    self.range_days_num = self.days.index(video_day_end) - self.days.index(video_day_start) + 1

            else:
                image_day_start, video_day_start = self.day_start, self.day_start
                image_day_end, video_day_end = self.day_end, self.day_end
                # Getting the number of days in the selected range by the user
                self.range_days_num = self.days.index(self.day_end) - self.days.index(self.day_start) + 1

            # Setting the progress bar for days to the initial state
            self.progress_days_start.emit(self.range_days_num)
            # Calculating and sending summary information about the selected time range to the user
            delete_from_ftp(image_day_start, video_day_start, image_day_end, video_day_end)
            self.message.emit(self.text_done)
            # Enable UI
            self.enable_disable_ui.emit(True)
        except:
            self.enable_disable_ui.emit(True)
            text_error = '<FONT COLOR=#f4320c>Проблемы с удалением.</FONT>'
            self.message.emit(text_error)
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
        self.worker_3 = None
        self.thread_3 = None
        self.worker_4 = None
        self.thread_4 = None

        uic.loadUi(get_path('ui/01_hiFTPDloader_gui_v3.ui'), self)

        self.button_delete_text = 'Удалить файлы камеры с FTP диска:'
        self.text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
        self.text_success = '<FONT COLOR=#008000>Успешно</FONT>'
        self.text_error = '<FONT COLOR=#f4320c>Ошибка</FONT>'
        self.text_getdays_problem = '<FONT COLOR=#f4320c>Проблемы с доступом. ' \
                                    'Попробуйте проверить host, user, пароль и соединение.</FONT>'
        self.text_done = '<FONT COLOR=#008000>Выполнено!</FONT>'

        # Removing the windows hint button of the window,
        # which is formed by default in Qt designer and adding 'Minimize' btn
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)

        # Define UI widgets
        self.lineEdit_ftp_host = self.findChild(QLineEdit, 'ftp_host')
        self.lineEdit_ftp_user = self.findChild(QLineEdit, 'ftp_user')
        self.lineEdit_ftp_pas = self.findChild(QLineEdit, 'ftp_pas')
        self.lineEdit_cam_name = self.findChild(QLineEdit, 'cam_name')

        self.label_connection = self.findChild(QLabel, 'label_19')
        self.pushButton_days = self.findChild(QPushButton, 'pushButton')
        self.pushButton_days_list = self.findChild(QPushButton, 'pushButton_3')
        self.pushButton_cameras_list = self.findChild(QPushButton, 'cameras')
        self.days_list_window = QMessageBox()
        self.cameras_list_window = QMessageBox()
        self.label_sd_days = self.findChild(QLabel, 'label_15')

        self.lineEdit_day_start = self.findChild(QLineEdit, 'lineEdit_4')
        self.lineEdit_day_end = self.findChild(QLineEdit, 'lineEdit')
        self.radioButton_refresh = self.findChild(QRadioButton, 'radioButton_6')
        self.lineEdit_ftr_from = self.findChild(QLineEdit, 'lineEdit_5')
        self.lineEdit_ftr_from_min = self.findChild(QLineEdit, 'lineEdit_7')
        self.lineEdit_ftr_to = self.findChild(QLineEdit, 'lineEdit_6')
        self.lineEdit_ftr_to_min = self.findChild(QLineEdit, 'lineEdit_10')
        self.radioButton_str = self.findChild(QRadioButton, 'radioButton_3')
        self.lineEdit_str_from = self.findChild(QLineEdit, 'lineEdit_8')
        self.lineEdit_str_from_min = self.findChild(QLineEdit, 'lineEdit_11')
        self.lineEdit_str_to = self.findChild(QLineEdit, 'lineEdit_9')
        self.lineEdit_str_to_min = self.findChild(QLineEdit, 'lineEdit_12')
        self.radioButton_alarm = self.findChild(QRadioButton, 'radioButton')
        self.radioButton_images = self.findChild(QRadioButton, 'radioButton_2')
        self.pushButton_save_settings = self.findChild(QPushButton, 'save_settings')

        self.pushButton_total = self.findChild(QPushButton, 'pushButton_4')
        self.progressBar_total = self.findChild(QProgressBar, 'progressBar_3')
        self.radioButton_auto = self.findChild(QRadioButton, 'radioButton_4')
        self.label_total = self.findChild(QLabel, 'label_17')

        self.pushButton_parse = self.findChild(QPushButton, 'pushButton_2')
        self.radioButton_with_deletion = self.findChild(QRadioButton, 'with_deletion')
        self.progressBar_days = self.findChild(QProgressBar, 'progressBar')
        self.progressBar_videos = self.findChild(QProgressBar, 'progressBar_2')
        self.label_out = self.findChild(QLabel, 'label_7')
        self.progressBar_pb_delete_from_ftp = self.findChild(QProgressBar, 'pb_delete_from_ftp')
        self.pushButton_delete_from_ftp = self.findChild(QPushButton, 'delete_from_ftp')

        self.label_wishes_thanks = self.findChild(QLabel, 'label_18')
        self.pushButton_wishes = self.findChild(QPushButton, 'pushButton_5')
        self.pushButton_thanks = self.findChild(QPushButton, 'pushButton_6')

        # Variables initialization
        self.ftp_host = ''
        self.ftp_user = ''
        self.ftp_pas = ''
        self.cam_name = ''

        self.day_start = ''
        self.day_end = ''
        self.ftr_from = ''
        self.ftr_to = ''
        self.str_from = ''
        self.str_to = ''
        self.alarm_only = True
        # Setting the output directory to the current program folder
        self.cwd_path = os.getcwd()
        self.output_dir = self.cwd_path + '/'
        self.days = []
        self.cameras = []

        # Connecting button signals to their slots (functions)
        self.pushButton_days.clicked.connect(self.button_days_clicked)
        self.pushButton_days_list.clicked.connect(self.button_days_list_clicked)
        self.pushButton_cameras_list.clicked.connect(self.button_cameras_list_clicked)
        self.radioButton_refresh.toggled.connect(self.refresh_open)
        self.radioButton_auto.toggled.connect(self.auto_open)
        self.radioButton_str.toggled.connect(self.second_time_range_open)
        self.pushButton_save_settings.clicked.connect(self.button_save_settings_clicked)
        self.pushButton_total.clicked.connect(self.button_total_clicked)
        self.pushButton_parse.clicked.connect(self.button_parse_clicked)
        self.pushButton_delete_from_ftp.clicked.connect(self.button_delete_from_ftp_clicked)
        self.pushButton_wishes.clicked.connect(self.button_wishes_clicked)
        self.pushButton_thanks.clicked.connect(self.button_thanks_clicked)

        # Show the app
        self.show()

    # Checking and correcting user input for spaces and emptiness
    def check_and_fix_spaces(self, row):
        if row[-1] == '\n':
            row = row[:-1]
        while row[-1] == ' ':
            row = row[:-1]
        while row[0] == ' ':
            row = row[1:]
        return row

    def start_enable_ui(self, signal):
        self.lineEdit_ftp_host.setEnabled(signal)
        self.lineEdit_ftp_user.setEnabled(signal)
        self.lineEdit_ftp_pas.setEnabled(signal)
        self.lineEdit_cam_name.setEnabled(signal)
        self.pushButton_days.setEnabled(signal)
        self.pushButton_cameras_list.setEnabled(signal)

    def sending_status_message_getdays(self, text):
        self.label_connection.setText(text)

    def sending_message_getdays(self, text):
        self.label_sd_days.setText(text)

    def sending_message_days(self, days_list):
        self.days = days_list

    def sending_message_cameras(self, cam_list):
        self.cameras = cam_list

    def run_GetDays(self):
        self.thread_3 = QThread()
        self.worker_3 = GetDays(main_window=self)
        self.worker_3.moveToThread(self.thread_3)
        self.thread_3.started.connect(self.worker_3.run)
        self.worker_3.finished.connect(self.thread_3.quit)
        self.worker_3.finished.connect(self.worker_3.deleteLater)
        self.thread_3.finished.connect(self.thread_3.deleteLater)
        self.worker_3.enable_disable_ui.connect(self.disable_enable_ui)
        self.worker_3.start_enable_ui.connect(self.start_enable_ui)
        self.worker_3.status_message.connect(self.sending_status_message_getdays)
        self.worker_3.message.connect(self.sending_message_getdays)
        self.worker_3.days_message.connect(self.sending_message_days)
        self.worker_3.cameras_message.connect(self.sending_message_cameras)
        self.thread_3.start()

    # A slot for a button that connects to the camera and parses its SD card.
    # This is a fast task, so it is executed in the main thread.
    def button_days_clicked(self):
        # Polling user input fields
        self.label_connection.setText('')

        self.ftp_host = self.lineEdit_ftp_host.text()
        self.ftp_user = self.lineEdit_ftp_user.text()
        self.ftp_pas = self.lineEdit_ftp_pas.text()
        self.cam_name = self.lineEdit_cam_name.text()

        self.progressBar_days.setValue(0)
        self.progressBar_videos.setValue(0)
        self.label_out.setText('')
        self.run_GetDays()

    def button_days_list_clicked(self):
        self.days_list_window.setWindowTitle('Days')
        self.days_list_window.setText(str(self.days))
        self.days_list_window.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.days_list_window.setGeometry(800, 200, 0, 0)
        self.days_list_window.exec_()

    def button_cameras_list_clicked(self):
        self.cameras_list_window.setWindowTitle('Cameras')
        self.cameras_list_window.setText(str(self.cameras))
        self.cameras_list_window.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.cameras_list_window.setGeometry(800, 200, 0, 0)
        self.cameras_list_window.exec_()

    # The ability for the user to connect a second time range
    def second_time_range_open(self):
        if self.radioButton_str.isChecked():
            self.lineEdit_str_from.setEnabled(True)
            self.lineEdit_str_from_min.setEnabled(True)
            self.lineEdit_str_to.setEnabled(True)
            self.lineEdit_str_to_min.setEnabled(True)
        else:
            self.lineEdit_str_from.setEnabled(False)
            self.lineEdit_str_from_min.setEnabled(False)
            self.lineEdit_str_to.setEnabled(False)
            self.lineEdit_str_to_min.setEnabled(False)

    def refresh_open(self):
        if self.radioButton_refresh.isChecked():
            self.lineEdit_day_start.setEnabled(False)
            self.lineEdit_day_end.setEnabled(False)
            volume_of_deleting = 'все'
        else:
            self.lineEdit_day_start.setEnabled(True)
            self.lineEdit_day_end.setEnabled(True)
            volume_of_deleting = 'выбранные'
        self.pushButton_delete_from_ftp.setText(f'{self.button_delete_text} {volume_of_deleting}')

    def auto_open(self):
        if self.radioButton_auto.isChecked():
            self.radioButton_refresh.setChecked(True)
            self.pushButton_days.setEnabled(False)
            self.pushButton_days_list.setEnabled(False)
            self.pushButton_cameras_list.setEnabled(False)
            self.pushButton_total.setEnabled(False)
            self.pushButton_delete_from_ftp.setEnabled(False)
            self.radioButton_refresh.setEnabled(False)
            self.radioButton_str.setEnabled(False)
            self.radioButton_alarm.setEnabled(False)
            self.radioButton_images.setEnabled(False)
            self.radioButton_with_deletion.setEnabled(False)
            self.lineEdit_ftp_host.setEnabled(False)
            self.lineEdit_ftp_user.setEnabled(False)
            self.lineEdit_ftp_pas.setEnabled(False)
            self.lineEdit_day_start.setEnabled(False)
            self.lineEdit_day_end.setEnabled(False)
            self.lineEdit_ftr_from.setEnabled(False)
            self.lineEdit_ftr_from_min.setEnabled(False)
            self.lineEdit_ftr_to.setEnabled(False)
            self.lineEdit_ftr_to_min.setEnabled(False)
        else:
            self.pushButton_days.setEnabled(True)
            self.pushButton_days_list.setEnabled(True)
            self.pushButton_cameras_list.setEnabled(True)
            self.pushButton_total.setEnabled(True)
            self.pushButton_delete_from_ftp.setEnabled(True)

            self.radioButton_refresh.setEnabled(True)
            self.radioButton_str.setEnabled(True)
            self.radioButton_alarm.setEnabled(True)
            self.radioButton_images.setEnabled(True)
            self.radioButton_with_deletion.setEnabled(True)

            self.lineEdit_ftp_host.setEnabled(True)
            self.lineEdit_ftp_user.setEnabled(True)
            self.lineEdit_ftp_pas.setEnabled(True)
            self.lineEdit_cam_name.setEnabled(True)

            self.lineEdit_day_start.setEnabled(False)
            self.lineEdit_day_end.setEnabled(False)
            self.lineEdit_ftr_from.setEnabled(True)
            self.lineEdit_ftr_from_min.setEnabled(True)
            self.lineEdit_ftr_to.setEnabled(True)
            self.lineEdit_ftr_to_min.setEnabled(True)

    def disable_enable_ui(self, signal):
        self.pushButton_save_settings.setEnabled(signal)
        self.pushButton_days.setEnabled(signal)
        self.pushButton_days_list.setEnabled(signal)
        self.pushButton_cameras_list.setEnabled(signal)
        self.pushButton_total.setEnabled(signal)
        self.pushButton_parse.setEnabled(signal)
        self.pushButton_delete_from_ftp.setEnabled(signal)

        self.radioButton_refresh.setEnabled(signal)
        self.radioButton_str.setEnabled(signal)
        self.radioButton_alarm.setEnabled(signal)
        self.radioButton_images.setEnabled(signal)
        self.radioButton_auto.setEnabled(signal)
        self.radioButton_with_deletion.setEnabled(signal)

        self.lineEdit_ftp_host.setEnabled(signal)
        self.lineEdit_ftp_user.setEnabled(signal)
        self.lineEdit_ftp_pas.setEnabled(signal)
        self.lineEdit_cam_name.setEnabled(signal)

        self.lineEdit_day_start.setEnabled(signal)
        self.lineEdit_day_end.setEnabled(signal)
        self.lineEdit_ftr_from.setEnabled(signal)
        self.lineEdit_ftr_from_min.setEnabled(signal)
        self.lineEdit_ftr_to.setEnabled(signal)
        self.lineEdit_ftr_to_min.setEnabled(signal)

        if signal:
            self.second_time_range_open()
            self.refresh_open()

        else:
            self.lineEdit_day_start.setEnabled(False)
            self.lineEdit_day_end.setEnabled(False)
            self.lineEdit_str_from.setEnabled(False)
            self.lineEdit_str_from_min.setEnabled(False)
            self.lineEdit_str_to.setEnabled(False)
            self.lineEdit_str_to_min.setEnabled(False)
            self.radioButton_alarm.setEnabled(False)

            self.radioButton_images.setEnabled(False)
            self.radioButton_auto.setEnabled(False)

    def load_hiFTPconfig(self):
        app_name = get_app_name()
        hiFTPconfig = []
        if os.path.exists(os.path.join(self.cwd_path, f'{app_name}_hiFTPconfig.dat')):
            with open(os.path.join(self.cwd_path, f'{app_name}_hiFTPconfig.dat'), 'rb') as data_file:
                hiFTPconfig = pickle.load(data_file)
        return hiFTPconfig

    def save_hiFTPconfig(self, hiFTPconfig):
        app_name = get_app_name()
        with open(os.path.join(self.cwd_path, f'{app_name}_hiFTPconfig.dat'), "wb") as data_file:
            pickle.dump(hiFTPconfig, data_file)

    def button_save_settings_clicked(self):
        hiFTPconfig = []
        hiFTPconfig.append({
            'ftp_host': self.lineEdit_ftp_host.text(),
            'ftp_user': self.lineEdit_ftp_user.text(),
            'ftp_pas': self.lineEdit_ftp_pas.text(),
            'cam_name': self.lineEdit_cam_name.text(),
            'day_start': self.lineEdit_day_start.text(),
            'day_end': self.lineEdit_day_end.text(),
            'rb_refresh': self.radioButton_refresh.isChecked(),
            'ftr_from': self.lineEdit_ftr_from.text(),
            'ftr_from_min': self.lineEdit_ftr_from_min.text(),
            'ftr_to': self.lineEdit_ftr_to.text(),
            'ftr_to_min': self.lineEdit_ftr_to_min.text(),
            'rb_str': self.radioButton_str.isChecked(),
            'str_from': self.lineEdit_str_from.text(),
            'str_from_min': self.lineEdit_str_from_min.text(),
            'str_to': self.lineEdit_str_to.text(),
            'str_to_min': self.lineEdit_str_to_min.text(),
            'rb_alarm': self.radioButton_alarm.isChecked(),
            'rb_images': self.radioButton_images.isChecked(),
            'with_deletion': self.radioButton_with_deletion.isChecked(),
            'rb_auto': self.radioButton_auto.isChecked()
        })
        self.save_hiFTPconfig(hiFTPconfig)
        self.label_wishes_thanks.setText('<FONT COLOR=#008000>Настройки сохранены</FONT>')

    # The following 3 functions belong to the first working thread to evaluate the user range
    def set_progress_bar_total_days_start(self, progress_days_max):
        self.progressBar_total.setMaximum(progress_days_max)
        self.progressBar_total.setValue(0)

    def set_progress_bar_total_days_process(self, value_days):
        self.progressBar_total.setValue(value_days)

    # The signal slot of the first working thread for transmitting
    # summary information about the selected time range
    def sending_message_total(self, text_total):
        self.label_total.setText(text_total)
        self.label_wishes_thanks.setText(' ')

    # The function of starting the first working thread
    # to evaluate files in the range selected by the user
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
        self.worker.progress_days_start.connect(self.set_progress_bar_total_days_start)
        self.worker.progress_days_process.connect(self.set_progress_bar_total_days_process)
        self.worker.message.connect(self.sending_message_total)
        # Step 5: Start the thread
        self.thread.start()

    def check_hour_input(self, input):
        if len(input) < 2:
            input = '0' + input
        return input

    # Processing the button click to start the first working thread to evaluate the user range
    def button_total_clicked(self):
        self.ftp_host = self.lineEdit_ftp_host.text()
        self.ftp_user = self.lineEdit_ftp_user.text()
        self.ftp_pas = self.lineEdit_ftp_pas.text()
        self.cam_name = self.lineEdit_cam_name.text()

        self.day_start = self.lineEdit_day_start.text()
        self.day_end = self.lineEdit_day_end.text()
        self.ftr_from = (self.check_hour_input(self.lineEdit_ftr_from.text()) +
                         self.check_hour_input(self.lineEdit_ftr_from_min.text()) + '00')
        self.ftr_to = (self.check_hour_input(self.lineEdit_ftr_to.text()) +
                       self.check_hour_input(self.lineEdit_ftr_to_min.text()) + '00')
        self.str_from = (self.check_hour_input(self.lineEdit_str_from.text()) +
                         self.check_hour_input(self.lineEdit_str_from_min.text()) + '00')
        self.str_to = (self.check_hour_input(self.lineEdit_str_to.text()) +
                       self.check_hour_input(self.lineEdit_str_to_min.text()) + '00')
        self.progressBar_days.setValue(0)
        self.progressBar_videos.setValue(0)
        self.progressBar_pb_delete_from_ftp.setValue(0)
        self.label_out.setText('')
        self.label_wishes_thanks.setText('')
        self.run_EstimateThread()

    # The following 5 functions belong to the second working thread to videos downloading
    def set_progress_bar_videos_start(self, progress_days_max):
        self.progressBar_videos.setMaximum(progress_days_max)
        self.progressBar_videos.setValue(0)

    def set_progress_bar_videos_process(self, value_videos):
        self.progressBar_videos.setValue(value_videos)

    def set_progress_bar_days_start(self, progress_days_max):
        self.progressBar_days.setMaximum(progress_days_max)
        self.progressBar_days.setValue(0)

    def set_progress_bar_days_process(self, value_days):
        self.progressBar_days.setValue(value_days)

    def sending_message_parser(self, message):
        self.label_out.setText(message)
        self.label_wishes_thanks.setText(' ')

    # The function of starting the second working thread
    # to videos downloading in the range selected by the user
    def run_ParseThread(self):
        self.thread_2 = QThread()
        self.worker_2 = ParseThread(main_window=self)
        self.worker_2.moveToThread(self.thread_2)
        self.thread_2.started.connect(self.worker_2.run)
        self.worker_2.finished.connect(self.thread_2.quit)
        self.worker_2.finished.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.enable_disable_ui.connect(self.disable_enable_ui)
        self.worker_2.progress_videos_start.connect(self.set_progress_bar_videos_start)
        self.worker_2.progress_videos_process.connect(self.set_progress_bar_videos_process)
        self.worker_2.progress_days_start.connect(self.set_progress_bar_days_start)
        self.worker_2.progress_days_process.connect(self.set_progress_bar_days_process)
        self.worker_2.message.connect(self.sending_message_parser)
        self.thread_2.start()

    # Processing the button click to start the second working thread
    def button_parse_clicked(self):
        self.ftp_host = self.lineEdit_ftp_host.text()
        self.ftp_user = self.lineEdit_ftp_user.text()
        self.ftp_pas = self.lineEdit_ftp_pas.text()
        self.cam_name = self.lineEdit_cam_name.text()

        self.day_start = self.lineEdit_day_start.text()
        self.day_end = self.lineEdit_day_end.text()
        self.ftr_from = (self.check_hour_input(self.lineEdit_ftr_from.text()) +
                         self.check_hour_input(self.lineEdit_ftr_from_min.text()) + '00')
        self.ftr_to = (self.check_hour_input(self.lineEdit_ftr_to.text()) +
                       self.check_hour_input(self.lineEdit_ftr_to_min.text()) + '00')
        self.str_from = (self.check_hour_input(self.lineEdit_str_from.text()) +
                         self.check_hour_input(self.lineEdit_str_from_min.text()) + '00')
        self.str_to = (self.check_hour_input(self.lineEdit_str_to.text()) +
                       self.check_hour_input(self.lineEdit_str_to_min.text()) + '00')
        self.progressBar_pb_delete_from_ftp.setValue(0)
        self.label_wishes_thanks.setText('')
        self.run_ParseThread()

    def set_progress_bar_delete_start(self, progress_days_max):
        self.progressBar_pb_delete_from_ftp.setMaximum(progress_days_max)
        self.progressBar_pb_delete_from_ftp.setValue(0)

    def set_progress_bar_delete_process(self, value_days):
        self.progressBar_pb_delete_from_ftp.setValue(value_days)

    def sending_message_delete(self, text_total):
        self.label_wishes_thanks.setText(text_total)

    def run_DeleteThread(self):
        # Step 1: Create a QThread object
        self.thread_4 = QThread()
        # Step 2: Create a worker object
        self.worker_4 = DeleteThread(main_window=self)
        # Step 3: Move worker to the thread
        self.worker_4.moveToThread(self.thread_4)
        # Step 4: Connect signals and slots
        self.thread_4.started.connect(self.worker_4.run)
        self.worker_4.finished.connect(self.thread_4.quit)
        self.worker_4.finished.connect(self.worker_4.deleteLater)
        self.thread_4.finished.connect(self.thread_4.deleteLater)
        self.worker_4.enable_disable_ui.connect(self.disable_enable_ui)
        self.worker_4.progress_days_start.connect(self.set_progress_bar_delete_start)
        self.worker_4.progress_days_process.connect(self.set_progress_bar_delete_process)
        self.worker_4.message.connect(self.sending_message_delete)
        # Step 5: Start the thread
        self.thread_4.start()

    def button_delete_from_ftp_clicked(self):
        self.ftp_host = self.lineEdit_ftp_host.text()
        self.ftp_user = self.lineEdit_ftp_user.text()
        self.ftp_pas = self.lineEdit_ftp_pas.text()
        self.cam_name = self.lineEdit_cam_name.text()

        self.day_start = self.lineEdit_day_start.text()
        self.day_end = self.lineEdit_day_end.text()
        self.ftr_from = (self.check_hour_input(self.lineEdit_ftr_from.text()) +
                         self.check_hour_input(self.lineEdit_ftr_from_min.text()) + '00')
        self.ftr_to = (self.check_hour_input(self.lineEdit_ftr_to.text()) +
                       self.check_hour_input(self.lineEdit_ftr_to_min.text()) + '00')
        self.str_from = (self.check_hour_input(self.lineEdit_str_from.text()) +
                         self.check_hour_input(self.lineEdit_str_from_min.text()) + '00')
        self.str_to = (self.check_hour_input(self.lineEdit_str_to.text()) +
                       self.check_hour_input(self.lineEdit_str_to_min.text()) + '00')
        self.progressBar_days.setValue(0)
        self.progressBar_videos.setValue(0)
        self.label_out.setText('')
        self.run_DeleteThread()

    # Feedback button
    def button_wishes_clicked(self):
        email = f'<FONT COLOR=#b96902>{CONTACT_EMAIL}</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)

    # Button for donations
    def button_thanks_clicked(self):
        tel = f'<FONT COLOR=#b96902>{CONTACT_CARD}</FONT>'
        thanks_text = 'Благодарность на карту Сбербанк: '
        self.label_wishes_thanks.setText(thanks_text + tel + ' Aleksey')

    def start(self):
        hiFTPconfig = self.load_hiFTPconfig()
        if len(hiFTPconfig) != 0:
            ftp_host = self.load_hiFTPconfig()[0]['ftp_host']
            self.lineEdit_ftp_host.setText(f'{ftp_host}')
            ftp_user = self.load_hiFTPconfig()[0]['ftp_user']
            self.lineEdit_ftp_user.setText(f'{ftp_user}')
            ftp_pas = self.load_hiFTPconfig()[0]['ftp_pas']
            self.lineEdit_ftp_pas.setText(f'{ftp_pas}')
            cam_name = self.load_hiFTPconfig()[0]['cam_name']
            self.lineEdit_cam_name.setText(f'{cam_name}')
            day_start = self.load_hiFTPconfig()[0]['day_start']
            self.lineEdit_day_start.setText(f'{day_start}')
            day_end =  self.load_hiFTPconfig()[0]['day_end']
            self.lineEdit_day_end.setText(f'{day_end}')
            rb_refresh = self.load_hiFTPconfig()[0]['rb_refresh']
            self.radioButton_refresh.setChecked(rb_refresh)
            ftr_from = self.load_hiFTPconfig()[0]['ftr_from']
            self.lineEdit_ftr_from.setText(f'{ftr_from}')
            ftr_from_min = self.load_hiFTPconfig()[0]['ftr_from_min']
            self.lineEdit_ftr_from_min.setText(f'{ftr_from_min}')
            ftr_to = self.load_hiFTPconfig()[0]['ftr_to']
            self.lineEdit_ftr_to.setText(f'{ftr_to}')
            ftr_to_min = self.load_hiFTPconfig()[0]['ftr_to_min']
            self.lineEdit_ftr_to_min.setText(f'{ftr_to_min}')
            rb_str = self.load_hiFTPconfig()[0]['rb_str']
            self.radioButton_str.setChecked(rb_str)
            str_from = self.load_hiFTPconfig()[0]['str_from']
            self.lineEdit_str_from.setText(f'{str_from}')
            str_from_min = self.load_hiFTPconfig()[0]['str_from_min']
            self.lineEdit_str_from_min.setText(f'{str_from_min}')
            str_to = self.load_hiFTPconfig()[0]['str_to']
            self.lineEdit_str_to.setText(f'{str_to}')
            str_to_min = self.load_hiFTPconfig()[0]['str_to_min']
            self.lineEdit_str_to_min.setText(f'{str_to_min}')
            rb_alarm = self.load_hiFTPconfig()[0]['rb_alarm']
            self.radioButton_alarm.setChecked(rb_alarm)
            rb_images = self.load_hiFTPconfig()[0]['rb_images']
            self.radioButton_images.setChecked(rb_images)
            rb_auto = self.load_hiFTPconfig()[0]['rb_auto']
            self.radioButton_auto.setChecked(rb_auto)
            with_deletion = self.load_hiFTPconfig()[0]['with_deletion']
            self.radioButton_with_deletion.setChecked(with_deletion)
            self.button_days_clicked()
            if self.radioButton_auto.isChecked():
                self.button_parse_clicked()


def main():
    app = QApplication(sys.argv)
    UIWindow = UI()
    UIWindow.start()
    app.exec_()


if __name__ == '__main__':
    main()
