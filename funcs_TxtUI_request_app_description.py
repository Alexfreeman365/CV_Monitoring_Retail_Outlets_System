import os
import sys
import csv
from datetime import datetime


def txt_notification(app_name, path, msg):
    txt_name = f'{app_name}_notification.txt'
    txt_path = os.path.join(path, txt_name)
    with open(txt_path, 'w', encoding='utf-8') as f:
        print(f'{msg}', file=f)


def request_app_description(app_name, path, request, description):
    txt_name = f'{app_name}_request_app_description.txt'
    txt_path = os.path.join(path, txt_name)
    data = []
    if os.path.exists(txt_path):
        with open(txt_path, mode='r', encoding='utf-8') as f:
            next(f)
            for line in f:
                data_txt = line.strip()
                if '---' not in data_txt:
                    data.append(data_txt.split('->:')[1].strip())
                else:
                    break
    else:
        with open(txt_path, mode='w', encoding='utf-8') as f:
            print(request, description, sep='\n', file=f)
        sys.exit(0)

    if not all(map(len, data)):
        msg = 'Для работы программы заполните данные в файле ниже'
        txt_notification(app_name, path, msg)
        sys.exit(0)
    return data


def log_event(cwd_path, name, message):
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    log_file_name = '11_FTPDataAlert_event_log.csv'
    log_file_path = os.path.join(cwd_path, log_file_name)
    with open(log_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not os.path.exists(log_file_path):
            writer.writerow(['timestamp', 'name', 'message'])
        writer.writerow([current_time, name, message])