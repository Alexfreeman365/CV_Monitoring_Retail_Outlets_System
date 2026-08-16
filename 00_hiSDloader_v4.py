import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import (QDialog,
                             QApplication,
                             QLineEdit, QRadioButton,
                             QPushButton, QProgressBar,
                             QLabel, QMessageBox)
import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pickle
import telebot

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, log_event, cleanup_mei_folders, get_app_name
from utils.contacts import CONTACT_EMAIL, CONTACT_CARD

import atexit
atexit.register(cleanup_mei_folders)


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
        self.ip = self.main_window.ip
        self.lineEdit_cam_name = self.main_window.lineEdit_cam_name
        self.host_sd = self.main_window.host_sd
        self.day_start = self.main_window.day_start
        self.day_end = self.main_window.day_end
        self.host = self.main_window.host
        self.ftr_from = self.main_window.ftr_from
        self.ftr_to = self.main_window.ftr_to
        self.str_from = self.main_window.str_from
        self.str_to = self.main_window.str_to
        self.output_dir = self.main_window.output_dir
        self.days = []
        self.day_folders = []
        self.range_days_num = 0
        self.videos_num = 0
        self.day_videos_size = 0
        self.text_range_days_num = ''
        self.text_videos_num = ''
        self.text_day_videos_size = ''
        self.text_total = ''

    def run(self):
        # Function to get the entire range of days existing on the SD card
        def get_days():
            # Getting a html page in the SD section
            r = requests.get(self.host_sd)
            # Structuring a html page in the SD section
            soup = BeautifulSoup(r.content, 'html5lib')
            # Getting all links on a page using the 'a' tag
            day_links = soup.find_all('a')
            # Getting rows with days
            dirty_days = [link['href'] for link in day_links if any(map(str.isdigit, link['href']))]
            # Clearing rows to get days
            return [day.split('/')[2] for day in dirty_days if day.split('/')[2].isdigit()]

        # The Camhi storage system uses folders for each day.
        # If the first folder contains more than 200 videos,
        # then another one is created and so on.
        # This function defines these folders for one day.
        def get_day_folders(host_sd, day):
            r = requests.get(host_sd + day + '/')
            soup = BeautifulSoup(r.content, 'html5lib')
            day_folder_rows = soup.find_all('a')[4:]
            return [''.join(list(row)) for row in day_folder_rows if any(map(str.isdigit, ''.join(list(row))))]

        # Formation of a custom time range: a condition for the first hour range
        def time_condition_ftr(link):
            video_time_start = str(list(link)[0]).split('/')[4].split('_')[1]
            video_time_end = str(list(link)[0]).split('/')[4].split('_')[2].split('.')[0]
            time_condition = ((self.ftr_from <= video_time_start) & (video_time_end <= self.ftr_to))
            return time_condition

        def image_time_condition_ftr(link):
            image_time = str(list(link)[0]).split('/')[4].split('.')[0][7:13]
            time_condition = ((self.ftr_from <= image_time) & (image_time <= self.ftr_to))
            return time_condition

        # Formation of a custom time range: a condition for the second hour range
        def time_condition_str(link):
            video_time_start = str(list(link)[0]).split('/')[4].split('_')[1]
            video_time_end = str(list(link)[0]).split('/')[4].split('_')[2].split('.')[0]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= video_time_start) & (video_time_end <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def image_time_condition_str(link):
            image_time = str(list(link)[0]).split('/')[4].split('.')[0][7:13]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= image_time) & (image_time <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def alarm_condition(link):
            video_status = str(list(link)[0]).split('/')[4].split('_')[0][0]
            condition = video_status == 'A'
            return condition

        def plan_condition(link):
            video_status = str(list(link)[0]).split('/')[4].split('_')[0][0]
            condition = video_status == 'P'
            return condition

        def get_last_pc_day():
            if len(self.lineEdit_cam_name.text()) != 0:
                ip = self.lineEdit_cam_name.text()
            else:
                ip = self.ip.replace(':', '_')
            image_last_pc_day = '0'
            video_last_pc_day = '0'

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, ip + '_photos')
                if os.path.exists(image_path):
                    image_last_pc_day = os.listdir(image_path)[-1]

            if self.main_window.radioButton_plan.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
                if os.path.exists(video_path):
                    video_last_pc_day = os.listdir(video_path)[-1]

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
                if os.path.exists(video_path):
                    video_last_pc_day = os.listdir(video_path)[-1]

            if image_last_pc_day <= self.days[0]:
                image_last_pc_day = self.days[0]
            if video_last_pc_day <= self.days[0]:
                video_last_pc_day = self.days[0]

            return image_last_pc_day, video_last_pc_day

        # Getting summary information about the video in the selected time range
        def get_summary(image_day_start, video_day_start, image_day_end, video_day_end):
            self.progress_days_start.emit(len(self.days))
            # Pass through all days included in the selected range
            for day in self.days:

                # Defining folders for this day
                day_folders = get_day_folders(self.host_sd, day)
                day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                day_image_folders = [folder for folder in day_folders if folder[0] == 'i']

                if self.main_window.radioButton_images.isChecked():
                    if image_day_start <= day <= image_day_end:
                        for folder in day_image_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            # Unlike the 'a' tag, which points to links,
                            # the 'tr' tag shows an entire row of the table,
                            # which contains both a link to the file and its size.
                            links = soup.find_all('tr')
                            # Postponing only those lines that are included in our conditions
                            folder_video_links = [link for link in links[3:] if
                                                  (image_time_condition_ftr(link) | image_time_condition_str(link))]
                            # Allocating numbers with the size of each file,
                            # taking into account the fact that the file can have a dimension of kilobytes or megabytes.
                            for link in folder_video_links:
                                if 'k' in ''.join(list(link)[2]):
                                    self.day_videos_size += float((''.join(list(link)[2])).replace('k', '')) / 1024
                                else:
                                    self.day_videos_size += float((''.join(list(link)[2])).replace('M', ''))
                            self.videos_num += len(folder_video_links)

                if self.main_window.radioButton_plan.isChecked():
                    if video_day_start <= day <= video_day_end:
                        for folder in day_video_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            # Unlike the 'a' tag, which points to links,
                            # the 'tr' tag shows an entire row of the table,
                            # which contains both a link to the file and its size.
                            links = soup.find_all('tr')
                            # Postponing only those lines that are included in our conditions
                            folder_video_links = [link for link in links[3:] if
                                                  plan_condition(link) & (time_condition_ftr(link) |
                                                                          time_condition_str(link))]
                            # Setting the initial state of the counter,
                            # which counts the total size of files for each folder
                            # Allocating numbers with the size of each file,
                            # taking into account the fact that the file can have a dimension of kilobytes or megabytes.
                            for link in folder_video_links:
                                if 'k' in ''.join(list(link)[2]):
                                    self.day_videos_size += float((''.join(list(link)[2])).replace('k', '')) / 1024
                                else:
                                    self.day_videos_size += float((''.join(list(link)[2])).replace('M', ''))
                            self.videos_num += len(folder_video_links)

                if self.main_window.radioButton_alarm.isChecked():
                    if video_day_start <= day <= video_day_end:
                        for folder in day_video_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            # Unlike the 'a' tag, which points to links,
                            # the 'tr' tag shows an entire row of the table,
                            # which contains both a link to the file and its size.
                            links = soup.find_all('tr')
                            # Postponing only those lines that are included in our conditions
                            folder_video_links = [link for link in links[3:] if
                                                  alarm_condition(link) & (time_condition_ftr(link) |
                                                                           time_condition_str(link))]
                            # Setting the initial state of the counter,
                            # which counts the total size of files for each folder
                            # Allocating numbers with the size of each file,
                            # taking into account the fact that the file can have a dimension of kilobytes or megabytes.
                            for link in folder_video_links:
                                if 'k' in ''.join(list(link)[2]):
                                    self.day_videos_size += float(
                                        (''.join(list(link)[2])).replace('k', '')) / 1024
                                else:
                                    self.day_videos_size += float((''.join(list(link)[2])).replace('M', ''))
                            self.videos_num += len(folder_video_links)

                # Setting the progress bar execution sequence
                value_days = self.main_window.progressBar_total.value() + 1
                self.progress_days_process.emit(value_days)
            self.progress_days_process.emit(len(self.days))
            # Returns the number of videos and their size in the time range selected by the user
            return self.videos_num, round(self.day_videos_size)

        # Starting thread execution in the try-except error handling construct
        try:
            # Disable UI to prevent unauthorized actions
            self.enable_disable_ui.emit(False)
            # Sending a message to the user about the need to wait
            text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
            self.message.emit(text_wait)
            # Getting a list of existing days on the SD card
            self.days = get_days()

            if self.main_window.radioButton_refresh.isChecked():
                image_day_start, video_day_start = get_last_pc_day()
                image_day_end, video_day_end = self.days[-1], self.days[-1]

                # Getting the number of days in the selected range by the user
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
            self.videos_num, self.day_videos_size = get_summary(image_day_start, video_day_start,
                                                                image_day_end, video_day_end)
            text_days_num = '<FONT COLOR=#008000>{}</FONT>'.format(self.range_days_num)
            text_videos_num = '<FONT COLOR=#008000>{}</FONT>'.format(self.videos_num)
            text_size = '<FONT COLOR=#008000>{}Mb</FONT>'.format(self.day_videos_size)
            text_time = '<FONT COLOR=#008000>~{}мин</FONT>'.format(self.day_videos_size // 500)
            text_total = ('Дни:' + text_days_num + ' Кол-во:' + text_videos_num + ' Размер:' + text_size +
                          ' Лок_время_скач.:' + text_time)
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
        self.ip = self.main_window.ip
        self.host_sd = self.main_window.host_sd
        self.day_start = self.main_window.day_start
        self.day_end = self.main_window.day_end
        self.host = self.main_window.host
        self.ftr_from = self.main_window.ftr_from
        self.ftr_to = self.main_window.ftr_to
        self.str_from = self.main_window.str_from
        self.str_to = self.main_window.str_to
        self.output_dir = self.main_window.output_dir
        self.days = []
        self.image_links_dict = {}
        self.video_links_dict = {}
        self.lineEdit_cam_name = self.main_window.lineEdit_cam_name
        self.lineEdit_token = self.main_window.lineEdit_token
        self.lineEdit_chat_id = self.main_window.lineEdit_chat_id
        self.TOKEN = self.lineEdit_token.text()
        self.chat_id = (self.lineEdit_chat_id.text())
        if self.TOKEN:
            self.bot = telebot.TeleBot(self.TOKEN, parse_mode=None)
        self.max_retries = 100  # Maximum number of reconnection attempts
        self.app_name = get_app_name()

    def run(self):
        # The following 5 functions are similar
        # and described in detail in the first working thread
        def get_days():
            r = requests.get(self.host_sd)
            soup = BeautifulSoup(r.content, 'html5lib')
            day_links = soup.find_all('a')
            dirty_days = [link['href'] for link in day_links if any(map(str.isdigit, link['href']))]
            return [day.split('/')[2] for day in dirty_days if day.split('/')[2].isdigit()]

        def get_day_folders(host_sd, day):
            r = requests.get(host_sd + day + '/')
            soup = BeautifulSoup(r.content, 'html5lib')
            day_folder_rows = soup.find_all('a')[4:]
            return [''.join(list(row)) for row in day_folder_rows if any(map(str.isdigit, ''.join(list(row))))]

        def time_condition_ftr(link):
            video_time = link['href'].split('/')[4].split('.')[0].split('_')
            time_condition = ((self.ftr_from <= video_time[1]) & (video_time[2] <= self.ftr_to))
            return time_condition

        def image_time_condition_ftr(link):
            image_time = link['href'].split('/')[4].split('.')[0][7:13]
            time_condition = ((self.ftr_from <= image_time) & (image_time <= self.ftr_to))
            return time_condition

        def time_condition_str(link):
            video_time = link['href'].split('/')[4].split('.')[0].split('_')
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= video_time[1]) & (video_time[2] <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def image_time_condition_str(link):
            image_time = link['href'].split('/')[4].split('.')[0][7:13]
            if self.main_window.radioButton_str.isChecked():
                time_condition = ((self.str_from <= image_time) & (image_time <= self.str_to))
            else:
                time_condition = False
            return time_condition

        def alarm_condition(link):
            condition = (link['href'].endswith(('264', '265')) &
                         link['href'].split('/')[4].split('.')[0].split('_')[0].startswith('A'))
            return condition

        def plan_condition(link):
            condition = (link['href'].endswith(('264', '265')) &
                         link['href'].split('/')[4].split('.')[0].split('_')[0].startswith('P'))
            return condition

        def get_last_pc_day():
            if len(self.lineEdit_cam_name.text()) != 0:
                ip = self.lineEdit_cam_name.text()
            else:
                ip = self.ip.replace(':', '_')
            image_last_pc_day = '0'
            video_last_pc_day = '0'

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, ip + '_photos')
                if os.path.exists(image_path):
                    image_last_pc_day = os.listdir(image_path)[-1]

            if self.main_window.radioButton_plan.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
                if os.path.exists(video_path):
                    video_last_pc_day = os.listdir(video_path)[-1]

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
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
                        day_folders = get_day_folders(self.host_sd, day)
                        day_image_folders = [folder for folder in day_folders if folder[0] == 'i']
                        for folder in day_image_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            links = soup.find_all('a')
                            folder_image_links = [self.host + link['href']
                                                  for link in links[4:]
                                                  if (image_time_condition_ftr(link) | image_time_condition_str(link))]
                            day_image_links += folder_image_links
                        if len(day_image_links) > 0:
                            self.image_links_dict[day] = day_image_links

                if self.main_window.radioButton_plan.isChecked():
                    if video_day_start <= day <= video_day_end:
                        day_folders = get_day_folders(self.host_sd, day)
                        day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                        for folder in day_video_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            links = soup.find_all('a')
                            folder_video_links = [self.host + link['href']
                                                  for link in links[4:]
                                                  if plan_condition(link) & (time_condition_ftr(link)
                                                                             | time_condition_str(link))]
                            day_video_links += folder_video_links
                        if len(day_video_links) > 0:
                            self.video_links_dict[day] = day_video_links

                if self.main_window.radioButton_alarm.isChecked():
                    if video_day_start <= day <= video_day_end:
                        day_folders = get_day_folders(self.host_sd, day)
                        day_video_folders = [folder for folder in day_folders if folder[0] == 'r']
                        for folder in day_video_folders:
                            r = requests.get(self.host_sd + day + '/' + folder)
                            soup = BeautifulSoup(r.content, 'html5lib')
                            links = soup.find_all('a')
                            folder_video_links = [self.host + link['href']
                                                  for link in links[4:]
                                                  if alarm_condition(link) & (time_condition_ftr(link)
                                                                              | time_condition_str(link))]
                            day_video_links += folder_video_links
                        if len(day_video_links) > 0:
                            self.video_links_dict[day] = day_video_links

            return self.image_links_dict, self.video_links_dict

        def get_last_day_filenames():
            if len(self.lineEdit_cam_name.text()) != 0:
                ip = self.lineEdit_cam_name.text()
            else:
                ip = self.ip.replace(':', '_')
            image_last_pc_day_filenames = []
            video_last_pc_day_filenames = []

            if self.main_window.radioButton_images.isChecked():
                image_path = os.path.join(self.output_dir, ip + '_photos')
                if os.path.exists(image_path):
                    try:
                        last_day = os.listdir(image_path)[-1]
                        if os.path.exists(os.path.join(image_path, last_day)):
                            image_last_pc_day_filenames = os.listdir(os.path.join(image_path, last_day))
                    except:
                        pass

            if self.main_window.radioButton_plan.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
                if os.path.exists(video_path):
                    try:
                        last_day = os.listdir(video_path)[-1]
                        if os.path.exists(os.path.join(video_path, last_day)):
                            video_last_pc_day_filenames = os.listdir(os.path.join(video_path, last_day))
                    except:
                        pass

            if self.main_window.radioButton_alarm.isChecked():
                video_path = os.path.join(self.output_dir, ip + '_videos')
                if os.path.exists(video_path):
                    try:
                        last_day = os.listdir(video_path)[-1]
                        if os.path.exists(os.path.join(video_path, last_day)):
                            video_last_pc_day_filenames = os.listdir(os.path.join(video_path, last_day))
                    except:
                        pass

            return image_last_pc_day_filenames, video_last_pc_day_filenames

        # A function that downloads videos from the received dictionary
        # from the previous function with the creation of a file structure.
        def download_series(links_dict_):
            # Creating a folder with the name of the camera's IP address.
            if len(self.lineEdit_cam_name.text()) != 0:
                ip = self.lineEdit_cam_name.text()
            else:
                ip = self.ip.replace(':', '_')

            if links_dict_ == self.image_links_dict:
                file_type = '_photos'
                if os.path.exists(self.main_window.output_dir + ip + file_type):
                    pass
                else:
                    if len(self.image_links_dict) != 0:
                        os.mkdir(self.main_window.output_dir + ip + file_type)
            else:
                file_type = '_videos'
                if os.path.exists(self.main_window.output_dir + ip + file_type):
                    pass
                else:
                    if len(self.video_links_dict) != 0:
                        os.mkdir(self.main_window.output_dir + ip + file_type)

            image_last_pc_day_filenames, video_last_pc_day_filenames = get_last_day_filenames()

            # A passage for each day from the dictionary to get links to the video
            self.progress_days_start.emit(len(links_dict_))
            self.progress_videos_start.emit(10)
            for day in links_dict_.keys():
                # Creating a folder with the name of the day.
                if os.path.exists(os.path.join(self.main_window.output_dir, ip + file_type, day)):
                    pass  # shutil.rmtree(self.output_dir + day)
                else:
                    os.mkdir(os.path.join(self.main_window.output_dir, ip + file_type, day))

                # Getting a list of links for the current day
                links = links_dict_[day]
                # Determining the number of links and
                # setting the initial state of the progress bar for the videos
                self.progress_videos_start.emit(len(links))
                # Getting each link from the list
                for link in links:
                    # Getting a title for a future video
                    file_line = link.split('/')[-1]
                    # Moving the video status to the end of the title for
                    # the correct sorting of files by the operating system.
                    file_title = file_line.split('.')[0]
                    file_extension = file_line.split('.')[1]
                    file_status = file_line[0]
                    if file_type == '_photos':
                        file_name = file_title[1:] + '.' + file_extension
                        if file_name not in image_last_pc_day_filenames:
                            # Create response object
                            r = requests.get(link, stream=True)
                            # Creating a directory and downloading videos to it in 1024*1024 chunks
                            with open(os.path.join(self.main_window.output_dir, ip + file_type, day, file_name),
                                      'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024 * 1024):
                                    if chunk:
                                        f.write(chunk)
                    if file_type == '_videos':
                        file_name = file_title[1:] + '_' + file_status + '.' + file_extension
                        if file_name not in video_last_pc_day_filenames:
                            # Create response object
                            r = requests.get(link, stream=True)
                            # Creating a directory and downloading videos to it in 1024*1024 chunks
                            with open(os.path.join(self.main_window.output_dir, ip + file_type, day, file_name),
                                      'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024 * 1024):
                                    if chunk:
                                        f.write(chunk)
                    # Updating the progress bar for videos
                    count_progress = self.main_window.progressBar_videos.value() + 1
                    self.progress_videos_process.emit(count_progress)
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

        def attempt_download(links_dict_):
            for attempt in range(self.max_retries):
                try:
                    download_series(links_dict_)
                    return True
                except Exception as e:
                    log_event(os.getcwd(), self.app_name, self.lineEdit_cam_name,
                              f'Error: {e}. Reconnect attempt: {attempt}')
                    if attempt < self.max_retries - 1:
                        time.sleep(5)  # Pause before trying again
                        continue
                    return False

        # Starting thread execution in the try-except error handling construct
        # The structure is similar to the launch of the first working thread.
        # For a detailed description, see there.
        try:
            # Disable UI to prevent unauthorized actions
            self.enable_disable_ui.emit(False)
            # Sending a message to the user about the need to wait
            text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
            self.message.emit(text_wait)
            # Getting a list of existing days on the SD card
            self.days = get_days()

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
                attempt_download(self.image_links_dict)
            if len(self.video_links_dict) != 0:
                attempt_download(self.video_links_dict)

            text_done = '<FONT COLOR=#008000>Выполнено!</FONT>'
            self.message.emit(text_done)
            self.enable_disable_ui.emit(True)
        except:
            self.enable_disable_ui.emit(True)
            text_error = '<FONT COLOR=#f4320c>Проблемы со скачиванием. ' \
                         'Попробуйте проверить ваш промежуток времени.</FONT>'
            self.message.emit(text_error)

        if self.main_window.radioButton_auto.isChecked():
            self.ftr_from = self.main_window.ftr_from
            self.ftr_to = self.main_window.ftr_to
            first_time_bot_notification = 0
            while self.main_window.radioButton_auto.isChecked():
                try:
                    # Disable UI to prevent unauthorized actions
                    self.enable_disable_ui.emit(False)
                    # Sending a message to the user about the need to wait
                    text_wait = '<FONT COLOR=#02a8ab>-=:АВТО_ОБНОВЛЕНИЕ_АРХИВА:=-</FONT>'
                    self.message.emit(text_wait)
                    # Getting a list of existing days on the SD card
                    self.days = get_days()

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
                        success = attempt_download(self.image_links_dict)
                        if not success:
                            time.sleep(10)
                    if len(self.video_links_dict) != 0:
                        success = attempt_download(self.video_links_dict)
                        if not success:
                            time.sleep(10)

                    self.progress_days_start.emit(10)
                    self.progress_videos_start.emit(10)
                    self.enable_disable_ui.emit(True)
                except:
                    self.enable_disable_ui.emit(True)
                    text_error = '<FONT COLOR=#f4320c>Проблемы со скачиванием. ' \
                                 'Попробуйте проверить ваш промежуток времени.</FONT>'
                    self.message.emit(text_error)
                    if first_time_bot_notification == 0:
                        try:
                            if len(self.lineEdit_cam_name.text()) != 0:
                                ip = self.lineEdit_cam_name.text()
                            else:
                                ip = self.ip.replace(':', '_')
                            if self.TOKEN:
                                self.bot.send_message(self.chat_id,
                                                      f'Внимание! Карта памяти камеры {ip} недоступна.')
                        except:
                            pass
                    first_time_bot_notification += 1
                self.ftr_from = (datetime.now() - timedelta(hours=0, minutes=20)).strftime("%H%M%S")
                self.str_from = (datetime.now() - timedelta(hours=0, minutes=20)).strftime("%H%M%S")
                time.sleep(5)

        self.finished.emit()


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

    # Receiving and saving variables from the main UI thread
    def __init__(self, main_window, parent=None):
        super(GetDays, self).__init__(parent)
        self.main_window = main_window
        self.host_sd = self.main_window.host_sd
        self.host = self.main_window.host
        self.days = []
        self.app_name = get_app_name()
        self.lineEdit_cam_name = self.main_window.lineEdit_cam_name
        self.lineEdit_token = self.main_window.lineEdit_token
        self.lineEdit_chat_id = self.main_window.lineEdit_chat_id

    def run(self):
        # Function for connecting to the camera and parsing the SD card
        # You can see detailed information at the beginning of the code in the first working thread.
        def get_days():
            r = requests.get(self.host_sd)
            soup = BeautifulSoup(r.content, 'html5lib')
            day_links = soup.find_all('a')
            dirty_days = [link['href'] for link in day_links if any(map(str.isdigit, link['href']))]
            return [day.split('/')[2] for day in dirty_days if day.split('/')[2].isdigit()]

        try:
            self.enable_disable_ui.emit(False)
            text_wait = '<FONT COLOR=#b96902>Ждите...</FONT>'
            self.message.emit(text_wait)
            self.days = get_days()
            text_success = '<FONT COLOR=#008000>Успешно</FONT>'
            self.status_message.emit(text_success)
            text_first_day = '<FONT COLOR=#008000>{}</FONT>'.format(self.days[0])
            text_last_day = '<FONT COLOR=#008000>{}</FONT>'.format(self.days[-1])
            text_day_amount = '<FONT COLOR=#008000>{}</FONT>'.format(str(len(self.days)))
            text_day_range = ('Первый_день:' + text_first_day + ' Последний_день:' +
                              text_last_day + ' Дни:' + text_day_amount)
            self.message.emit(text_day_range)
            self.days_message.emit(self.days)
            self.enable_disable_ui.emit(True)
        except Exception as e:
            log_event(os.getcwd(), self.app_name, self.lineEdit_cam_name, e)
            self.start_enable_ui.emit(True)
            text_error = '<FONT COLOR=#f4320c>Ошибка</FONT>'
            self.status_message.emit(text_error)
            self.message.emit('<FONT COLOR=#f4320c>Проблемы с доступом к камере. '
                              'Попробуйте проверить IP адрес, пароль и соединение.</FONT>')
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

        uic.loadUi(get_path('ui/00_hiSDloader_gui_v4.ui'), self)

        # Removing the windows hint button of the window,
        # which is formed by default in Qt designer and adding 'Minimize' btn
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowCloseButtonHint)

        # Define UI widgets
        self.lineEdit_ip_num = self.findChild(QLineEdit, 'ip_num')
        self.lineEdit_cam_name = self.findChild(QLineEdit, 'cam_name')
        self.lineEdit_pas = self.findChild(QLineEdit, 'lineEdit_2')
        self.label_connection = self.findChild(QLabel, 'label_19')
        self.pushButton_days = self.findChild(QPushButton, 'pushButton')
        self.pushButton_days_list = self.findChild(QPushButton, 'pushButton_3')
        self.days_list_window = QMessageBox()
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
        self.radioButton_plan = self.findChild(QRadioButton, 'radioButton_5')
        self.radioButton_images = self.findChild(QRadioButton, 'radioButton_2')
        self.pushButton_save_settings = self.findChild(QPushButton, 'save_settings')
        self.pushButton_total = self.findChild(QPushButton, 'pushButton_4')
        self.progressBar_total = self.findChild(QProgressBar, 'progressBar_3')
        self.radioButton_auto = self.findChild(QRadioButton, 'radioButton_4')
        self.label_total = self.findChild(QLabel, 'label_17')
        self.pushButton_parse = self.findChild(QPushButton, 'pushButton_2')
        self.progressBar_days = self.findChild(QProgressBar, 'progressBar')
        self.progressBar_videos = self.findChild(QProgressBar, 'progressBar_2')
        self.label_out = self.findChild(QLabel, 'label_7')
        self.lineEdit_token = self.findChild(QLineEdit, 'token')
        self.lineEdit_chat_id = self.findChild(QLineEdit, 'chat_id')
        self.label_wishes_thanks = self.findChild(QLabel, 'label_18')
        self.pushButton_wishes = self.findChild(QPushButton, 'pushButton_5')
        self.pushButton_thanks = self.findChild(QPushButton, 'pushButton_6')

        # Variables initialization
        self.ip = ''
        self.pas = ''
        self.host_sd = ''
        self.host = ''
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

        # Connecting button signals to their slots (functions)
        self.pushButton_days.clicked.connect(self.button_days_clicked)
        self.pushButton_days_list.clicked.connect(self.button_days_list_clicked)
        self.radioButton_refresh.toggled.connect(self.refresh_open)
        self.radioButton_auto.toggled.connect(self.auto_open)
        self.radioButton_str.toggled.connect(self.second_time_range_open)
        self.pushButton_save_settings.clicked.connect(self.button_save_settings_clicked)
        self.pushButton_total.clicked.connect(self.button_total_clicked)
        self.pushButton_parse.clicked.connect(self.button_parse_clicked)
        self.pushButton_wishes.clicked.connect(self.button_wishes_clicked)
        self.pushButton_thanks.clicked.connect(self.button_thanks_clicked)

        # Show the app
        self.show()

    # Checking and correcting user input for spaces
    def check_and_fix_spaces(self, row):
        if len(row) == 0:
            row = '123456Vn'
        if row[-1] == '\n':
            row = row[:-1]
        while row[-1] == ' ':
            row = row[:-1]
        while row[0] == ' ':
            row = row[1:]
        return row

    def start_enable_ui(self, signal):
        self.lineEdit_pas.setEnabled(signal)
        self.lineEdit_ip_num.setEnabled(signal)
        self.pushButton_days.setEnabled(signal)

    def sending_status_message_getdays(self, text):
        self.label_connection.setText(text)

    def sending_message_getdays(self, text):
        self.label_sd_days.setText(text)

    def sending_message_days(self, days_list):
        self.days = days_list

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
        self.thread_3.start()

    # A slot for a button that connects to the camera and parses its SD card.
    # This is a fast task, so it is executed in the main thread.
    def button_days_clicked(self):
        # Polling user input fields
        self.label_connection.setText('')
        self.pas = self.check_and_fix_spaces(self.lineEdit_pas.text())
        self.ip = self.lineEdit_ip_num.text()
        self.host = 'http://admin:' + self.pas + '@' + self.ip + ''
        self.host_sd = self.host + '/sd/'
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
        else:
            self.lineEdit_day_start.setEnabled(True)
            self.lineEdit_day_end.setEnabled(True)

    def auto_open(self):
        if self.radioButton_auto.isChecked():
            self.radioButton_refresh.setChecked(True)
            self.pushButton_days.setEnabled(False)
            self.pushButton_days_list.setEnabled(False)
            self.pushButton_total.setEnabled(False)
            self.radioButton_refresh.setEnabled(False)
            self.radioButton_str.setEnabled(False)
            self.radioButton_alarm.setEnabled(False)
            self.radioButton_plan.setEnabled(False)
            self.radioButton_images.setEnabled(False)
            self.lineEdit_pas.setEnabled(False)
            self.lineEdit_ip_num.setEnabled(False)
            self.lineEdit_day_start.setEnabled(False)
            self.lineEdit_day_end.setEnabled(False)
            self.lineEdit_ftr_from.setEnabled(False)
            self.lineEdit_ftr_from_min.setEnabled(False)
            self.lineEdit_ftr_to.setEnabled(False)
            self.lineEdit_ftr_to_min.setEnabled(False)
        else:
            self.pushButton_days.setEnabled(True)
            self.pushButton_days_list.setEnabled(True)
            self.pushButton_total.setEnabled(True)
            self.radioButton_refresh.setEnabled(True)
            self.radioButton_str.setEnabled(True)
            self.radioButton_alarm.setEnabled(True)
            self.radioButton_plan.setEnabled(True)
            self.radioButton_images.setEnabled(True)
            self.lineEdit_pas.setEnabled(True)
            self.lineEdit_ip_num.setEnabled(True)
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
        self.pushButton_total.setEnabled(signal)
        self.pushButton_parse.setEnabled(signal)
        self.radioButton_refresh.setEnabled(signal)
        self.radioButton_str.setEnabled(signal)
        self.radioButton_alarm.setEnabled(signal)
        self.radioButton_plan.setEnabled(signal)
        self.radioButton_images.setEnabled(signal)
        self.radioButton_auto.setEnabled(signal)
        self.lineEdit_pas.setEnabled(signal)
        self.lineEdit_ip_num.setEnabled(signal)
        self.lineEdit_cam_name.setEnabled(signal)
        self.lineEdit_day_start.setEnabled(signal)
        self.lineEdit_day_end.setEnabled(signal)
        self.lineEdit_ftr_from.setEnabled(signal)
        self.lineEdit_ftr_from_min.setEnabled(signal)
        self.lineEdit_ftr_to.setEnabled(signal)
        self.lineEdit_ftr_to_min.setEnabled(signal)
        self.lineEdit_token.setEnabled(signal)
        self.lineEdit_chat_id.setEnabled(signal)


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
            self.radioButton_plan.setEnabled(False)
            self.radioButton_images.setEnabled(False)
            self.radioButton_auto.setEnabled(False)

    def load_hiSDconfig(self):
        app_name = get_app_name()
        hiSDconfig = []
        if os.path.exists(os.path.join(self.cwd_path, f'{app_name}_hiSDconfig.dat')):
            with open(os.path.join(self.cwd_path, f'{app_name}_hiSDconfig.dat'), 'rb') as data_file:
                hiSDconfig = pickle.load(data_file)
        return hiSDconfig

    def save_hiSDconfig(self, hiSDconfig):
        app_name = get_app_name()
        with open(os.path.join(self.cwd_path, f'{app_name}_hiSDconfig.dat'), "wb") as data_file:
            pickle.dump(hiSDconfig, data_file)

    def button_save_settings_clicked(self):
        hiSDconfig = []
        hiSDconfig.append({
            'ip_num': self.lineEdit_ip_num.text(),
            'password': self.check_and_fix_spaces(self.lineEdit_pas.text()),
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
            'rb_plan': self.radioButton_plan.isChecked(),
            'rb_images': self.radioButton_images.isChecked(),
            'rb_auto': self.radioButton_auto.isChecked(),
            'token': self.lineEdit_token.text(),
            'chat_id': self.lineEdit_chat_id.text()
        })
        self.save_hiSDconfig(hiSDconfig)
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
        self.pas = self.check_and_fix_spaces(self.lineEdit_pas.text())
        self.ip = self.lineEdit_ip_num.text()
        self.host = 'http://admin:' + self.pas + '@' + self.ip + ''
        self.host_sd = self.host + '/sd/'
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
        self.pas = self.check_and_fix_spaces(self.lineEdit_pas.text())
        self.ip = self.lineEdit_ip_num.text()
        self.host = 'http://admin:' + self.pas + '@' + self.ip + ''
        self.host_sd = self.host + '/sd/'
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
        self.run_ParseThread()

    # Feedback button
    def button_wishes_clicked(self):
        email = f'<FONT COLOR=#b96902>{CONTACT_EMAIL}</FONT>'
        self.label_wishes_thanks.setText('E-mail: ' + email)

    # Button for donations
    def button_thanks_clicked(self):
        tel = f'<FONT COLOR=#b96902>{CONTACT_CARD}</FONT>'
        self.label_wishes_thanks.setText('Благодарность на карту Сбербанк: ' + tel + ' Алексей')

    def start(self):
        hiSDconfig = self.load_hiSDconfig()
        if len(hiSDconfig) != 0:
            ip_num = self.load_hiSDconfig()[0]['ip_num']
            self.lineEdit_ip_num.setText(f'{ip_num}')
            password = self.load_hiSDconfig()[0]['password']
            self.lineEdit_pas.setText(f'{password}')
            cam_name = self.load_hiSDconfig()[0]['cam_name']
            self.lineEdit_cam_name.setText(f'{cam_name}')
            day_start = self.load_hiSDconfig()[0]['day_start']
            self.lineEdit_day_start.setText(f'{day_start}')
            day_end =  self.load_hiSDconfig()[0]['day_end']
            self.lineEdit_day_end.setText(f'{day_end}')
            rb_refresh = self.load_hiSDconfig()[0]['rb_refresh']
            self.radioButton_refresh.setChecked(rb_refresh)
            ftr_from = self.load_hiSDconfig()[0]['ftr_from']
            self.lineEdit_ftr_from.setText(f'{ftr_from}')
            ftr_from_min = self.load_hiSDconfig()[0]['ftr_from_min']
            self.lineEdit_ftr_from_min.setText(f'{ftr_from_min}')
            ftr_to = self.load_hiSDconfig()[0]['ftr_to']
            self.lineEdit_ftr_to.setText(f'{ftr_to}')
            ftr_to_min = self.load_hiSDconfig()[0]['ftr_to_min']
            self.lineEdit_ftr_to_min.setText(f'{ftr_to_min}')
            rb_str = self.load_hiSDconfig()[0]['rb_str']
            self.radioButton_str.setChecked(rb_str)
            str_from = self.load_hiSDconfig()[0]['str_from']
            self.lineEdit_str_from.setText(f'{str_from}')
            str_from_min = self.load_hiSDconfig()[0]['str_from_min']
            self.lineEdit_str_from_min.setText(f'{str_from_min}')
            str_to = self.load_hiSDconfig()[0]['str_to']
            self.lineEdit_str_to.setText(f'{str_to}')
            str_to_min = self.load_hiSDconfig()[0]['str_to_min']
            self.lineEdit_str_to_min.setText(f'{str_to_min}')
            rb_alarm = self.load_hiSDconfig()[0]['rb_alarm']
            self.radioButton_alarm.setChecked(rb_alarm)
            rb_plan = self.load_hiSDconfig()[0]['rb_plan']
            self.radioButton_plan.setChecked(rb_plan)
            rb_images = self.load_hiSDconfig()[0]['rb_images']
            self.radioButton_images.setChecked(rb_images)
            rb_auto = self.load_hiSDconfig()[0]['rb_auto']
            self.radioButton_auto.setChecked(rb_auto)
            token = self.load_hiSDconfig()[0]['token']
            self.lineEdit_token.setText(f'{token}')
            chat_id = self.load_hiSDconfig()[0]['chat_id']
            self.lineEdit_chat_id.setText(f'{chat_id}')
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
