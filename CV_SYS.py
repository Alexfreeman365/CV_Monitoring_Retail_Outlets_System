# Version 1.2
from keras.models import load_model
import cv2
import numpy as np
import pandas as pd
import shutil
import os
import tensorflow as tf
from datetime import datetime, timedelta
import subprocess, time, psutil
from tqdm import tqdm


def load_camconfig():
    camconfig = []
    if os.path.exists(os.path.join(cwd_path, 'db', 'camconfig.csv')):
        camconfig = pd.read_csv(os.path.join(cwd_path, 'db', 'camconfig.csv'))
        camconfig = camconfig.to_dict(orient='records')
    return camconfig


def save_camconfig(camconfig):
    camconfig = pd.DataFrame(camconfig)
    camconfig.to_csv(os.path.join(cwd_path, 'db', 'camconfig.csv'), index=False)


def get_cam_frame(cam_name, ip_cam_data_paths_dict):
    first_day = os.listdir(ip_cam_data_paths_dict[cam_name])[0]
    first_image_name = os.listdir(os.path.join(ip_cam_data_paths_dict[cam_name], first_day))[0]
    first_image = cv2.imread(os.path.join(ip_cam_data_paths_dict[cam_name], first_day, first_image_name))
    shape = first_image.shape[:2]
    frame = 0, shape[0], 0, shape[1]
    return frame


def get_coords_from_text(coords):
    if len(coords.split(',')) == 4:
        # Single zone coords
        dirty_list = coords[1:-1].split(',')
        ymin = int(dirty_list[0])
        ymax = int(dirty_list[1][1:])
        xmin = int(dirty_list[2][1:])
        xmax = int(dirty_list[3][1:])
        return ymin, ymax, xmin, xmax

    if len(coords.split(',')) == 8:
        # Double zone coords
        l0 = coords.split(')')[0][2:].split(',')
        t0 = tuple(np.array(l0, dtype='int'))
        l1 = coords.split(')')[1][3:].split(',')
        t1 = tuple(np.array(l1, dtype='int'))
        return [t0, t1]

    if len(coords.split(',')) == 12:
        # Triple zone coords
        l0 = coords.split(')')[0][2:].split(',')
        t0 = tuple(np.array(l0, dtype='int'))
        l1 = coords.split(')')[1][3:].split(',')
        t1 = tuple(np.array(l1, dtype='int'))
        l2 = coords.split(')')[2][3:].split(',')
        t2 = tuple(np.array(l2, dtype='int'))
        return [t0, t1, t2]


def save_shape_db_info(cam_names):
    if len(cam_names) != 0:
        shape_db_info = []
        for cam_name in cam_names:
            if os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')):
                df_cam = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
                first_day = df_cam.iloc[0]['origin_file_name'][:6]
                last_day = df_cam.iloc[-1]['origin_file_name'][:6]
                df_cam_len = len(df_cam)
                row = {'Camera': cam_name, 'File_name': f'{cam_name}_shapes_locs.csv',
                       'First_day': datetime.strptime(first_day, '%y%m%d'),
                       'Last_day': datetime.strptime(last_day, '%y%m%d'),
                       'Number_of_lines': df_cam_len}
                shape_db_info.append(row)
                del df_cam
        shape_db_info = pd.DataFrame(shape_db_info)
        shape_db_info.to_csv(os.path.join(cwd_path, 'db', 'shape_db_info.csv'), index=False)


def initializer():
    def data_condition(item):
        return (len(str(item).split('_')) > 1) & (str(item).split('_')[-1] in ['images', 'photos'])

    media_path = os.path.join(cwd_path, 'cams_media')
    ip_cam_data_folders = [item for item in os.listdir(media_path) if data_condition(item)]
    ip_cam_data_folders = sorted(ip_cam_data_folders, reverse=True)
    ip_cam_data_paths = [os.path.join(media_path, item) for item in ip_cam_data_folders]
    cam_names = ['_'.join(str(item).split('_')[:-1]) for item in ip_cam_data_folders]
    ip_cam_data_paths_dict = dict(zip(cam_names, ip_cam_data_paths))

    if os.path.exists(os.path.join(cwd_path, 'db')):
        pass
    else:
        os.mkdir(os.path.join(cwd_path, 'db'))

    if os.path.exists(os.path.join(cwd_path, 'db', 'camconfig.csv')):
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

    save_shape_db_info(cam_names)

    return ip_cam_data_paths_dict, cam_names


