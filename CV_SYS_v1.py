from ultralytics import YOLO
import telebot
import psutil
import sys, os, subprocess

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_CV import *
from utils.funcs_vis_count_noseller_time import *
from utils.funcs_TxtUI_request_app_description import *
import utils.db as db

MODEL_REL_PATH = os.path.join('venv', 'neural_network_models', 'yolov10x.pt')


def _launch_helper(cwd_path, loc_path, name_substr):
    """Launch a helper (hiFTPCleaner / CVloadAntifreeze). Priority: .exe -> .py -> skip."""
    exe = sorted(f for f in os.listdir(loc_path) if name_substr in f and f.endswith('.exe'))
    if exe:
        return subprocess.Popen([os.path.join(loc_path, exe[0])], cwd=loc_path)

    py = sorted(f for f in os.listdir(loc_path) if name_substr in f and f.endswith('.py'))
    if not py:
        py = sorted(f for f in os.listdir(cwd_path) if name_substr in f and f.endswith('.py'))
    if py:
        return subprocess.Popen([sys.executable, os.path.join(cwd_path, py[0])], cwd=loc_path)

    log_event(cwd_path, 'CV_SYS', 'sys', f'{name_substr}: helper not found (no .exe / .py)')
    return None


def start_hiFTPCleaner_CVloadAntifreeze(cwd_path, hiFTPCleaner=True):
    loc_path = os.path.join(cwd_path, 'cams_media')
    process = []
    if hiFTPCleaner:
        process.append(_launch_helper(cwd_path, loc_path, 'hiFTPCleaner'))
    process.append(_launch_helper(cwd_path, loc_path, 'CVloadAntifreeze'))
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
        model_path = os.path.join(cwd_path, MODEL_REL_PATH)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model not found: {model_path}')
        shape_detector = YOLO(model_path)

        print('The system is loaded')
        log_event(cwd_path, app_name, 'sys', 'Starting the system')

        try:
            while True:
                for cam_name in sorted(cam_names):
                    cam_shapes_db_len = db.shapes_count(cam_name, cwd_path)

                    shape_detection(shape_detector, cam_shapes_db_len, ip_cam_data_paths_dict[cam_name],
                                    cam_name, cam_names, change_past=None, cwd_path=cwd_path)
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

