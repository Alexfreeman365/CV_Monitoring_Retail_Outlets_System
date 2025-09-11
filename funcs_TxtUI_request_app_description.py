import os
import sys
import shutil
import glob
import portalocker
import csv
from datetime import datetime
import time


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


def log_event(cwd_path, app_name, name, message):
    current_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    log_file_name = f'{app_name}_event_log.csv'
    log_file_path = os.path.join(cwd_path, log_file_name)

    try:
        with open(log_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not os.path.exists(log_file_path):
                writer.writerow(['timestamp', 'name', 'message'])
            writer.writerow([current_time, name, message])
    except IOError as e:
        pass


def cleanup_mei_folders(cwd_path=os.getcwd()):
    hi_temp_path = os.path.join(cwd_path, "hi_temp")
    lock_file = os.path.join(hi_temp_path, "cleanup.lock")

    if os.path.exists(hi_temp_path):
        try:
            # Создаём файл блокировки
            with portalocker.Lock(lock_file, timeout=0.1,
                                  flags=portalocker.LOCK_EX | portalocker.LOCK_NB,
                                  fail_when_locked=False):  # Ждём 0.1 сек
                current_mei = getattr(sys, '_MEIPASS', None)
                # Нормализуем путь текущего MEI для точного сравнения
                current_mei_normalized = os.path.normcase(os.path.abspath(current_mei)) if current_mei else None

                mei_folders = glob.glob(os.path.join(hi_temp_path, "_MEI*"))
                for mei_folder in mei_folders:
                    # Нормализуем путь для сравнения
                    mei_folder_normalized = os.path.normcase(os.path.abspath(mei_folder))
                    if current_mei_normalized and mei_folder_normalized == current_mei_normalized:
                        continue  # Точно пропускаем свой каталог

                    try:
                        if os.path.exists(mei_folder):
                            shutil.rmtree(mei_folder, ignore_errors=True)
                    except Exception:
                        continue

        except portalocker.exceptions.LockException:
            pass  # Другая программа уже выполняет очистку
        finally:
            if os.path.exists(lock_file):
                for _ in range(3):  # 3 попытки удалить lock-файл
                    try:
                        os.remove(lock_file)
                        break
                    except PermissionError:
                        time.sleep(0.1)  # Короткая пауза между попытками
                    except Exception:
                        break