def get_first_part(i):
    return str(i).split('.')[0].split('_')[0].split('-')[0].split('b')[0]


def dt_slice_shape_df(df_cam, dt_start, dt_end):
    df = df_cam.copy()
    dt_end_full = str(int(dt_end) + 1)
    df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
    return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]


def rectangle_on_shape(img, shape_location):
    y1, y2, x1, x2 = shape_location
    return cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)


def rectangle_on_face(img, face_loc):
    y1, x2, y2, x1 = face_loc
    return cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)


def detection_zone_intersection(shape_location, zone_coords):
    if len(str(zone_coords).split(',')) == 4:
        # Single_zone_intersection
        ymin, ymax, xmin, xmax = shape_location

        if type(zone_coords) == tuple:
            y1, y2, x1, x2 = zone_coords
        else:
            y1, y2, x1, x2 = get_coords_from_text(zone_coords)

        dx = min(xmax, x2) - max(xmin, x1)
        dy = min(ymax, y2) - max(ymin, y1)

        if (dx >= 0) and (dy >= 0):
            return 1
        else:
            return 0

    if len(str(zone_coords).split(',')) == 8:
        # Double_zone_intersection
        ymin, ymax, xmin, xmax = shape_location

        y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
        y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]

        dx0 = min(xmax, x02) - max(xmin, x01)
        dy0 = min(ymax, y02) - max(ymin, y01)
        dx1 = min(xmax, x12) - max(xmin, x11)
        dy1 = min(ymax, y12) - max(ymin, y11)

        if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)):
            return 1
        else:
            return 0

    if len(str(zone_coords).split(',')) == 12:
        # Triple_zone_intersection
        ymin, ymax, xmin, xmax = shape_location

        y01, y02, x01, x02 = get_coords_from_text(zone_coords)[0]
        y11, y12, x11, x12 = get_coords_from_text(zone_coords)[1]
        y21, y22, x21, x22 = get_coords_from_text(zone_coords)[2]

        dx0 = min(xmax, x02) - max(xmin, x01)
        dy0 = min(ymax, y02) - max(ymin, y01)
        dx1 = min(xmax, x12) - max(xmin, x11)
        dy1 = min(ymax, y12) - max(ymin, y11)
        dx2 = min(xmax, x22) - max(xmin, x21)
        dy2 = min(ymax, y22) - max(ymin, y21)

        if ((dx0 >= 0) and (dy0 >= 0)) | ((dx1 >= 0) and (dy1 >= 0)) | ((dx2 >= 0) and (dy2 >= 0)):
            return 1
        else:
            return 0


def plus_random_8(image_name):
    date_time = get_first_part(image_name)
    random_num = np.random.randint(10000000, 99999999)
    return date_time[:14] + str(random_num)


def load_last_day_processed_imgs(cam_name):
    last_day_processed_imgs = []
    if os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_last_day_processed_imgs.csv')):
        last_day_processed_imgs = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_last_day_processed_imgs.csv'))
        if len(last_day_processed_imgs) <= 1:
            last_day_processed_imgs = [str(last_day_processed_imgs.squeeze())]
        else:
            last_day_processed_imgs = last_day_processed_imgs.squeeze().to_list()
    return last_day_processed_imgs


def save_last_day_processed_imgs(last_day_processed_imgs, cam_name):
    last_day_processed_imgs = pd.Series(last_day_processed_imgs)
    last_day_processed_imgs.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_last_day_processed_imgs.csv'), index=False)


