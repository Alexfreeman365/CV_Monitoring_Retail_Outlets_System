import os
import shutil
from datetime import datetime
import time
import sys

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import (
    cleanup_mei_folders,
    request_app_description,
    log_event,
    get_app_name
)

import atexit
atexit.register(cleanup_mei_folders)


def get_max_mtime(path, ignore_list):
    """
    Сканирует все дерево папок и возвращает время последнего изменения файла,
    игнорируя папки из списка исключений и скрытые файлы.
    """
    max_mtime = 0.0
    try:
        for root, dirs, files in os.walk(path):
            # modify dirs in place so os.walk skips unwanted folders
            dirs[:] = [d for d in dirs if d not in ignore_list and not d.startswith('.')]

            for f in files:
                if f.startswith('.'):
                    continue
                full_path = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(full_path)
                    if mtime > max_mtime:
                        max_mtime = mtime
                except (OSError, PermissionError):
                    continue
    except Exception:
        pass
    return max_mtime


def perform_sync(source_path, target_path, ignore_list, app_name, cwd):
    """
    Рекурсивно копирует проект и логирует количество синхронизированных файлов.
    """
    try:
        # 1. count files for the report (skip hidden and excluded)
        total_files = 0
        for root, dirs, files in os.walk(source_path):
            # filter folders to skip unwanted ones
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_list]
            # count only useful files
            total_files += len([f for f in files if not f.startswith('.')])

        # 2. define the copy filter
        def ignore_filter(directory, contents):
            return [item for item in contents if item.startswith('.') or item in ignore_list]

        # 3. run the sync
        if os.path.exists(target_path):
            shutil.copytree(source_path, target_path, ignore=ignore_filter, dirs_exist_ok=True)
        else:
            shutil.copytree(source_path, target_path, ignore=ignore_filter)

        # 4. get a timestamp for monitoring
        m_time = get_max_mtime(source_path, ignore_list)

        # 5. print the requested message
        log_event(cwd, app_name, "Sync", f"Обновлено объектов: {total_files}")

        return m_time
    except Exception as e:
        log_event(cwd, app_name, "Error", f"Ошибка при синхронизации: {str(e)}")
        return None


if __name__ == '__main__':
    app_name = get_app_name()
    cwd = os.getcwd()

    # build the settings request; the fourth line is now functional
    prompt_msg = (
        "ИНСТРУКЦИЯ: Данные вносить строго после '->:'\n"
        "1. Исходный путь (папка проекта) ->:\n"
        "2. Целевой путь (Google Диск) ->:\n"
        "3. Игнорировать папки (через запятую) ->: .git, .idea, venv, __pycache__"
    )
    description = "--- Параметры синхронизации проекта ---"

    # read data via the utils module
    config_data = request_app_description(app_name, cwd, prompt_msg, description)

    if len(config_data) >= 3:
        source_path = config_data[0].strip().replace('"', '')
        target_base_path = config_data[1].strip().replace('"', '')

        # parse the exclusion list (split by comma, strip spaces)
        raw_ignore = config_data[2].strip()
        ignore_list = [i.strip() for i in raw_ignore.split(',') if i.strip()]

        # project folder name to create in the target directory
        folder_name = os.path.basename(source_path.rstrip(os.sep))
        final_target_path = os.path.join(target_base_path, folder_name)

        try:
            if os.path.exists(source_path):
                # ensure the destination folder exists
                os.makedirs(final_target_path, exist_ok=True)

                # initial pass
                last_mtime = perform_sync(source_path, final_target_path, ignore_list, app_name, cwd)

                if last_mtime is not None:
                    log_event(cwd, app_name, "System", f"Запуск мониторинга. Игнорируем: {', '.join(ignore_list)}")

                    while True:
                        time.sleep(5)
                        try:
                            # check for changes across the whole project tree
                            current_mtime = get_max_mtime(source_path, ignore_list)

                            if current_mtime > last_mtime:
                                updated_mtime = perform_sync(source_path, final_target_path, ignore_list, app_name, cwd)
                                if updated_mtime is not None:
                                    last_mtime = updated_mtime
                        except Exception:
                            pass
            else:
                log_event(cwd, app_name, "Error", f"Путь источника не найден: {source_path}")
        except Exception as e:
            log_event(cwd, app_name, "Fatal Error", str(e))
            sys.exit(1)
    else:
        # fallback if request_app_description found no data
        sys.exit(0)