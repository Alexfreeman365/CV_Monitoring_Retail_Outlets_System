from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import (QDialog, QApplication, QRadioButton,
                             QPushButton, QLabel, QCheckBox)
import shutil
import os
import sys

# Добавляем корень проекта в пути поиска, чтобы Python видел папку utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import get_path, cleanup_mei_folders

import atexit
atexit.register(cleanup_mei_folders)


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

        uic.loadUi(get_path('ui/10_hiSampler_gui_v1.ui'), self)

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