def shape_detection(total_len_shapes_db, images_path, cam_name, cam_names):
    last_day_processed_imgs = load_last_day_processed_imgs(cam_name)
    if len(last_day_processed_imgs) != 0:
        last_seen_day = last_day_processed_imgs[0][:6]
    else:
        last_seen_day = '000101'

    cam_imgs_dict = {}
    for day in os.listdir(images_path):
        day_cam_imgs = []
        if day[2:] >= last_seen_day:
            for file_name in os.listdir(os.path.join(images_path, day)):
                if get_first_part(file_name) != 'Thumbs':
                    day_cam_imgs.append(file_name)
            cam_imgs_dict[day] = day_cam_imgs

    shapes_locs = []
    last_day = str()
    for day in cam_imgs_dict.keys():
        last_day = day[2:]

        if (last_seen_day != last_day and
                (not cam_name[-1].isdigit() or cam_name[-1] == '1') and
                os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))):
            vis_count_noseller_pipeline(cam_name)
            save_shape_db_info(cam_names)

        countdown = 0
        for image_name in tqdm(cam_imgs_dict[day]):
            if (image_name not in last_day_processed_imgs) & (get_first_part(image_name) != 'Thumbs'):

                img_size = os.path.getsize(os.path.join(images_path, day, image_name))
                if img_size == 0:
                    time.sleep(2)

                try:
                    img = cv2.imread(os.path.join(images_path, day, image_name))
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                except:
                    print('Problem with: ', image_name, cam_name)
                    if get_first_part(image_name) != 'Thumbs':
                        last_day_processed_imgs.append(image_name)

                        log_entry(image_name, cam_name)
                    continue

                inputTensor = tf.convert_to_tensor(img_rgb, dtype=tf.uint8)
                inputTensor = inputTensor[tf.newaxis, ...]

                detections = shape_detector(inputTensor)
                bboxs = detections['detection_boxes'][0].numpy()
                classIndexes = detections['detection_classes'][0].numpy().astype(np.int32)
                classScores = detections['detection_scores'][0].numpy()

                imH, imW, imC = img.shape
                bboxIdx = tf.image.non_max_suppression(bboxs, classScores, max_output_size=50,
                                                       iou_threshold=0.5, score_threshold=0.5)
                if len(bboxIdx) != 0:

                    for i in bboxIdx:
                        bbox = tuple(bboxs[i].tolist())
                        # classConfidence = round(100*classScores[i])
                        classIndex = classIndexes[i]

                        if classIndex == 1:
                            ymin, xmin, ymax, xmax = bbox

                            xmin, xmax, ymin, ymax = (xmin * imW, xmax * imW, ymin * imH, ymax * imH)
                            xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)
                            shape_location = [ymin, ymax, xmin, xmax]
                            square_of_shape = (ymax - ymin) * (xmax - xmin)

                            camconfig = load_camconfig()
                            shape_zone = [cam_set['shape_zone'] for cam_set in camconfig
                                          if cam_set['cam_name'] == cam_name][0]
                            shape_alarm = detection_zone_intersection(shape_location, shape_zone)

                            face_zone = [cam_set['face_zone'] for cam_set in camconfig
                                         if cam_set['cam_name'] == cam_name][0]
                            face_alarm = detection_zone_intersection(shape_location, face_zone)

                            date_time = plus_random_8(image_name)
                            new_image_name = date_time + '.jpg'

                            shape_loc = {'origin_file_name': image_name, 'uid8': date_time,
                                         'shape_location': shape_location, 'shape_zone_coords': shape_zone,
                                         'shape_zone': shape_alarm, 'face_zone_coords': face_zone,
                                         'face_zone': face_alarm}
                            shapes_locs.append(shape_loc)
                last_day_processed_imgs.append(image_name)
            # countdown += 1
            # print(f'{cam_name}_{day} Processing {int(countdown / (len(cam_imgs_dict[day])) * 100)}%')
            # clear_output(wait=True)

        df_new = pd.DataFrame(shapes_locs)
        if os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')):
            df_new.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'),
                          mode='a', header=False, index=False)
        else:
            df_new.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'), index=False)

        if len(df_new) > 0:
            print(f'{(datetime.now()).strftime("%y%m%d %H:%M")} '
                  f'Detected {len(df_new)} new shapes in {cam_name} total: {total_len_shapes_db}')

        last_day_processed_imgs_filtered = [v for v in last_day_processed_imgs if str(v)[:6] >= last_day]
        if len(last_day_processed_imgs_filtered) == 0:
            last_day_processed_imgs_filtered = last_day_processed_imgs
        save_last_day_processed_imgs(last_day_processed_imgs_filtered, cam_name)
    return


