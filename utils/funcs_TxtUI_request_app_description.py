import os
import sys
import shutil
import glob
import csv
from datetime import datetime


def get_path(relative_path):
    """Универсальное получение пути к ресурсам"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # resolve path relative to the project ROOT (one level above utils)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_app_name():
    """Application name without extension. Works both as a .py script and a PyInstaller exe."""
    return os.path.splitext(os.path.basename(sys.argv[0].replace('\\', '/')))[0]


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

    if not all(map(len, data[:3])):
        msg = 'Для работы программы заполните данные в файле ниже'
        txt_notification(app_name, path, msg)
        sys.exit(0)
    return data


def log_event(cwd_path, app_name, name, message):
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{name}] Event: {message}")
    log_file_name = f'{app_name}_event_log.csv'
    log_file_path = os.path.join(cwd_path, log_file_name)

    try:
        write_header = not os.path.exists(log_file_path)
        with open(log_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(['timestamp', 'name', 'message'])
            writer.writerow([current_time, str(name), str(message)])
    except IOError:
        pass


def cleanup_mei_folders(cwd_path=os.getcwd()):
    hi_temp_path = os.path.join(cwd_path, "hi_temp")

    if os.path.exists(hi_temp_path):
        mei_folders = glob.glob(os.path.join(hi_temp_path, "_MEI*"))
        for mei_folder in mei_folders:
            try:
                if os.path.exists(mei_folder):
                    shutil.rmtree(mei_folder, ignore_errors=True)
            except Exception:
                continue