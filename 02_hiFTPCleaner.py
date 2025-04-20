import os
import time
from datetime import datetime, timedelta
import pickle
import ftplib
import sys


def create_txt_window_request(text_note_path):
    if os.path.exists(text_note_path):
        pass
    else:
        f = open(text_note_path, 'x')
        f.close()


def get_window(text_note_path):
    window = str()
    if os.path.exists(text_note_path):
        window = open(text_note_path, 'rb').read().decode('utf8')
    return window


def load_hiFTPconfig(file):
    hiFTPconfig = []
    with open(os.path.join(os.getcwd(), file), 'rb') as data_file:
        hiFTPconfig = pickle.load(data_file)
    return hiFTPconfig


def get_ftp_host_user_pas():
    list_of_datfiles = [f for f in os.listdir(os.getcwd()) if f.split('.')[-1]=='dat']
    ftp_host = str
    ftp_user = str
    ftp_pas = str
    if len(list_of_datfiles) != 0:
        for file in list_of_datfiles:
            try:
                hiFTPconfig = load_hiFTPconfig(file)
                ftp_host = hiFTPconfig[0]['ftp_host']
                ftp_user = hiFTPconfig[0]['ftp_user']
                ftp_pas = hiFTPconfig[0]['ftp_pas']
                break
            except:
                sys.exit(0)
    else:
        sys.exit(0)
    return ftp_host, ftp_user, ftp_pas


def get_cam_names(ftp_host, ftp_user, ftp_pas):
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pas)
    cam_names = ftp.nlst()
    if cam_names[0] == '.':
        path = cam_names[-1]
        cam_names = [i for i in ftp.nlst(path) if i not in ['.', '..', 'System Volume Information']]
    return cam_names


def get_days_dd(ftp_host, ftp_user, ftp_pas, cam_name):
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pas)
    days = [day.split('/')[-1] for day in ftp.nlst(cam_name)
            if day.split('/')[-1].replace('-', '').isdigit()]
    dd = '-' if days and len(days[0].replace('-', '')) != len(days[0]) else ''
    return [day.replace('-', '') for day in days], dd


def get_cams_days_dict(ftp_host, ftp_user, ftp_pas, cam_names):
    cams_days_dict = {}
    for cam_name in cam_names:
        days, dd = get_days_dd(ftp_host, ftp_user, ftp_pas, cam_name)
        cams_days_dict[cam_name] = (days, dd)
    return cams_days_dict


def get_dt_last_day(cams_days_dict):
    last_day = str()
    for cam_name in cams_days_dict.keys():
        days, dd = cams_days_dict[cam_name]
        cam_last_day = max(days)
        if cam_last_day > last_day:
            last_day = cam_last_day
    return datetime.strptime(last_day, '%Y%m%d')


def get_dt_window_range(dt_last_day, window):
    dt_window_range = []
    for days in range(window):
        dt_window_range.append(dt_last_day - timedelta(days=days))
    return dt_window_range[::-1]


def get_cams_out_days_dict(cams_days_dict, df_window_range):
    cams_out_days_dict = {}
    for cam_name in cams_days_dict.keys():
        days, dd = cams_days_dict[cam_name]
        dt_days = [datetime.strptime(d, '%Y%m%d') for d in days]
        dt_out_days = [d for d in dt_days if d not in df_window_range]
        if len(dt_out_days) != 0:
            out_days = [datetime.strftime(d, '%Y%m%d') for d in dt_out_days]
            cams_out_days_dict[cam_name] = (out_days, dd)
    return cams_out_days_dict


def get_day_folders(ftp_host, ftp_user, ftp_pas, cam_name, day, dd):
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pas)
    path = cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:]))
    return [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]


def delete_out_days(ftp_host, ftp_user, ftp_pas, cams_out_days_dict):
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pas)
    for cam_name in cams_out_days_dict.keys():
        days, dd = cams_out_days_dict[cam_name]
        for day in days:
            day_folders = get_day_folders(ftp_host, ftp_user, ftp_pas, cam_name, day, dd)
            for folder in day_folders:
                path = cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:])) + '/' + folder
                file_names = [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]
                for file in file_names:
                    link = path + '/' + file
                    ftp.delete(link)

            try:
                ftp.rmd(cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'images')
            except:
                pass

            try:
                ftp.rmd(cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:])) + '/' + 'record')
            except:
                pass

            try:
                ftp.rmd(cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:])))
            except:
                pass

            try:
                ftp.rmd(cam_name)
            except:
                pass


def create_txt_msg(text):
    with open(os.path.join(os.getcwd(), 'message.txt'), 'w') as f:
        f.write(text)


if __name__ == '__main__':
    cwd_path = os.getcwd() #r'H:\odfr_data\hiFTPCleaner_dlink'
    text_note_path = os.path.join(cwd_path, 'hiFTPCleaner_Days_window_size_request.txt')
    create_txt_window_request(text_note_path)
    note_text = get_window(text_note_path)
    str_window = note_text.split('-')[0]

    try:
        window = int(str_window)
    except:
        sys.exit(0)

    try:
        usb_part = note_text.split('-')[1]
    except:
        usb_part = 0

    if len(str_window) != 0:
        while True:
            try:
                ftp_host, ftp_user, ftp_pas = get_ftp_host_user_pas()
                cam_names = get_cam_names(ftp_host, ftp_user, ftp_pas)
                print(cam_names)

                if usb_part != 0:
                    cam_names = [usb_part+'/'+cam for cam in cam_names]

                if len(cam_names) != 0:
                    cams_days_dict = get_cams_days_dict(ftp_host, ftp_user, ftp_pas, cam_names)
                    dt_last_day = get_dt_last_day(cams_days_dict)
                    dt_window_range = get_dt_window_range(dt_last_day, window)
                    cams_out_days_dict = get_cams_out_days_dict(cams_days_dict, dt_window_range)
                    if len(cams_out_days_dict) != 0:
                        delete_out_days(ftp_host, ftp_user, ftp_pas, cams_out_days_dict)
            except:
                pass

            time.sleep(43200)
            # break
    else:
        sys.exit(0)