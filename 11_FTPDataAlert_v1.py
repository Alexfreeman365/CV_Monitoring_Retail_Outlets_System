import os
import sys
import time
import ftplib
import atexit
import threading
import queue
import asyncio
import ast
from datetime import datetime

# imports for extended timeout handling
import httpx
import httpcore

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_initializer_camconfig_getcamframe import load_camconfig
from utils.funcs_FTP_access_cams_media_structure import get_ftp_host_user_pas
from utils.funcs_TxtUI_request_app_description import *

atexit.register(cleanup_mei_folders)
from telegram.error import NetworkError, TimedOut

# global thread-safe queue for Telegram messages
msg_queue = queue.Queue()


# ============================================================
# 1. async engine to bypass blocks
# ============================================================
async def telegram_worker_loop(bot_token, api_server_url, chat_id, proxy=None):
    from telegram.ext import ApplicationBuilder
    from telegram.request import HTTPXRequest

    print(f"[DEBUG] Инициализация сетевого транспорта бота с прокси: {proxy}...")

    request_init = None
    if proxy:
        request_init = HTTPXRequest(proxy=proxy, connect_timeout=5.0, read_timeout=5.0)

    builder = ApplicationBuilder().token(bot_token).base_url(api_server_url)
    if request_init:
        builder = builder.request(request_init)

    application = builder.build()
    print("[DEBUG] Сборка Application завершена успешно.")

    for init_attempt in range(5):
        try:
            await application.initialize()
            break
        except Exception as init_err:
            print(f"[DEBUG] Ошибка инициализации транспорта (Попытка {init_attempt + 1}/5): {init_err}")
            if init_attempt < 4:
                await asyncio.sleep(3)
            else:
                print("[DEBUG] Не удалось инициализировать сетевой транспорт.")
                return

    bot = application.bot
    loop = asyncio.get_running_loop()

    while True:
        try:
            message = await loop.run_in_executor(None, msg_queue.get)
            if message is None:
                break

            for attempt in range(3):
                try:
                    await bot.send_message(
                        chat_id=int(chat_id),
                        text=message,
                        parse_mode=None
                    )
                    print(f"[DEBUG] Успешно отправлено оповещение!")
                    break
                except (TimedOut, httpx.ReadTimeout, httpcore.ReadTimeout) as timeout_err:
                    print(f"[DEBUG] Таймаут ответа от API ({type(timeout_err).__name__}). Пропуск ретрая.")
                    break
                except (NetworkError, httpx.ConnectTimeout, httpcore.ConnectTimeout) as net_err:
                    print(f"[DEBUG] Сетевая ошибка (Попытка {attempt + 1}/3): {net_err}")
                    if attempt < 2:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    else:
                        raise
                except Exception as send_err:
                    retry_after = getattr(send_err, "retry_after", None)
                    if retry_after is not None or "retry after" in str(send_err).lower():
                        if attempt < 2:
                            sleep_time = float(retry_after) if retry_after else 1.0
                            print(f"[DEBUG] Flood control. Ожидание {sleep_time} сек...")
                            await asyncio.sleep(sleep_time)
                            continue
                    raise

            msg_queue.task_done()
        except Exception as e:
            print(f"[DEBUG] Непредвиденная ошибка в фоновом отправщике: {e}")
            await asyncio.sleep(1)

    await application.shutdown()


def start_telegram_worker(bot_token, base_url, chat_id, proxy=None):
    """Запускает изолированный фоновый поток для асинхронного Application."""

    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(telegram_worker_loop(bot_token, base_url, chat_id, proxy))

    worker_thread = threading.Thread(target=run, daemon=True)
    worker_thread.start()


def send_telegram_message(bot, chat_id, message):
    """Кладет сообщение в очередь отправки фонового потока."""
    if chat_id is None or not message:
        return
    msg_queue.put(message)


# ============================================================
# 2. functions from the old version (with .cache filtering)
# ============================================================
def get_last_frame(cam_name):
    ftp.cwd(cam_name)
    last_img = None
    try:
        # filter .cache and check the camera folder is not empty
        items = sorted([d for d in ftp.nlst() if d != '.cache'])
        if not items:
            ftp.cwd('..')
            return None

        ftp.cwd(items[-1])
        ftp.cwd('images')
        try:
            files = sorted([f for f in ftp.nlst() if f != '.cache'])
            last_img = files[-1] if files else None
        except:
            try:
                time.sleep(2)
                files = sorted([f for f in ftp.nlst() if f != '.cache'])
                last_img = files[-1] if files else None
            except:
                try:
                    time.sleep(2)
                    files = sorted([f for f in ftp.nlst() if f != '.cache'])
                    last_img = files[-1] if files else None
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
        days = sorted([d for d in ftp.nlst() if d != '.cache'])
        ftp.cwd(days[-1])
        ftp.cwd('images')
        try:
            total = sum([1 for img in ftp.nlst() if img != '.cache' and ftp.size(img)])
        except:
            try:
                time.sleep(2)
                total = sum([1 for img in ftp.nlst() if img != '.cache' and ftp.size(img)])
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


# ============================================================
# 3. program description
# ============================================================
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
    '7. Используется локальный сервер Telegram Bot API (контейнер) для обхода блокировок провайдера.\n'
)

