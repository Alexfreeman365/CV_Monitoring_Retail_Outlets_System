import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# import sys


def load_camconfig():
    camconfig = []
    if os.path.exists(os.path.join(cwd_path, 'db', 'camconfig.csv')):
        camconfig = pd.read_csv(os.path.join(cwd_path, 'db', 'camconfig.csv'))
        camconfig = camconfig.to_dict(orient='records')
    return camconfig


def save_camconfig(camconfig):
    camconfig = pd.DataFrame(camconfig)
    camconfig.to_csv(os.path.join(cwd_path, 'db', 'camconfig.csv'), index=False)


def create_txt_params(text_path, camconfig):
    with open(text_path, 'w', encoding='utf-8') as f:
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
    lines = list(map(str.strip, lines))
    params = {}
    for l in lines:
        cam_name, dirty_params = l.split(':')
        params[cam_name] = tuple(map(int, dirty_params.strip(' ()').split(', ')))
    return params


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


def dt_slice_shape_df(df_cam, dt_start, dt_end):
    df = df_cam.copy()
    dt_end_full = str(int(dt_end) + 1)
    df['dt'] = df['uid8'].apply(lambda x: str(x)[:10])
    return df[(df['dt'] >= dt_start) & (df['dt'] < dt_end_full)].iloc[:, 0:-1]


def find_new_shapes(cam_name, last_cam_visitors_day):
    next_cam_visitors_day = datetime.strptime(last_cam_visitors_day, '%y%m%d') #+ timedelta(days=1)
    str_next_cam_visitors_day = datetime.strftime(next_cam_visitors_day, '%y%m%d')
    print(str_next_cam_visitors_day)

    cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
    cam_shapes = cam_shapes.sort_values('origin_file_name')
    cam_shapes = cam_shapes.reset_index(drop=True)
    cam_shapes.to_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'), index=False)
    cam_shapes['cam_name'] = cam_name

    new_shapes = dt_slice_shape_df(cam_shapes, str_next_cam_visitors_day, str_next_cam_visitors_day)
    new_shapes = new_shapes.sort_values('origin_file_name')
    new_shapes = new_shapes.reset_index(drop=True)
    return new_shapes, next_cam_visitors_day


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


def evaluation(cam_name, params, camconfig):
    # Reading manual data
    xls = pd.ExcelFile(os.path.join(cwd_path, 'db', '1_real_viscount.xlsx'))
    all_real_visitors = pd.read_excel(xls, short_name(cam_name))
    xls.close()
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
        cur_eval_statistic = pd.read_csv(os.path.join
                                         (cwd_path, 'db', f'{short_name(cam_name)}_evstat.csv'),
                                         parse_dates=['date'])
        cur_eval_days_dt = np.unique(cur_eval_statistic['date'].dt.date)
        cur_eval_days = list(map(dt_to_str, cur_eval_days_dt))
        exist_eval_days = sorted(list(set(cur_eval_days) & set(all_real_days)))
        new_real_days = sorted(list(set(all_real_days) - set(exist_eval_days)))

        mean_threshold, window_next = cur_params
        auto_visitors = pd.DataFrame()
        for day in new_real_days:
            cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
            new_shapes = dt_slice_shape_df(cam_shapes, day, day)
            new_shapes['cam_name'] = cam_name
            day_visitors = visitors_counting(cam_name, new_shapes, day, mean_threshold, window_next)
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
            eval_statistic.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_evstat.csv'), index=False)

        elif set(cur_eval_days) != set(all_real_days):
            eval_statistic = cur_eval_statistic[cur_eval_statistic['date'].isin(all_real_days_dt)].copy()
            eval_statistic.sort_values('date', inplace=True)
            eval_statistic.reset_index(drop=True, inplace=True)
            eval_statistic.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_evstat.csv'), index=False)

    else:
        mean_threshold, window_next = params[cam_name]
        auto_visitors = pd.DataFrame()
        for day in all_real_days:
            cam_shapes = pd.read_csv(os.path.join(cwd_path, 'db', f'{cam_name}_shapes_locs.csv'))
            new_shapes = dt_slice_shape_df(cam_shapes, day, day)
            new_shapes['cam_name'] = cam_name
            day_visitors = visitors_counting(cam_name, new_shapes, day, mean_threshold, window_next)
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
            eval_statistic.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_evstat.csv'), index=False)

    # Updating visitors data using manual data
    if os.path.exists(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv')):
        cam_visitors = pd.read_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv'))
        all_real_visitors['s'] = 'real'
        all_real_visitors = all_real_visitors[cam_visitors.columns]
        all_real_visitors.set_index('date', inplace=True)
        cam_visitors.set_index('date', inplace=True)
        cam_visitors.update(all_real_visitors)
        cam_visitors.reset_index(inplace=True)
        cam_visitors.to_csv(os.path.join(cwd_path, 'db', f'{short_name(cam_name)}_visitors.csv'), index=False)


if __name__ == '__main__':
    cwd_path = r'L:\Active_pjs\RG' # os.getcwd()
    camconfig = load_camconfig()
    text_params_path = os.path.join(cwd_path, 'SysViscountEval_current_params.txt')
    text_program_status_path = os.path.join(cwd_path, 'SysViscountEval_program_status.txt')

    if not os.path.exists(text_params_path):
        create_txt_params(text_params_path, camconfig)
    else:
        txt_params = read_txt_params(text_params_path)

        create_txt_program_status(text_program_status_path, msg='Ждите...')

        for cam_name in txt_params:
            evaluation(cam_name, txt_params, camconfig)

        for cam_name in txt_params:
            for cam_set in camconfig:
                if cam_set['cam_name'][:-1] == cam_name[:-1]:
                    cam_set['vis_count_alg'] = txt_params[cam_name]
        save_camconfig(camconfig)

        create_txt_program_status(text_program_status_path, msg='Готово!')

