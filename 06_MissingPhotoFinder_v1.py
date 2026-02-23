import os
import sys
from datetime import datetime, timedelta

# Добавляем корень проекта в пути поиска, чтобы Python видел папку utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import cleanup_mei_folders

import atexit
atexit.register(cleanup_mei_folders)


def create_msg(msg_path, msg):
    with open(msg_path, 'w', encoding='utf-8') as f:
        print(*msg, sep='\n', file=f)


def get_request_msg(msg_path):
    if os.path.exists(msg_path):
        with open(msg_path, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
        path = data[0].split(':', maxsplit=1)[1].strip()
        hours_str = data[1].split(':', maxsplit=1)[1].strip().split('-')
        start, end = tuple(map(int, hours_str))
        return path, start, end
    return None, None, None


def parse_photo_time(filename, format_str):
    """Пытается извлечь время из имени файла"""
    try:
        return datetime.strptime(filename[:12], format_str)
    except:
        return None


if __name__ == '__main__':
    cwd_path = os.getcwd()
    app_name = os.path.basename(sys.executable).split('.')[0]
    request_msg_path = os.path.join(os.getcwd(), f'{app_name}_request.txt')
    respond_msg_path = os.path.join(cwd_path, f'{app_name}_respond.txt')

    request_msg = ['path:', 'working hours (10-20):']
    good_respond = ['Все OK! Пропусков нет.']
    bed_respond = ['Ошибка! Проверьте введенные данные.']

    if not os.path.exists(request_msg_path):
        create_msg(request_msg_path, request_msg)
    else:
        try:
            data = get_request_msg(request_msg_path)
            if data[0] is None:
                create_msg(respond_msg_path, bed_respond + ["Файл запроса не найден или поврежден"])
                sys.exit(1)

            photo_path, start_hour, end_hour = data

            if not os.path.exists(photo_path):
                create_msg(respond_msg_path, bed_respond + [f"Путь не существует: {photo_path}"])
                sys.exit(1)

            # Получаем все файлы и сортируем по времени
            all_files = os.listdir(photo_path)
            f = '%y%m%d%H%M%S'

            # Фильтруем только файлы с корректной датой в имени
            photos_with_time = []
            for file in all_files:
                dt = parse_photo_time(file, f)
                if dt:
                    photos_with_time.append((dt, file))

            if not photos_with_time:
                create_msg(respond_msg_path, bed_respond + ["Нет файлов с корректной датой в имени"])
                sys.exit(1)

            # Сортируем по времени
            photos_with_time.sort(key=lambda x: x[0])

            # Определяем границы рабочего дня для каждого дня
            respond_msg = []

            # Группируем по дням
            current_day = photos_with_time[0][0].date()
            day_photos = []

            for dt, file in photos_with_time + [(None, None)]:  # Добавляем sentinel для обработки последнего дня
                if dt and dt.date() == current_day:
                    day_photos.append((dt, file))
                else:
                    # Анализируем текущий день
                    if day_photos:
                        # Устанавливаем границы рабочего дня
                        day_start = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=start_hour)
                        day_end = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=end_hour)

                        # Проверяем промежутки между файлами
                        prev_time = day_start
                        for dt, _ in day_photos:
                            if dt > day_end:
                                break

                            # Если есть промежуток между предыдущим файлом и текущим
                            if prev_time < dt:
                                minutes = (dt - prev_time).seconds // 60
                                if minutes >= 1:
                                    start_str = prev_time.strftime("%H:%M")
                                    end_str = dt.strftime("%H:%M")
                                    respond_msg.append(f'{start_str} - {end_str}: ~ {minutes} min')

                            prev_time = dt

                        # Проверяем промежуток после последнего файла до конца дня
                        if prev_time < day_end:
                            minutes = (day_end - prev_time).seconds // 60
                            if minutes >= 1:
                                start_str = prev_time.strftime("%H:%M")
                                end_str = day_end.strftime("%H:%M")
                                respond_msg.append(f'{start_str} - {end_str}: ~ {minutes} min')

                    # Начинаем новый день
                    if dt:
                        current_day = dt.date()
                        day_photos = [(dt, file)]
                    else:
                        day_photos = []

            if respond_msg:
                create_msg(respond_msg_path, respond_msg)
            else:
                create_msg(respond_msg_path, good_respond)
            sys.exit(0)

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Ошибка: {e}", file=sys.stderr)
            if 'request_msg_path' in locals() and os.path.exists(request_msg_path):
                create_msg(respond_msg_path, bed_respond + [str(e)])
            sys.exit(1)