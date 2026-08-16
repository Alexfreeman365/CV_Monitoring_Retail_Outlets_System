import os
import sys
from datetime import datetime, timedelta

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_TxtUI_request_app_description import cleanup_mei_folders, get_app_name, request_app_description

import atexit
atexit.register(cleanup_mei_folders)


def create_msg(msg_path, msg):
    with open(msg_path, 'w', encoding='utf-8') as f:
        print(*msg, sep='\n', file=f)


def parse_photo_time(filename, format_str):
    """Пытается извлечь время из имени файла"""
    try:
        return datetime.strptime(filename[:12], format_str)
    except:
        return None


DESCRIPTION = (
    'Программа для поиска пропущенных фотографий.\n'
    'Находит временные промежутки (от 1 минуты) без кадров в указанном рабочем\n'
    'диапазоне и записывает их в файл <app>_respond.txt.\n'
)


if __name__ == '__main__':
    cwd_path = os.getcwd()
    app_name = get_app_name()
    respond_msg_path = os.path.join(cwd_path, f'{app_name}_respond.txt')

    request = (f"Введите данные:\n"
               f"Путь к папке с фото->:\n"
               f"Рабочие часы (10-20)->:\n"
               f"{'-' * 30}")

    data = request_app_description(app_name, cwd_path, request, DESCRIPTION)
    photo_path = data[0]
    start_hour, end_hour = tuple(map(int, data[1].split('-')))

    good_respond = ['Все OK! Пропусков нет.']
    bed_respond = ['Ошибка! Проверьте введенные данные.']

    try:
        if not os.path.exists(photo_path):
            create_msg(respond_msg_path, bed_respond + [f"Путь не существует: {photo_path}"])
            sys.exit(1)

        # collect all files and sort by time
        all_files = os.listdir(photo_path)
        f = '%y%m%d%H%M%S'

        # keep only files with a valid timestamp in the name
        photos_with_time = []
        for file in all_files:
            dt = parse_photo_time(file, f)
            if dt:
                photos_with_time.append((dt, file))

        if not photos_with_time:
            create_msg(respond_msg_path, bed_respond + ["Нет файлов с корректной датой в имени"])
            sys.exit(1)

        # sort by time
        photos_with_time.sort(key=lambda x: x[0])

        # group by day and analyse gaps
        respond_msg = []
        current_day = photos_with_time[0][0].date()
        day_photos = []

        for dt, file in photos_with_time + [(None, None)]:
            if dt and dt.date() == current_day:
                day_photos.append((dt, file))
            else:
                # analyse the current day
                if day_photos:
                    day_start = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=start_hour)
                    day_end = datetime.combine(current_day, datetime.min.time()) + timedelta(hours=end_hour)

                    prev_time = day_start
                    for dt, _ in day_photos:
                        if dt > day_end:
                            break
                        if prev_time < dt:
                            minutes = (dt - prev_time).seconds // 60
                            if minutes >= 1:
                                start_str = prev_time.strftime("%H:%M")
                                end_str = dt.strftime("%H:%M")
                                respond_msg.append(f'{start_str} - {end_str}: ~ {minutes} min')
                        prev_time = dt

                    if prev_time < day_end:
                        minutes = (day_end - prev_time).seconds // 60
                        if minutes >= 1:
                            start_str = prev_time.strftime("%H:%M")
                            end_str = day_end.strftime("%H:%M")
                            respond_msg.append(f'{start_str} - {end_str}: ~ {minutes} min')

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
        create_msg(respond_msg_path, bed_respond + [str(e)])
        sys.exit(1)
