from keras.models import load_model
import subprocess, psutil
import telebot
from ultralytics import YOLO
from funcs_CV import *
from funcs_vis_count_noseller_time import *
from funcs_TxtUI_request_app_description import *


def start_hiFTPCleaner_CVloadAntifreeze(cwd_path, hiFTPCleaner=True):
    loc_path = os.path.join(cwd_path, 'cams_media')
    if hiFTPCleaner:
        hiFTPCleaner_exe = [f for f in os.listdir(loc_path)
                            if 'hiFTPCleaner' in f
                            and f.split('.')[-1] == 'exe'][0]
        hiFTPCleaner_proc = subprocess.Popen([os.path.join(loc_path, hiFTPCleaner_exe)], cwd=loc_path)
    else:
        hiFTPCleaner_proc = None

    CVloadAntifreeze_exe = [f for f in os.listdir(loc_path)
                            if 'CVloadAntifreeze' in f
                            and f.split('.')[-1] == 'exe'][0]
    CVloadAntifreeze_proc = subprocess.Popen([os.path.join(loc_path, CVloadAntifreeze_exe)], cwd=loc_path)
    process = [hiFTPCleaner_proc, CVloadAntifreeze_proc]
    return [p for p in process if p]


def terminate_hiFTPCleaner_CVloadAntifreeze(process):
    for proc in process:
        try:
            pobj = psutil.Process(proc.pid)
            for c in pobj.children(recursive=True):
                try:
                    c.terminate()
                except psutil.NoSuchProcess:
                    continue

            pobj.terminate()

            try:
                pobj.wait(timeout=5)
            except (psutil.TimeoutExpired, psutil.NoSuchProcess):

                try:
                    pobj.kill()
                except psutil.NoSuchProcess:
                    continue

        except psutil.NoSuchProcess:
            continue


if __name__ == '__main__':
    cwd_path = os.getcwd()
    app_name = 'CV_SYS'

    request = f"Введите данные:\n" \
              f"bot_token->:\nchat_id->:\nЖурнал событий->: Нет\n{'-' * 30}"
    data = request_app_description(app_name, cwd_path, request, '---')
    bot_token, chat_id, ledger_msg = data
    chat_id = int(chat_id)
    bot = telebot.TeleBot(bot_token)

    ip_cam_data_paths_dict, cam_names = initializer(cwd_path)
    process = start_hiFTPCleaner_CVloadAntifreeze(cwd_path, hiFTPCleaner=False) #1
    time.sleep(60 * 30) #2

    try:
        shape_detector = YOLO(os.path.join(cwd_path, 'venv', 'neural_network_models', 'yolov10x.pt'))

        print('The system is loaded')
        log_event(cwd_path, app_name, 'sys', 'Starting the system')

        try:
            while True:
                for cam_name in sorted(cam_names):
                    cam_shapes_db_len = 0
                    cam_shapes_path = os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')
                    if os.path.exists(cam_shapes_path):
                        with open(cam_shapes_path, 'r') as f:
                            for _ in f:
                                cam_shapes_db_len += 1
                        cam_shapes_db_len -= 1  # Вычитаем заголовок

                    shape_detection(shape_detector, cam_shapes_db_len, ip_cam_data_paths_dict[cam_name],
                                    cam_name, cam_names, cwd_path)
                    time.sleep(5)
        except Exception as error:
            log_event(cwd_path, app_name, 'error', type(error).__name__)
            terminate_hiFTPCleaner_CVloadAntifreeze(process) #3
            bot.send_message(chat_id, 'CV_SYS >>> Ошибка в основном pipeline')
            raise error

    except KeyboardInterrupt:
        for cam_name in sorted(cam_names):
            camconfig = load_camconfig()
            cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
            hour_end = cam_set['work_hours'].split(',')[1][1:-1]
            if (datetime.now()).strftime('%H') >= hour_end: # '0'
                if not cam_name[-1].isdigit() or cam_name[-1] == '1':
                    vis_count_noseller_pipeline(cam_name, ip_cam_data_paths_dict[cam_name])
        save_shape_db_info(cam_names)
        backup_db(cwd_path)

        log_event(cwd_path, app_name, 'sys', 'Stopping the system')
        terminate_hiFTPCleaner_CVloadAntifreeze(process) #4
        cleanup_mei_folders(os.path.join(cwd_path, 'cams_media'))

