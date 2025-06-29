import numpy as np
from datetime import datetime, timedelta

from funcs_initializer_camconfig_getcamframe import *


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


def find_new_shapes(cam_name, last_cam_visitors_day, camconfig, cwd_path=os.getcwd()):
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


def add_photos_to_noSeller(noSeller_time_cam, ip_cam_data_path):
    noSeller_time_cam['photos'] = 0

    def get_day_photos(row):
        day = ''.join(str(row['date'])[:10].split('-'))
        day_photo_path = os.path.join(ip_cam_data_path, day)
        return len([p for p in os.listdir(day_photo_path)])

    noSeller_time_cam['photos'] = noSeller_time_cam.apply(get_day_photos, axis=1)
    return noSeller_time_cam


def vis_count_noseller_pipeline(cam_name, ip_cam_data_path, cwd_path=os.getcwd()):
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
        noSeller_time_cam = add_photos_to_noSeller(noSeller_time_cam, ip_cam_data_path)

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