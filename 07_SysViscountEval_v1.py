import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add project root to sys.path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.funcs_vis_count_noseller_time import short_name, visitors_counting
from utils.funcs_initializer_camconfig_getcamframe import load_camconfig, save_camconfig, dt_slice_shape_df
import utils.db as db
from utils.funcs_TxtUI_request_app_description import cleanup_mei_folders, get_app_name
import atexit
atexit.register(cleanup_mei_folders)


DESCRIPTION = (
    'Программа оценки точности подсчета посетителей.\n'
    'Сравнивает ручные данные из db/1_real_viscount.xlsx с расчетом алгоритма\n'
    'и обновляет таблицы оценки. Параметры алгоритма (mean_threshold, window_next)\n'
    'задаются ниже для каждой камеры в формате: имя_камеры: (mean, window).\n'
)


def create_txt_params(text_path, camconfig, description):
    with open(text_path, 'w', encoding='utf-8') as f:
        for line in description.strip().split('\n'):
            print(f'# {line}', file=f)
        for cam in camconfig:
            if not cam['cam_name'][-1].isdigit() or cam['cam_name'][-1] == '1':
                print(f"{cam['cam_name']}: {cam['vis_count_alg']}", file=f)


def create_txt_program_status(text_note_path, msg):
    with open(text_note_path, 'w', encoding='utf-8') as f:
        print(f'{msg}', file=f)


def read_txt_params(text_note_path):
    lines = []
    if os.path.exists(text_note_path):
        with open(text_note_path, 'r') as f:
            lines = f.readlines()
    params = {}
    for l in lines:
        l = l.strip()
        if not l or l.startswith('#'):
            continue
        cam_name, dirty_params = l.split(':')
        params[cam_name] = tuple(map(int, dirty_params.strip(' ()').split(', ')))
    return params


def find_new_shapes(cam_name, last_cam_visitors_day):
    next_cam_visitors_day = datetime.strptime(last_cam_visitors_day, '%y%m%d') #+ timedelta(days=1)
    str_next_cam_visitors_day = datetime.strftime(next_cam_visitors_day, '%y%m%d')
    print(str_next_cam_visitors_day)

    cam_shapes = db.read_shapes(cam_name, cwd_path)
    cam_shapes = cam_shapes.sort_values('origin_file_name')
    cam_shapes = cam_shapes.reset_index(drop=True)
    db.write_shapes(cam_name, cam_shapes, cwd_path, mode='replace')
    cam_shapes['cam_name'] = cam_name

    new_shapes = dt_slice_shape_df(cam_shapes, str_next_cam_visitors_day, str_next_cam_visitors_day)
    new_shapes = new_shapes.sort_values('origin_file_name')
    new_shapes = new_shapes.reset_index(drop=True)
    return new_shapes, next_cam_visitors_day


