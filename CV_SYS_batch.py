"""Batch pipeline: process all accumulated days per shop group, then exit.

Run ONCE with CV_SYS stopped (single-shot, not a daemon). After it finishes,
start CV_SYS_v1.py for real-time operation.

Orchestration is BY DAYS inside each group (the invariant that CV_SYS's
real-time loop does not guarantee for accumulated days):
    for each group (shop) -> for each day (ascending) ->
        shape_detection(all cameras of the group, only that day)
        -> vis_count_noseller_pipeline(main camera)

The newest (last) day of each group gets shape_detection only; its vis_count is
left to CV_SYS, matching "count visitors only after the day is closed".
"""
import os
import sys

from ultralytics import YOLO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils.db as db
from utils.funcs_CV import shape_detection, save_shape_db_info
from utils.funcs_vis_count_noseller_time import vis_count_noseller_pipeline, short_name
from utils.funcs_initializer_camconfig_getcamframe import (
    initializer, load_last_day_processed_imgs)

MODEL_REL_PATH = os.path.join('.venv', 'neural_network_models', 'yolov10x.pt')


def group_cameras(cam_names):
    groups = {}
    for cn in sorted(cam_names):
        groups.setdefault(short_name(cn), []).append(cn)
    return groups


def last_seen_day(cam_name, cwd_path):
    imgs = load_last_day_processed_imgs(cam_name, cwd_path)
    return imgs[0][:6] if len(imgs) else '000101'


def unprocessed_days(cam_name, images_path, cwd_path):
    seen = last_seen_day(cam_name, cwd_path)
    days = []
    for day in sorted(os.listdir(images_path)):
        if day[2:] >= seen:
            days.append(day[2:])
    return days


def main():
    cwd_path = os.getcwd()
    ip_cam_data_paths_dict, cam_names = initializer(cwd_path)

    model_path = os.path.join(cwd_path, MODEL_REL_PATH)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f'Model not found: {model_path}')
    shape_detector = YOLO(model_path)

    groups = group_cameras(cam_names)
    print(f'Camera groups (shops): {groups}')

    for sn, cams in sorted(groups.items()):
        main_cam = next((c for c in cams if not c[-1].isdigit() or c[-1] == '1'), cams[0])
        print(f'\n=== Group {sn}: cams={cams}, main={main_cam} ===')

        cam_days = {cn: unprocessed_days(cn, ip_cam_data_paths_dict[cn], cwd_path) for cn in cams}
        all_days = sorted({d for days in cam_days.values() for d in days})
        if not all_days:
            print('  nothing to process')
            continue

        last_day = all_days[-1]
        for day in all_days:
            run_vis = (day != last_day)
            print(f'  day {day}: shape_detection(all cams)'
                  + ('' if run_vis else ' [last day -> no vis_count, left for CV_SYS]'))
            for cn in cams:
                if day not in cam_days[cn]:
                    print(f'    {cn}: no frames, skip')
                    continue
                cam_shapes_db_len = db.shapes_count(cn, cwd_path)
                shape_detection(shape_detector, cam_shapes_db_len,
                                ip_cam_data_paths_dict[cn], cn, cam_names,
                                only_day=day, skip_vis_count=True, cwd_path=cwd_path)
            if run_vis:
                vis_count_noseller_pipeline(main_cam, ip_cam_data_paths_dict[main_cam], cwd_path)
                save_shape_db_info(cam_names, cwd_path)

    print('\nBatch processing finished.')


if __name__ == '__main__':
    main()
