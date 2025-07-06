import os
import subprocess, time, psutil

from funcs_TxtUI_request_app_description import *

def get_loaders(cwd_path):
    exes = [f for f in os.listdir(cwd_path) if f.split('.')[-1] == 'exe']
    hiSDloaders = [f for f in exes if 'hiSDloader' in f]
    hiFTPDloaders = [f for f in exes if 'hiFTPDloader' in f]
    loaders = hiSDloaders + hiFTPDloaders
    return loaders


def start_loaders(cwd_path, loaders, load_interval):
    process = []
    for p in range(len(loaders)):
        proc = subprocess.Popen([os.path.join(cwd_path, loaders[p])], cwd=cwd_path)
        process.append(proc)
        time.sleep(load_interval)
    return process


def kill_loaders(process):
    for proc in process:
        try:
            pobj = psutil.Process(proc.pid)
            for c in pobj.children(recursive=True):
                c.kill()
            pobj.kill()
        except psutil.NoSuchProcess:
            continue


DESCRIPTION = (
        'Программа CVloadAntifreeze сначала запускает все загрузчики из текущей папки,\n'        
        'с необходимым интервалом, а затем через заданный период времени перезапускает их,\n'
        'чтобы предотвратить их заморозку в случае отсутствия связи.\n'
    )


if __name__ == '__main__':
    # cwd_path = r'G:\cams_media'
    cwd_path = os.getcwd()
    app_name = '03_CVloadAntifreeze'

    request = f"Введите данные:\n" \
              f"Интервал запуска загрузчиков (мин)->:\nПериод перезапуска загрузчиков (час)->:\n{'-' * 30}"
    data = request_app_description(app_name, cwd_path, request, DESCRIPTION)
    load_interval, reload_period = data
    load_interval, reload_period = int(float(load_interval) * 60), int(float(reload_period) * 3600)

    try:
        loaders = get_loaders(cwd_path)
        process = start_loaders(cwd_path, loaders, load_interval)

        while True:
            time.sleep(reload_period)
            kill_loaders(process)
            process = start_loaders(cwd_path, loaders, load_interval)
    except Exception as error:
        log_event(cwd_path, app_name, 'error', type(error).__name__)




