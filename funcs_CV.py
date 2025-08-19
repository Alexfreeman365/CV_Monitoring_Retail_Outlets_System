import cv2
import tensorflow as tf
import time
from tqdm import tqdm
import numpy as np
import csv
from datetime import datetime

from funcs_initializer_camconfig_getcamframe import *
from funcs_TxtUI_request_app_description import log_event
from funcs_vis_count_noseller_time import vis_count_noseller_pipeline


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


def save_shape_db_info(cam_names, cwd_path=os.getcwd()):
    if len(cam_names) != 0:
        shape_db_info = []
        for cam_name in cam_names:
            cam_shapes_path = os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv')
            if os.path.exists(cam_shapes_path):
                with open(cam_shapes_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    header = next(reader)

                    first_row = next(reader)
                    first_day = first_row['origin_file_name'][:6]

                    df_cam_len = 1
                    last_day = first_day

                    for row in reader:
                        df_cam_len += 1
                        last_day = row['origin_file_name'][:6]

                row = {'Camera': cam_name, 'File_name': f'{cam_name}_shapes_locs.csv',
                       'First_day': datetime.strptime(first_day, '%y%m%d'),
                       'Last_day': datetime.strptime(last_day, '%y%m%d'),
                       'Number_of_lines': df_cam_len}
                shape_db_info.append(row)

        shape_db_info = pd.DataFrame(shape_db_info)
        shape_db_info.to_csv(os.path.join(cwd_path, 'db', 'shape_db_info.csv'), index=False)


def get_first_part(i):
    return str(i).split('.')[0].split('_')[0].split('-')[0].split('b')[0]


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


def shape_detection(shape_detector, total_len_shapes_db, images_path, cam_name, cam_names, cwd_path=os.getcwd()):
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
            vis_count_noseller_pipeline(cam_name, images_path)
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

                        log_event(cwd_path, 'CV_SYS', 'sys', 'Starting the system')
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