import os
import shutil
from datetime import datetime
import time
import sys

# Добавляем корень проекта в пути поиска для доступа к utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import (
    cleanup_mei_folders,
    request_app_description,
    log_event
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
            # Модифицируем dirs на месте, чтобы os.walk не заходил в ненужные папки
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
        # 1. Считаем количество файлов для отчета (пропуская скрытые и исключения)
        total_files = 0
        for root, dirs, files in os.walk(source_path):
            # Фильтруем папки, чтобы не заходить в лишние
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_list]
            # Считаем только полезные файлы
            total_files += len([f for f in files if not f.startswith('.')])

        # 2. Определяем фильтр для копирования
        def ignore_filter(directory, contents):
            return [item for item in contents if item.startswith('.') or item in ignore_list]

        # 3. Выполняем синхронизацию
        if os.path.exists(target_path):
            shutil.copytree(source_path, target_path, ignore=ignore_filter, dirs_exist_ok=True)
        else:
            shutil.copytree(source_path, target_path, ignore=ignore_filter)

        # 4. Получаем метку времени для мониторинга
        m_time = get_max_mtime(source_path, ignore_list)

        # 5. Выводим то самое сообщение, которое вы просили
        log_event(cwd, app_name, "Sync", f"Обновлено объектов: {total_files}")

        return m_time
    except Exception as e:
        log_event(cwd, app_name, "Error", f"Ошибка при синхронизации: {str(e)}")
        return None


if __name__ == '__main__':
    app_name = os.path.basename(sys.executable).split('.')[0]
    cwd = os.getcwd()

    # Формируем запрос настроек. Четвертая строка теперь функциональна.
    prompt_msg = (
        "ИНСТРУКЦИЯ: Данные вносить строго после '->:'\n"
        "1. Исходный путь (папка проекта) ->:\n"
        "2. Целевой путь (Google Диск) ->:\n"
        "3. Игнорировать папки (через запятую) ->: .git, .idea, venv, __pycache__"
    )
    description = "--- Параметры синхронизации проекта ---"

    # Читаем данные через ваш модуль utils
    config_data = request_app_description(app_name, cwd, prompt_msg, description)

    if len(config_data) >= 3:
        source_path = config_data[0].strip().replace('"', '')
        target_base_path = config_data[1].strip().replace('"', '')

        # Обработка списка исключений (разбиваем по запятой и чистим пробелы)
        raw_ignore = config_data[2].strip()
        ignore_list = [i.strip() for i in raw_ignore.split(',') if i.strip()]

        # Имя папки проекта для создания в целевой директории
        folder_name = os.path.basename(source_path.rstrip(os.sep))
        final_target_path = os.path.join(target_base_path, folder_name)

        try:
            if os.path.exists(source_path):
                # Гарантируем наличие папки назначения
                os.makedirs(final_target_path, exist_ok=True)

                # Первичный проход
                last_mtime = perform_sync(source_path, final_target_path, ignore_list, app_name, cwd)

                if last_mtime is not None:
                    log_event(cwd, app_name, "System", f"Запуск мониторинга. Игнорируем: {', '.join(ignore_list)}")

                    while True:
                        time.sleep(5)
                        try:
                            # Проверяем изменения во всем дереве проекта
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
        # Сюда попадем, если utils.request_app_description не нашел данных
        sys.exit(0)