def base_columns_hours(cam_name):
    camconfig = load_camconfig()
    cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
    hour_start = int(cam_set['work_hours'].split(',')[0][1:])
    hour_end = int(cam_set['work_hours'].split(',')[1][:-1])
    int_hours = np.arange(hour_start, hour_end)
    cols = [str(hour) for hour in int_hours]
    cols.insert(0, 'date')
    cols.append('sum')
    cols.append('s')
    return cols, hour_start, hour_end


def short_name(name):
    if name[-1].isdigit():
        name = name[:-1]
    return name


def find_new_shapes(cam_name, last_cam_visitors_day, camconfig):
    next_cam_visitors_day = datetime.strptime(last_cam_visitors_day, '%y%m%d') + timedelta(days=1)
    str_next_cam_visitors_day = datetime.strftime(next_cam_visitors_day, '%y%m%d')
    print(str_next_cam_visitors_day)

    if not cam_name[-1].isdigit():
        cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
        cam_shapes = cam_shapes.sort_values('origin_file_name')
        cam_shapes = cam_shapes.reset_index(drop=True)
        cam_shapes.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'), index=False)
        cam_shapes['cam_name'] = cam_name
        new_shapes = dt_slice_shape_df(cam_shapes, str_next_cam_visitors_day, str_next_cam_visitors_day)
    else:
        group = [cam_set['cam_name'] for cam_set in camconfig if cam_set['cam_name'][:-1] == cam_name[:-1]]
        new_shapes = pd.DataFrame()
        for cam_name in group:
            cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
            cam_shapes = cam_shapes.sort_values('origin_file_name')
            cam_shapes = cam_shapes.reset_index(drop=True)
            cam_shapes.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'), index=False)
            cam_shapes['cam_name'] = cam_name
            cam_new_shapes = dt_slice_shape_df(cam_shapes, str_next_cam_visitors_day, str_next_cam_visitors_day)
            new_shapes = pd.concat([new_shapes, cam_new_shapes])

        new_shapes = new_shapes.sort_values('origin_file_name')
        new_shapes = new_shapes.reset_index(drop=True)

    return new_shapes, str_next_cam_visitors_day


