import os
from PIL import Image

import utils.db as db


def initializer(cwd_path=os.getcwd()):
    def data_condition(item):
        return (len(str(item).split('_')) > 1) & (str(item).split('_')[-1] in ['images', 'photos'])

    media_path = os.path.join(cwd_path, 'cams_media')
    ip_cam_data_folders = [item for item in os.listdir(media_path) if data_condition(item)]
    ip_cam_data_folders = sorted(ip_cam_data_folders, reverse=True)
    ip_cam_data_paths = [os.path.join(media_path, item) for item in ip_cam_data_folders]
    cam_names = ['_'.join(str(item).split('_')[:-1]) for item in ip_cam_data_folders]
    ip_cam_data_paths_dict = dict(zip(cam_names, ip_cam_data_paths))

    os.makedirs(os.path.join(cwd_path, 'db'), exist_ok=True)

    camconfig = load_camconfig(cwd_path)
    for cam_name in cam_names:
        frame = get_cam_frame(cam_name, ip_cam_data_paths_dict)
        if cam_name not in [cam_set['cam_name'] for cam_set in camconfig]:
            camconfig.append({
                'cam_name': cam_name,
                'shape_zone': frame,
                'face_zone': (round(frame[1] * 0.65), frame[1], frame[2], frame[3]),
                'frame': frame,
                'work_hours': (10, 21),
                'vis_count_alg': (2, 2)
            })
    camconfig = [cam_set for cam_set in camconfig if cam_set['cam_name'] in cam_names]
    save_camconfig(camconfig, cwd_path)
    return ip_cam_data_paths_dict, cam_names


def load_camconfig(path=os.getcwd()):
    return db.load_camconfig(path)


def save_camconfig(camconfig, cwd_path=os.getcwd()):
    db.save_camconfig(camconfig, cwd_path)


def get_cam_frame(cam_name, ip_cam_data_paths_dict):
    first_day = os.listdir(ip_cam_data_paths_dict[cam_name])[0]
    first_image_name = os.listdir(os.path.join(ip_cam_data_paths_dict[cam_name], first_day))[0]
    img_path = os.path.join(ip_cam_data_paths_dict[cam_name], first_day, first_image_name)
    img = Image.open(img_path)
    frame = 0, img.size[1], 0, img.size[0]
    return frame


def dt_slice_shape_df(df_cam, dt_start, dt_end):
    df = df_cam.copy()
    dt_end_full = str(int(dt_end) + 1)
    df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
    return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]


def load_last_day_processed_imgs(cam_name, cwd_path=os.getcwd()):
    return db.read_last_day_processed(cam_name, cwd_path)


def save_last_day_processed_imgs(last_day_processed_imgs, cam_name, cwd_path=os.getcwd()):
    db.write_last_day_processed(last_day_processed_imgs, cam_name, cwd_path)