# ============================================================
# 4. initialization
# ============================================================
if __name__ == '__main__':
    cwd_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(cwd_path)
    app_name = get_app_name()

    cam_work_hours = {d['cam_name']: d['work_hours'] for d in load_camconfig(parent_dir)}
    ftp_host, ftp_user, ftp_pas = get_ftp_host_user_pas(cwd_path)

    request = (f"Введите данные:\n"
               f"bot_token->:\n"
               f"chat_id->:\n"
               f"Журнал событий->: Нет\n"
               f"{'-' * 30}")

    config_exists = any('.txt' in f for f in os.listdir(cwd_path) if app_name in f)
    data = request_app_description(app_name, cwd_path, request, DESCRIPTION)
    if not config_exists:
        print(f"\n[{app_name}] Первый запуск: Файл конфигурации создан. Настройте параметры и перезапустите.")
        sys.exit(0)

    bot_token, chat_id, ledger_raw = data[:3]
    ledger_flag = ledger_raw.strip().lower() in ['да', 'true', '1', 'yes']
    chat_id = int(chat_id)

    final_url = "https://api.telegram.org/bot"
    proxy_url = "http://host.docker.internal:2080"

    start_telegram_worker(bot_token, final_url, chat_id, proxy=proxy_url)

    no_connection = {}
    total_sended = set()  # set prevents mutual camera reset
    first_launch = True

    # ============================================================
    # 5. main synchronous loop
    # ============================================================
    while True:
        ftp = None
        try:
            ftp = ftplib.FTP(ftp_host, timeout=10)
            ftp.login(ftp_user, ftp_pas)

            cam_names = sorted(ftp.nlst())
            cam_names = [name for name in cam_names if name != '.cache']

            if first_launch:
                msg = f'Программа для контроля {len(cam_names)} камер ({", ".join(cam_names)}) запущена успешно'
                send_telegram_message(None, chat_id, msg)
                if ledger_flag:
                    log_event(cwd_path, app_name, 'SYSTEM', 'Application started successfully')
                first_launch = False

            cur_dt = datetime.today()
            all_work_hours = (h for i in cam_work_hours.values() for h in ast.literal_eval(i))
            sorted_hours = sorted(all_work_hours)
            min_hour, max_hour = sorted_hours[0], sorted_hours[-1]
            min_work_hour_dt = cur_dt.replace(hour=min_hour, minute=0, second=0)
            max_work_hour_dt = cur_dt.replace(hour=max_hour, minute=10, second=0)

            if min_work_hour_dt <= cur_dt <= max_work_hour_dt:
                for cam_name in sorted(cam_work_hours):
                    if cam_name in cam_names:
                        start_hour, end_hour = ast.literal_eval(cam_work_hours[cam_name])
                        start_dt = cur_dt.replace(hour=start_hour, minute=1, second=0)
                        end_dt = cur_dt.replace(hour=end_hour, minute=0, second=0)

                        # monitor connection loss
                        if start_dt <= cur_dt <= end_dt:
                            res_frame = get_last_frame(cam_name)
                            last_img_dt = datetime.strptime(res_frame[1:13], '%y%m%d%H%M%S') if res_frame else cur_dt
                            delta = (cur_dt - last_img_dt).total_seconds()

                            if delta > 180 and cam_name not in no_connection:
                                no_connection[cam_name] = last_img_dt
                                msg = f'{cam_name.upper()} XXX Не в сети больше трех минут ¯\\_(ツ)_/¯'
                                send_telegram_message(None, chat_id, msg)
                                if ledger_flag:
                                    log_event(cwd_path, app_name, cam_name, 'disconnected over 3 min')

                            if cam_name in no_connection and delta < 60:
                                lost_delta = (last_img_dt - no_connection[cam_name]).total_seconds()
                                del no_connection[cam_name]
                                lost_time = seconds_to_hhmmss(int(lost_delta))
                                msg = f'{cam_name.upper()} Ok - В сети! - {lost_time}'
                                send_telegram_message(None, chat_id, msg)
                                if ledger_flag:
                                    log_event(cwd_path, app_name, cam_name, f'connected >>> lost {lost_time}')

                            if cam_name in total_sended:
                                total_sended.remove(cam_name)

                        # end-of-day summary
                        elif (end_dt.replace(hour=end_hour, minute=3, second=0) < cur_dt
                              and cam_name not in total_sended):
                            res_frame = get_last_frame(cam_name)
                            last_img_dt = datetime.strptime(res_frame[1:13], '%y%m%d%H%M%S') if res_frame else cur_dt

                            if last_img_dt.day == cur_dt.day:
                                estimated_num_frames = (end_hour - start_hour) * 3600 // 45
                                total_not_empty_frames = last_day_total(cam_name)
                                msg = (f'{cam_name.upper()} Общее кол-во кадров за день: '
                                       f'из {estimated_num_frames} в наличии {total_not_empty_frames}')
                                send_telegram_message(None, chat_id, msg)
                                total_sended.add(cam_name)
                            else:
                                total_sended.clear()
            ftp.quit()
        except Exception as error:
            error_name = type(error).__name__
            print(f"[DEBUG] Ошибка в цикле: {error_name} ({error})")
            if ledger_flag:
                try:
                    log_event(cwd_path, app_name, 'error', error_name)
                except:
                    pass
            time.sleep(5)

        time.sleep(45)