def visitors_counting(cam_name, new_shapes, date, mean_threshold, window_next, step_of_frames=1):
    columns, hour_start, hour_end = base_columns_hours(cam_name)
    if len(new_shapes) != 0:
        new_shapes = new_shapes[new_shapes['cam_name'] == cam_name]
        shapes = new_shapes[new_shapes['shape_zone'] == 1]
        if len(shapes) != 0:
            column = ['origin_file_name', 'cam_name']
            shapes = shapes[column].copy()

            shapes['date'] = shapes['origin_file_name'].apply(lambda x: int(x[0:6])).astype('str')
            shapes['hour'] = shapes['origin_file_name'].apply(lambda x: int(x[6:8])).astype('str')

            # Combining people into groups according to their frames and counting them
            df_mto = shapes[shapes.duplicated(subset='origin_file_name', keep=False)]
            df_mto_gr = (df_mto[df_mto.duplicated(subset='origin_file_name', keep=False)]
                         .groupby('origin_file_name')['date'].count())
            df_mto_gr = pd.DataFrame(df_mto_gr)
            df_mto_gr.columns = ['people_num']

            # Connecting group frames with single ones
            df_ones = shapes.drop_duplicates(
                subset='origin_file_name').set_index('origin_file_name')
            df_pc = df_ones.join(df_mto_gr)
            df_pc = df_pc.fillna(1)
            df_pc.reset_index(inplace=True)
            df_pc['people_num'] = df_pc['people_num'].astype('int')

            # Creating a sample of frames according to the time step
            if step_of_frames > 1:
                df_pc = df_pc.copy().iloc[range(0, len(df_pc), step_of_frames)]

            # Creating a quantitative shift to count the change
            # in the number of people from frame to frame
            df_pc['people_lag'] = df_pc['people_num'].shift(1)
            df_pc = df_pc.fillna(1)
            df_pc['people_lag'] = df_pc['people_lag'].astype('int')

            df_pc = df_pc.fillna(1)
            df_pc['people_diff'] = df_pc['people_num'] - df_pc['people_lag']
            df_pc.loc[df_pc['people_diff'] < 0, 'people_diff'] = 0

            def custom_rolling_mean(data, mean_threshold, window_next):
                window = 1
                result = []
                for i in range(len(data)):
                    if i < window:
                        mean = 1
                    else:
                        start = max(i - window, 0)
                        end = i
                        mean = sum(data[start:end]) / (end - start)
                        if mean <= mean_threshold:
                            window = 1
                        else:
                            window = window_next
                    result.append(mean)
                result = result[1:]
                result.append(1)
                return result

            df_pc['people_num_rol'] = custom_rolling_mean(
                df_pc['people_num'], mean_threshold, window_next)
            df_pc['people_lag_rol'] = custom_rolling_mean(
                df_pc['people_lag'], mean_threshold, window_next)

            df_pc = df_pc.fillna(1)
            df_pc['people_diff_rol'] = df_pc['people_num_rol'] - df_pc['people_lag_rol']
            df_pc.loc[df_pc['people_diff_rol'] < 0, 'people_diff_rol'] = 0

            visitors = pd.pivot_table(
                df_pc, values='people_diff_rol', index='date',
                columns='hour', aggfunc='sum', fill_value=0).reset_index()
            visitors.iloc[:, 1:12] = round(visitors.iloc[:, 1:12])
            visitors['sum'] = visitors.iloc[:, 1:12].sum(axis=1)
            visitors['s'] = 'auto'
            visitors.columns.name = None
            visitors['date'] = pd.to_datetime(visitors['date'], format='%y%m%d')

            if len(visitors.columns) < len(columns):
                visitors = pd.DataFrame(visitors, columns=columns).fillna(0)

            int_columns = {c: 'int' for c in visitors.columns[1:-1]}
            visitors = visitors.astype(int_columns)
            visitors['date'] = visitors['date'].astype('str')

        else:
            hour_zero_values = np.zeros((1, hour_end - hour_start + 1), dtype=int)
            visitors = pd.DataFrame(hour_zero_values, columns=columns[1:-1])
            visitors['date'] = datetime.strptime(date, '%y%m%d')
            visitors['date'] = visitors['date'].astype('str')
            visitors['s'] = 'auto'
            visitors = visitors[columns]
    else:
        hour_zero_values = np.zeros((1, hour_end - hour_start + 1), dtype=int)
        visitors = pd.DataFrame(hour_zero_values, columns=columns[1:-1])
        visitors['date'] = datetime.strptime(date, '%y%m%d')
        visitors['date'] = visitors['date'].astype('str')
        visitors['s'] = 'auto'
        visitors = visitors[columns]

    return visitors