def evaluation(cam_name, params, camconfig, cwd_path):
    # Reading manual data
    all_real_visitors = db.read_real_viscount(short_name(cam_name), cwd_path)
    all_real_visitors.sort_values('date', inplace=True)
    all_real_visitors.reset_index(drop=True, inplace=True)
    all_real_days_dt = np.unique(all_real_visitors['date'].dt.date)
    dt_to_str = lambda x: datetime.strftime(x, '%y%m%d')
    all_real_days = list(map(dt_to_str, all_real_days_dt))

    # Automatic calculation of the number of visitors
    cur_params = [cam_set['vis_count_alg'] for cam_set in camconfig if cam_set['cam_name'] == cam_name][0]
    if type(cur_params) != tuple:
        cur_params = tuple(map(int, cur_params.strip('()').split(', ')))

    if params[cam_name] == cur_params:
        cur_eval_statistic = db.read_evstat(short_name(cam_name), cwd_path)
        cur_eval_statistic['date'] = pd.to_datetime(cur_eval_statistic['date'])
        cur_eval_days_dt = np.unique(cur_eval_statistic['date'].dt.date)
        cur_eval_days = list(map(dt_to_str, cur_eval_days_dt))
        exist_eval_days = sorted(list(set(cur_eval_days) & set(all_real_days)))
        new_real_days = sorted(list(set(all_real_days) - set(exist_eval_days)))

        mean_threshold, window_next = cur_params
        auto_visitors = pd.DataFrame()
        for day in new_real_days:
            cam_shapes = db.read_shapes(cam_name, cwd_path)
            new_shapes = dt_slice_shape_df(cam_shapes, day, day)
            new_shapes['cam_name'] = cam_name
            day_visitors = visitors_counting(cam_name, new_shapes, day, mean_threshold, window_next, cwd_path=cwd_path)
            day_visitors['date'] = pd.to_datetime(day_visitors['date'])
            auto_visitors = pd.concat([auto_visitors, day_visitors])

        if len(auto_visitors) != 0:
            new_real = all_real_visitors[all_real_visitors['date'].isin(auto_visitors['date'].unique())].copy()

            new_real.sort_values('date', inplace=True)
            new_real.reset_index(drop=True, inplace=True)

            auto_visitors.sort_values('date', inplace=True)
            auto_visitors.reset_index(drop=True, inplace=True)
            auto_visitors['*'] = new_real['*']

            auto_visitors['s'] = 'auto'
            new_real['s'] = 'real'

            # Error calculation, data aggregation and storage
            new_real['err'] = new_real['sum'] - auto_visitors['sum']
            new_real['mape'] = round(abs(new_real['err']) / new_real['sum'], 2)

            auto_visitors['err'] = new_real['sum'] - auto_visitors['sum']
            auto_visitors['mape'] = round(abs(new_real['err']) / new_real['sum'], 2)

            new_real.index = list(range(0, len(new_real)*2, 2))
            auto_visitors.index = list(range(1, len(auto_visitors)*2, 2))

            new_eval = pd.concat([new_real, auto_visitors]).sort_index()
            new_eval['mape'] = new_eval['mape'].apply(lambda x: str(x).replace('.', ','))
            new_eval['mape'] = new_eval['mape'].replace('nan', '0,0')
            new_eval['mape'] = new_eval['mape'].fillna('0,0')

            str_to_dt = lambda x: datetime.strptime(x, '%y%m%d')
            exist_eval_days_dt = list(map(str_to_dt, exist_eval_days))
            exist_evalstat = cur_eval_statistic[cur_eval_statistic['date'].isin(exist_eval_days_dt)]
            eval_statistic = pd.concat([exist_evalstat, new_eval])
            eval_statistic.sort_values('date', inplace=True)
            eval_statistic.reset_index(drop=True, inplace=True)
            db.write_evstat(short_name(cam_name), eval_statistic, cwd_path, mode='replace')

        elif set(cur_eval_days) != set(all_real_days):
            eval_statistic = cur_eval_statistic[cur_eval_statistic['date'].isin(all_real_days_dt)].copy()
            eval_statistic.sort_values('date', inplace=True)
            eval_statistic.reset_index(drop=True, inplace=True)
            db.write_evstat(short_name(cam_name), eval_statistic, cwd_path, mode='replace')

    else:
        mean_threshold, window_next = params[cam_name]
        auto_visitors = pd.DataFrame()
        for day in all_real_days:
            cam_shapes = db.read_shapes(cam_name, cwd_path)
            new_shapes = dt_slice_shape_df(cam_shapes, day, day)
            new_shapes['cam_name'] = cam_name
            day_visitors = visitors_counting(cam_name, new_shapes, day, mean_threshold, window_next, cwd_path=cwd_path)
            day_visitors['date'] = pd.to_datetime(day_visitors['date'])
            auto_visitors = pd.concat([auto_visitors, day_visitors])

        if len(auto_visitors) != 0:
            all_real_visitors.sort_values('date', inplace=True)
            all_real_visitors.reset_index(drop=True, inplace=True)

            auto_visitors.sort_values('date', inplace=True)
            auto_visitors.reset_index(drop=True, inplace=True)
            auto_visitors['*'] = all_real_visitors['*']

            auto_visitors['s'] = 'auto'
            all_real_visitors['s'] = 'real'

            # Error calculation, data aggregation and storage
            all_real_visitors['err'] = all_real_visitors['sum'] - auto_visitors['sum']
            all_real_visitors['mape'] = round(abs(all_real_visitors['err']) / all_real_visitors['sum'], 2)

            auto_visitors['err'] = all_real_visitors['sum'] - auto_visitors['sum']
            auto_visitors['mape'] = round(abs(all_real_visitors['err']) / all_real_visitors['sum'], 2)

            all_real_visitors.index = list(range(0, len(all_real_visitors)*2, 2))
            auto_visitors.index = list(range(1, len(auto_visitors)*2, 2))

            eval_statistic = pd.concat([all_real_visitors, auto_visitors]).sort_index()
            eval_statistic['mape'] = eval_statistic['mape'].apply(lambda x: str(x).replace('.', ','))
            eval_statistic['mape'] = eval_statistic['mape'].replace('nan', '0,0')
            eval_statistic['mape'] = eval_statistic['mape'].fillna('0,0')
            db.write_evstat(short_name(cam_name), eval_statistic, cwd_path, mode='replace')

    # Updating visitors data using manual data
    cam_visitors = db.read_visitors(short_name(cam_name), cwd_path)
    if not cam_visitors.empty:
        all_real_visitors['s'] = 'real'
        all_real_visitors = all_real_visitors[cam_visitors.columns]
        all_real_visitors.set_index('date', inplace=True)
        cam_visitors.set_index('date', inplace=True)
        cam_visitors.update(all_real_visitors)
        cam_visitors.reset_index(inplace=True)
        db.write_visitors(short_name(cam_name), cam_visitors, cwd_path, mode='replace')


if __name__ == '__main__':
    cwd_path = os.getcwd()
    app_name = get_app_name()
    text_params_path = os.path.join(cwd_path, f'{app_name}_request_app_description.txt')
    text_program_status_path = os.path.join(cwd_path, f'{app_name}_program_status.txt')

    camconfig = load_camconfig()

    if not os.path.exists(text_params_path):
        create_txt_params(text_params_path, camconfig, DESCRIPTION)
    else:
        txt_params = read_txt_params(text_params_path)

        create_txt_program_status(text_program_status_path, msg='Ждите...')

        for cam_name in txt_params:
            print(cam_name)
            evaluation(cam_name, txt_params, camconfig, cwd_path)

        for cam_name in txt_params:
            for cam_set in camconfig:
                if cam_set['cam_name'][:-1] == cam_name[:-1]:
                    cam_set['vis_count_alg'] = txt_params[cam_name]
        save_camconfig(camconfig)

        create_txt_program_status(text_program_status_path, msg='Готово!')

