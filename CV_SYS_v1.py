from keras.models import load_model
import shutil
import subprocess, psutil

from funcs_initializer_camconfig_getcamframe import *
from funcs_CV import *
from funcs_vis_count_noseller_time import vis_count_noseller_pipeline
from funcs_TxtUI_request_app_description import log_event


def backup_db():
    if os.path.exists(os.path.join(cwd_path, 'db_backups')):
        pass
    else:
        os.mkdir(os.path.join(cwd_path, 'db_backups'))

    today = '20' + (datetime.now()).strftime('%y%m%d')

    if os.path.exists(os.path.join(cwd_path, 'db_backups', today)):
        pass
    else:
        try:
            shutil.copytree(os.path.join(cwd_path, 'db'), os.path.join(cwd_path, 'db_backups', today))
        except:
            pass

    # if len(os.listdir(os.path.join(cwd_path, 'db_backups'))) > 30:
    #     oldest_day = os.listdir(os.path.join(cwd_path, 'db_backups'))[0]
    #     shutil.rmtree(os.path.join(cwd_path, 'db_backups', oldest_day))


def start_hiFTPCleaner_CVloadAntifreeze(cwd_path):
    loc_path = os.path.join(cwd_path, 'cams_media')
    # hiFTPCleaner_exe = [f for f in os.listdir(loc_path)
    #                     if f.__contains__('hiFTPCleaner')
    #                     and f.split('.')[-1] == 'exe'][0]
    # hiFTPCleaner_proc = subprocess.Popen([os.path.join(loc_path, hiFTPCleaner_exe)], cwd=loc_path)
    CVloadAntifreeze_exe = [f for f in os.listdir(loc_path)
                            if f.__contains__('CVloadAntifreeze')
                            and f.split('.')[-1] == 'exe'][0]
    CVloadAntifreeze_proc = subprocess.Popen([os.path.join(loc_path, CVloadAntifreeze_exe)], cwd=loc_path)
    return [CVloadAntifreeze_proc] #[hiFTPCleaner_proc, CVloadAntifreeze_proc]


def kill_hiFTPCleaner_CVloadAntifreeze(process):
    for proc in process:
        pobj = psutil.Process(proc.pid)
        for c in pobj.children(recursive=True):
            try:
                c.kill()
            except:
                pass
        try:
            pobj.kill()
        except:
            pass


if __name__ == '__main__':
    cwd_path = os.getcwd()
    app_name = 'CV_SYS'
    ip_cam_data_paths_dict, cam_names = initializer()
    process = start_hiFTPCleaner_CVloadAntifreeze(cwd_path) #1

    time.sleep(60 * 20) #2

    try:
        shape_detector = load_model(os.path.join(cwd_path, 'venv', 'neural_network_models',
                                                 'efficientdet_d5_coco17_tpu-32', 'saved_model'))

        print('The system is loaded')
        log_event(cwd_path, app_name, 'sys', 'Starting the system')

        while True:
            for cam_name in sorted(cam_names):
                cam_shapes_db_len = 0
                if os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')):
                    df = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
                    cam_shapes_db_len = len(df)
                    del df

                shape_detection(shape_detector, cam_shapes_db_len, ip_cam_data_paths_dict[cam_name],
                                cam_name, cam_names)

                backup_db()
                time.sleep(5)

    except KeyboardInterrupt:
        for cam_name in sorted(cam_names):
            camconfig = load_camconfig()
            cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
            hour_end = cam_set['work_hours'].split(',')[1][1:-1]
            if (datetime.now()).strftime('%H') >= hour_end: #'0'
                if not cam_name[-1].isdigit() or cam_name[-1] == '1':
                    vis_count_noseller_pipeline(cam_name, ip_cam_data_paths_dict[cam_name])
        save_shape_db_info(cam_names)

        log_event(cwd_path, app_name, 'sys', 'Starting the system')
        kill_hiFTPCleaner_CVloadAntifreeze(process) #3