def noSeller_time(cam_name, new_shapes, date, absence_threshold=10):
    # Get the standard hours for the specific outlet camera
    columns, hour_start, hour_end = base_columns_hours(cam_name)
    columns = columns[:-1]  # Drop 's' ('source') column
    if len(new_shapes) != 0:
        shapes = new_shapes[new_shapes['shape_zone'] == 1]

        if len(shapes) != 0:
            # Use only the photo name as data
            column = ['origin_file_name']
            shapes = shapes[column].copy()

            shapes['date'] = shapes['origin_file_name'].apply(lambda x: int(x[0:6])).astype('str')
            shapes['hour'] = shapes['origin_file_name'].apply(lambda x: int(x[6:8])).astype('str')

            # Get photos with people
            df_ones = shapes.drop_duplicates(subset='origin_file_name').copy()
            df_ones['dt'] = df_ones['origin_file_name'].apply(
                lambda x: datetime.strptime(x[:12], '%y%m%d%H%M%S'))

            # Find missing hours and create milestones from them
            existing_hours = list(set(df_ones['hour']))
            normal_hours = columns[1:][:-1]
            normal_hours.append(str(hour_end))  # Append the last hour for safety time shift
            missing_hours = [hour for hour in normal_hours if hour not in existing_hours]
            missing_hours_rows = []
            for hour in missing_hours:
                current_date = datetime.strptime(df_ones.iloc[0]['date'] + str(hour), '%y%m%d%H')
                row = {'origin_file_name': 'auto_insert', 'date': df_ones.iloc[0]['date'],
                       'hour': hour, 'dt': current_date}
                missing_hours_rows.append(row)
            full_ones = pd.concat([df_ones, pd.DataFrame(missing_hours_rows)])
            full_ones = full_ones.sort_values('dt')

            # Shift the time column to calculate the difference
            full_ones['dt_shift'] = full_ones['dt'].shift(1, fill_value=full_ones['dt'].iloc[0])
            full_ones['dt_delta'] = full_ones['dt'] - full_ones['dt_shift']
            full_ones['minutes'] = full_ones['dt_delta'].dt.seconds / 60

            # Сompare with the threshold
            full_ones['thresholded'] = round(
                full_ones['minutes'].where(full_ones['minutes'] >= absence_threshold, 0)).astype('int')
            full_ones['thresholded_rshift'] = full_ones['thresholded'].shift(-1, fill_value=0)

            # Aggregate the time of absence above the threshold by the hour
            full_no_seller_time = pd.pivot_table(
                full_ones, values='thresholded_rshift', index='date',
                columns='hour', aggfunc='sum').reset_index()

            # If the time is more than 60 minutes, then move the rest to the next hour
            for i, val in enumerate(full_no_seller_time.iloc[0, 1:]):
                if val > 60:
                    if (val - 60) == 1:  # Accounting for rounding inaccuracies
                        full_no_seller_time.iloc[0, i + 2] = 0
                    else:
                        val_over2 = full_no_seller_time.iloc[0, i+2]
                        full_no_seller_time.iloc[0, i+2] = (val - 60) + val_over2
                    full_no_seller_time.iloc[0, i + 1] = 60
            full_no_seller_time = full_no_seller_time.iloc[:, :-1]

            full_no_seller_time['sum'] = full_no_seller_time.iloc[:, 1:12].sum(axis=1)
            full_no_seller_time.columns.name = None
            full_no_seller_time['date'] = pd.to_datetime(full_no_seller_time['date'], format='%y%m%d')

            # Use the integer type for better human understanding
            int_columns = {c: 'int' for c in full_no_seller_time.columns[1:]}
            full_no_seller_time = full_no_seller_time.astype(int_columns)
        else:
            # If there is no data for the day, then create a row filled with zeros
            hour_60_values = np.full(hour_end - hour_start, 60)
            hour_60_values = np.append(hour_60_values, np.sum(hour_60_values))

            length = len(hour_60_values)
            full_no_seller_time = pd.DataFrame(data=hour_60_values.reshape(1, length), columns=columns[1:])
            full_no_seller_time['date'] = datetime.strptime(date, '%y%m%d')
            full_no_seller_time['date'] = full_no_seller_time['date'].astype('str')
            full_no_seller_time = full_no_seller_time[columns]
    else:
        # If there is no data for the day, then create a row filled with zeros
        hour_60_values = np.full(hour_end - hour_start, 60)
        hour_60_values = np.append(hour_60_values, np.sum(hour_60_values))

        length = len(hour_60_values)
        full_no_seller_time = pd.DataFrame(data=hour_60_values.reshape(1, length), columns=columns[1:])
        full_no_seller_time['date'] = datetime.strptime(date, '%y%m%d')
        full_no_seller_time['date'] = full_no_seller_time['date'].astype('str')
        full_no_seller_time = full_no_seller_time[columns]

    return full_no_seller_time


def add_photos_to_noSeller(noSeller_time_cam):
    noSeller_time_cam['photos'] = 0

    def get_day_photos(row):
        day = ''.join(str(row['date'])[:10].split('-'))
        day_photo_path = os.path.join(ip_cam_data_paths_dict[cam_name], day)
        return len([p for p in os.listdir(day_photo_path)])

    noSeller_time_cam['photos'] = noSeller_time_cam.apply(get_day_photos, axis=1)
    return noSeller_time_cam


