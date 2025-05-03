from datetime import datetime, timedelta
import telebot
import time
import csv
import os
import ftplib

from funcs_FTP_access_cams_media_structure import get_ftp_host_user_pas
from funcs_initializer_camconfig_getcamframe import load_camconfig


def get_last_frame(cam_name):
    ftp.cwd(cam_name)
    last_img = None
    try:
        ftp.cwd(ftp.nlst()[-1])
        ftp.cwd('images')
        try:
            last_img = sorted(ftp.nlst())[-1]
        except:
            try:
                time.sleep(2)
                last_img = sorted(ftp.nlst())[-1]
            except:
                try:
                    time.sleep(2)
                    last_img = sorted(ftp.nlst())[-1]
                except:
                    pass
        ftp.cwd('..')
    except:
        ftp.cwd('..')
        pass
    ftp.cwd('..')
    ftp.cwd('..')
    return last_img


def last_day_total(cam_name):
    ftp.cwd(cam_name)
    total = None
    try:
        ftp.cwd(ftp.nlst()[-1])
        ftp.cwd('images')
        try:
            total = sum([1 for img
                         in ftp.nlst()
                         if ftp.size(img)])
        except:
            try:
                time.sleep(2)
                total = sum([1 for img
                             in ftp.nlst()
                             if ftp.size(img)])
            except:
                pass
        ftp.cwd('..')
    except:
        ftp.cwd('..')
        pass
    ftp.cwd('..')
    ftp.cwd('..')
    return total


def seconds_to_hhmmss(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_Telegram_access(path=os.getcwd()):
    bot_token, chat_id = str(), str()
    text_note_path = os.path.join(path, 'Telegram_access.txt')
    if os.path.exists(text_note_path):
        with open(text_note_path, 'r') as f:
            bot_token, chat_id = f.read().splitlines()
    return bot_token, int(chat_id)


def send_message(chat_id=None, message=None):
    if chat_id is None:
        pass
    else:
        try:
            bot.send_message(chat_id, message)
        except:
            try:
                time.sleep(2)
                bot.send_message(chat_id, message)
            except:
                time.sleep(2)
                bot.send_message(chat_id, message)


def log_error(error_message):
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    log_file = '11_FTPDataAlert_error_log.csv'
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Error Message'])
        writer.writerow([current_time, error_message])


if __name__ == '__main__':
    # cwd_path = 'L:\Active_pjs\RG\cams_media'
    cwd_path = os.getcwd()
    parent_dir = os.path.dirname(cwd_path)

    cam_work_hours = {d['cam_name']: d['work_hours']
                      for d in load_camconfig(parent_dir)}

    bot_token, chat_id = get_Telegram_access(cwd_path)
    bot = telebot.TeleBot(bot_token)

    ftp_host, ftp_user, ftp_pas = get_ftp_host_user_pas(cwd_path)

    no_connection = {}
    total_sended = []

    while True:
        try:
            ftp = ftplib.FTP(ftp_host)
            ftp.login(ftp_user, ftp_pas)

            for cam_name in sorted(cam_work_hours):
                if cam_name in ftp.nlst():
                    cur_dt = datetime.today()
                    start_hour, end_hour = eval(cam_work_hours[cam_name])
                    start_dt = cur_dt.replace(hour=start_hour, minute=1, second=0)
                    end_dt = cur_dt.replace(hour=end_hour, minute=0, second=0)

                    if start_dt <= cur_dt <= end_dt:
                        last_img_dt = datetime.strptime(get_last_frame(cam_name)[1:13], '%y%m%d%H%M%S')
                        delta = (cur_dt - last_img_dt).total_seconds()
                        # print(cam_name, delta)
                        if delta > 180 and cam_name not in no_connection:  # 180
                            no_connection[cam_name] = last_img_dt
                            msg = f'{cam_name.upper()} XXX Не в сети больше трех минут ¯\_(ツ)_/¯'
                            send_message(chat_id, msg)
                        if cam_name in no_connection and delta < 60:  # 60
                            lost_delta = (last_img_dt - no_connection[cam_name]).total_seconds()
                            del no_connection[cam_name]
                            lost_time = seconds_to_hhmmss(int(lost_delta))
                            msg = f'{cam_name.upper()} Ok - В сети! - {lost_time}'
                            send_message(chat_id, msg)
                        if cam_name in total_sended:
                            total_sended.remove(cam_name)

                    elif end_dt < cur_dt and cam_name not in total_sended:
                        last_img_dt = datetime.strptime(get_last_frame(cam_name)[1:13], '%y%m%d%H%M%S')
                        if last_img_dt.day == cur_dt.day:
                            total_not_empty_frames = last_day_total(cam_name)
                            msg = f'{cam_name.upper()} Общее количество кадров за день: {total_not_empty_frames}'
                            send_message(chat_id, msg)
                            total_sended.append(cam_name)
            ftp.quit()
        except Exception as error:
            log_error(error)
            time.sleep(5)
            pass
        # print(no_connection)
        time.sleep(45)  # 45


