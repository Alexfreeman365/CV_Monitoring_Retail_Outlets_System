import telebot
import time
import ftplib

from funcs_initializer_camconfig_getcamframe import load_camconfig
from funcs_FTP_access_cams_media_structure import get_ftp_host_user_pas
from funcs_TxtUI_request_app_description import *


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
    return f'{hours:02}:{minutes:02}:{seconds:02}'


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


DESCRIPTION = (
        'После успешного запуска программы создайте для нее ярлык и перенесите его в папку автозагрузки Windows.\n'
        '\n'
        '11_FTPDataAlert - программа для контроля равномерного потока кадров камер,\n'
        'поступающих на FTP. Другими словами, программа контролирует работоспособность камер на объектах.\n'
        'В случае потери связи с камерой из-за проблем с интернетом или потери питания на объекте программа\n'
        'отправит сообщение в Telegram. Также в конце рабочего дня, указанного для каждой камеры в\n'
        'файле базы данных camconfig, программа отправит общее количество непустых кадров за весь день\n'
        'для каждой камеры.\n'
        '\n'
        'Принцип работы программы:\n' 
        '1. Нахождение программы – папка cams_media в структуре системы\n'
        '2. Из файла camconfig программа получает названия камер, подключенных к системе, вместе с их рабочими часами\n'
        '3. Программа получает учетные реквизиты FTP доступа из сохраненных настроек рядом находящихся загрузчиков\n'
        '(из первого файла .dat)\n'
        '4. Программа делает запрос для получения учетных Telegram реквизитов (шапка этого файла)\n'
        '5. Далее программа в непрерывном цикле:\n'
        '   Каждые 45 секунд заходит на FTP сервер и в соответствующие рабочие часы сравнивает последние кадры\n'
        '   для каждой камеры с текущим временем. Если промежуток больше 3 минут, то программа отправляет сообщение\n'
        '   о том, что определенная камера не в сети. Также она сообщает о восстановлении потока с камеры\n'
        '   В конце рабочего дня программа отправляет общее количество кадров для каждой камеры.\n'
        '6. Программа защищена от любых ошибок, возникающих в цикле. В случае появление таковых программа создает\n'
        'и ведет журнал.\n'
    )


if __name__ == '__main__':
    # cwd_path = 'L:\Active_pjs\RG\cams_media'
    cwd_path = os.getcwd()
    parent_dir = os.path.dirname(cwd_path)

    cam_work_hours = {d['cam_name']: d['work_hours']
                      for d in load_camconfig(parent_dir)}

    ftp_host, ftp_user, ftp_pas = get_ftp_host_user_pas(cwd_path)

    request = f"Введите данные:\n" \
              f"bot_token->:\nchat_id->:\nЖурнал событий->: Нет\n{'-' * 30}"
    data = request_app_description('11_FTPDataAlert', cwd_path, request, DESCRIPTION)
    bot_token, chat_id, ledger_msg = data
    chat_id = int(chat_id)
    bot = telebot.TeleBot(bot_token)
    ledger_flag = ledger_msg == 'Да'

    no_connection = {}
    total_sended = []
    first_launch = True

    while True:
        try:
            ftp = ftplib.FTP(ftp_host)
            ftp.login(ftp_user, ftp_pas)
            cam_names = sorted(ftp.nlst())

            if first_launch:
                send_message(chat_id, f'Программа для контроля {len(cam_names)} камер '
                                      f'({", ".join(cam_names)}) запущена успешно')
                first_launch = False

            cur_dt = datetime.today()
            all_work_hours = (h for i in cam_work_hours.values() for h in eval(i))
            sorted_hours = sorted(all_work_hours)
            min_hour, max_hour = sorted_hours[0], sorted_hours[-1]
            min_work_hour_dt = cur_dt.replace(hour=min_hour, minute=0, second=0)
            max_work_hour_dt = cur_dt.replace(hour=max_hour, minute=10, second=0)

            if min_work_hour_dt <= cur_dt <= max_work_hour_dt:
                for cam_name in sorted(cam_work_hours):
                    if cam_name in cam_names:
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
                                if ledger_flag:
                                    log_event(cwd_path, cam_name, 'disconnected over 3 min')
                            if cam_name in no_connection and delta < 60:  # 60
                                lost_delta = (last_img_dt - no_connection[cam_name]).total_seconds()
                                del no_connection[cam_name]
                                lost_time = seconds_to_hhmmss(int(lost_delta))
                                msg = f'{cam_name.upper()} Ok - В сети! - {lost_time}'
                                send_message(chat_id, msg)
                                if ledger_flag:
                                    log_event(cwd_path, cam_name, f'connected >>> lost {lost_time}')
                            if cam_name in total_sended:
                                total_sended.remove(cam_name)

                        elif (end_dt.replace(hour=end_hour, minute=3, second=0)
                              < cur_dt and cam_name not in total_sended):
                            last_img_dt = datetime.strptime(get_last_frame(cam_name)[1:13], '%y%m%d%H%M%S')
                            if last_img_dt.day == cur_dt.day:
                                estimated_num_frames = (end_hour - start_hour) * 3600 // 45
                                total_not_empty_frames = last_day_total(cam_name)
                                msg = f'{cam_name.upper()} Общее кол-во кадров за день: ' \
                                      f'из {estimated_num_frames} в наличии {total_not_empty_frames}'
                                send_message(chat_id, msg)
                                total_sended.append(cam_name)
                            else:
                                total_sended.clear()
                ftp.quit()
        except Exception as error:
            if ledger_flag:
                log_event(cwd_path, 'error', type(error).__name__)
            time.sleep(5)
        # print(no_connection)
        time.sleep(45)  # 45


