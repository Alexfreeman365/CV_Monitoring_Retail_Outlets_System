import os
import pandas as pd
from PIL import Image


def initializer():
    def data_condition(item):
        return (len(str(item).split('_')) > 1) & (str(item).split('_')[-1] in ['images', 'photos'])

    media_path = os.path.join(os.getcwd(), 'cams_media')
    ip_cam_data_folders = [item for item in os.listdir(media_path) if data_condition(item)]
    ip_cam_data_folders = sorted(ip_cam_data_folders, reverse=True)
    ip_cam_data_paths = [os.path.join(media_path, item) for item in ip_cam_data_folders]
    cam_names = ['_'.join(str(item).split('_')[:-1]) for item in ip_cam_data_folders]
    ip_cam_data_paths_dict = dict(zip(cam_names, ip_cam_data_paths))

    if os.path.exists(os.path.join(os.getcwd(), 'db')):
        pass
    else:
        os.mkdir(os.path.join(os.getcwd(), 'db'))

    if os.path.exists(os.path.join(os.getcwd(), 'db', 'camconfig.csv')):
        camconfig = load_camconfig()
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
        save_camconfig(camconfig)

    else:
        camconfig = []
        for cam_name in cam_names:
            frame = get_cam_frame(cam_name, ip_cam_data_paths_dict)
            camconfig.append({
                'cam_name': cam_name,
                'shape_zone': frame,
                'face_zone': (round(frame[1] * 0.65), frame[1], frame[2], frame[3]),
                'frame': frame,
                'work_hours': (10, 21),
                'vis_count_alg': (2, 2)
            })
        save_camconfig(camconfig)
    return ip_cam_data_paths_dict, cam_names


def load_camconfig(path=os.getcwd()):
    camconfig = []
    if os.path.exists(os.path.join(path, 'db', 'camconfig.csv')):
        camconfig = pd.read_csv(os.path.join(path, 'db', 'camconfig.csv'))
        camconfig = camconfig.to_dict(orient='records')
    return camconfig


def save_camconfig(camconfig):
    camconfig = pd.DataFrame(camconfig)
    camconfig.to_csv(os.path.join(os.getcwd(), 'db', 'camconfig.csv'), index=False)


def get_cam_frame(cam_name, ip_cam_data_paths_dict):
    first_day = os.listdir(ip_cam_data_paths_dict[cam_name])[0]
    first_image_name = os.listdir(os.path.join(ip_cam_data_paths_dict[cam_name], first_day))[0]
    img_path = os.path.join(ip_cam_data_paths_dict[cam_name], first_day, first_image_name)
    img = Image.open(img_path)
    frame = 0, img.size[1], 0, img.size[0]
    return frame


