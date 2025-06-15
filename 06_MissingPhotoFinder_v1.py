import os
from datetime import datetime, timedelta


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


if __name__ == '__main__':
    cwd_path = os.getcwd()
    request_msg_path = os.path.join(os.getcwd(), 'MissingPhotoFinder_request.txt')
    respond_msg_path = os.path.join(cwd_path, 'MissingPhotoFinder_respond.txt')

    request_msg = ['path:', 'working hours (10-20):']
    good_respond = ['Все OK! Пропусков нет.']
    bed_respond = ['Ошибка! Проверьте введенные данные.']

    if not os.path.exists(request_msg_path):
        create_msg(request_msg_path, request_msg)
    else:
        try:
            data = get_request_msg(request_msg_path)
            photo_path, start_hour, end_hour = data

            photos = os.listdir(photo_path)

            f = '%y%m%d%H%M%S'
            initial_time = datetime.strptime(photos[0][:12], f)
            start_time = initial_time.replace(hour=start_hour, minute=0, second=0)
            end_time = initial_time.replace(hour=end_hour - 1, minute=59, second=59)

            end = [datetime.strptime(i[:12], f) for i in photos] + [end_time]
            start = [start_time] + end

            diff = list(map(lambda x, y: (x - y).seconds // 60, end, start))
            miss_time = list(filter(lambda m: m[2] >= 1, zip(start, end, diff)))

            hour_min_start = lambda dt: datetime.strftime(dt + timedelta(minutes=1), "%H:%M")
            hour_min_end = lambda dt: datetime.strftime(dt, "%H:%M")

            respond_msg = []
            for r in miss_time:
                respond_msg.append(f'{hour_min_start(r[0])} - {hour_min_end(r[1])}: ~ {r[2]} min')

            if respond_msg:
                create_msg(respond_msg_path, respond_msg)
            else:
                create_msg(respond_msg_path, good_respond)
        except:
            create_msg(respond_msg_path, bed_respond)