def vis_count_noseller_pipeline(cam_name):
    print(f'{short_name(cam_name)} camera visitors_counting and noSeller algorithms in processing')

    camconfig = load_camconfig()
    cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
    mean_threshold = int(cam_set['vis_count_alg'].split(',')[0][1:])
    window_next = int(cam_set['vis_count_alg'].split(',')[1][1:-1])

    if os.path.exists(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv')):
        cam_visitors = pd.read_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv'))
        last_cam_visitors_day = ''.join(cam_visitors['date'].iloc[-1][2:].split('-'))
    else:
        cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
        last_cam_visitors_day = cam_shapes.iloc[0]['origin_file_name'][:6]
        last_cam_visitors_day = datetime.strptime(last_cam_visitors_day, '%y%m%d') - timedelta(days=1)
        last_cam_visitors_day = datetime.strftime(last_cam_visitors_day, '%y%m%d')

    new_shapes, date = find_new_shapes(cam_name, last_cam_visitors_day, camconfig)
    last_day_processed_imgs = load_last_day_processed_imgs(cam_name)
    if len(last_day_processed_imgs) != 0:
        last_seen_day = last_day_processed_imgs[0][:6]
    else:
        last_seen_day = '000101'

    if last_seen_day == date:
        visitors_pvt_cam = visitors_counting(cam_name, new_shapes, date,
                                             mean_threshold=mean_threshold,
                                             window_next=window_next)

        if cam_name == 'tlt' and len(new_shapes) != 0:
            new_shapes = dt_slice_shape_df(new_shapes, '231223',
                                           new_shapes.iloc[-1]['origin_file_name'][:6]).copy()

        noSeller_time_cam = noSeller_time(cam_name, new_shapes, date)
        noSeller_time_cam = add_photos_to_noSeller(noSeller_time_cam)

        if os.path.exists(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv')):
            visitors_pvt_cam.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv'),
                                    mode='a', header=False, index=False)
        else:
            visitors_pvt_cam.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv'), index=False)

        if os.path.exists(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_noSeller_time.csv')):
            noSeller_time_cam.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_noSeller_time.csv'),
                                     mode='a', header=False, index=False)
        else:
            noSeller_time_cam.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_noSeller_time.csv'),
                                     index=False)


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
    hiFTPCleaner_proc = subprocess.Popen([os.path.join(loc_path, 'hiFTPCleaner.exe')], cwd=loc_path)
    CVloadAntifreeze_proc = subprocess.Popen([os.path.join(loc_path, 'CVloadAntifreeze.exe')], cwd=loc_path)
    return [hiFTPCleaner_proc, CVloadAntifreeze_proc]


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


def log_entry(event, source):
    log = {
        'date_time': pd.to_datetime(datetime.now(), format='%y%m%d %H%M%S').round('s'),
        'event': event,
        'source': source
    }
    log_df = pd.DataFrame([log])

    if os.path.exists(os.path.join(cwd_path, 'db', 'logs.csv')):
        log_df.to_csv(os.path.join(cwd_path, 'db', 'logs.csv'), mode='a', header=False,
                      index=False)
    else:
        log_df.to_csv(os.path.join(cwd_path, 'db', 'logs.csv'), index=False)


if __name__ == '__main__':
    cwd_path = os.getcwd()
    ip_cam_data_paths_dict, cam_names = initializer()
    # process = start_hiFTPCleaner_CVloadAntifreeze(cwd_path) #1

    try:
        shape_detector = load_model(os.path.join(cwd_path, 'venv', 'neural_network_models',
                                                 'efficientdet_d5_coco17_tpu-32', 'saved_model'))

        print('The system is loaded')
        log_entry('Starting the system', 'sys')

        while True:
            for cam_name in sorted(cam_names):
                cam_shapes_db_len = 0
                if os.path.exists(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')):
                    df = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
                    cam_shapes_db_len = len(df)
                    del df

                shape_detection(cam_shapes_db_len, ip_cam_data_paths_dict[cam_name], cam_name, cam_names)

                backup_db()
                time.sleep(5)

    except KeyboardInterrupt:
        for cam_name in sorted(cam_names):
            camconfig = load_camconfig()
            cam_set = [cam_set for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
            hour_end = cam_set['work_hours'].split(',')[1][1:-1]
            if (datetime.now()).strftime('%H') >= hour_end: #'0'
                if not cam_name[-1].isdigit() or cam_name[-1] == '1':
                    vis_count_noseller_pipeline(cam_name)
        save_shape_db_info(cam_names)

        log_entry('Stopping the system', 'sys')
        # kill_hiFTPCleaner_CVloadAntifreeze(process) #2


