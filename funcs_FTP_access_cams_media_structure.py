import os
import pickle
import sys
import ftplib
from datetime import datetime


def load_hiFTPconfig(file, path=os.getcwd()):
    hiFTPconfig = []
    with open(os.path.join(path, file), 'rb') as data_file:
        hiFTPconfig = pickle.load(data_file)
    return hiFTPconfig


def get_ftp_host_user_pas(path=os.getcwd()):
    list_of_datfiles = [f for f in os.listdir(path) if f.split('.')[-1]=='dat']
    ftp_host = str
    ftp_user = str
    ftp_pas = str
    if len(list_of_datfiles) != 0:
        for file in list_of_datfiles:
            try:
                hiFTPconfig = load_hiFTPconfig(file, path)
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


def get_day_folders(ftp_host, ftp_user, ftp_pas, cam_name, day, dd):
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_pas)
    path = cam_name + '/' + f'{dd}'.join((day[:4], day[4:6], day[6:]))
    return [f.split('/')[-1] for f in ftp.nlst(path) if len(f) > 3]


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