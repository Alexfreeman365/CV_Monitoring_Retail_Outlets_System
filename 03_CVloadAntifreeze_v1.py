import subprocess, psutil

from funcs_TxtUI_request_app_description import *

import atexit
atexit.register(cleanup_mei_folders)


def get_loaders(cwd_path):
    exes = [f for f in os.listdir(cwd_path) if f.split('.')[-1] == 'exe']
    hiSDloaders = sorted([f for f in exes if 'hiSDloader' in f])
    hiFTPDloaders = sorted([f for f in exes if 'hiFTPDloader' in f])
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
    cwd_path = os.getcwd()
    app_name = os.path.basename(sys.executable).split('.')[0]

    request = f"Введите данные:\n" \
              f"Интервал запуска загрузчиков (мин)->:\nПериод перезапуска загрузчиков (час)->:\n{'-' * 30}"
    data = request_app_description(app_name, cwd_path, request, DESCRIPTION)
    load_interval, reload_period = data

    try:
        load_interval = int(float(load_interval) * 60)
        reload_period = int(float(reload_period) * 3600)
    except ValueError as e:
        log_event(cwd_path, app_name, 'critical', f"Invalid input parameters: {str(e)}")
        sys.exit(1)

    loaders = get_loaders(cwd_path)
    if not loaders:
        log_event(cwd_path, app_name, 'warning', 'No loaders found')
        sys.exit(0)

    process = start_loaders(cwd_path, loaders, load_interval)

    error_count = 0
    while True:
        try:
            time.sleep(reload_period)

            try:
                kill_loaders(process)
                time.sleep(1)  # Пауза для гарантии освобождения ресурсов
                process = start_loaders(cwd_path, loaders, load_interval)
                log_event(cwd_path, app_name, 'info',
                          f'Restarted: {len(process)} loaders')
                error_count = 0
            except Exception as error:
                error_msg = f"{type(error).__name__}: {str(error)}"
                log_event(cwd_path, app_name, 'error', error_msg)
                error_count += 1
                if error_count > 3:
                    log_event(cwd_path, app_name, 'critical', 'Too many consecutive errors')
                    sys.exit(1)
                continue

        except KeyboardInterrupt:
            kill_loaders(process)
            log_event(cwd_path, app_name, 'info', 'Manual interrupt by user')
            cleanup_mei_folders()
            sys.exit(0)
        except Exception as critical_error:
            kill_loaders(process)
            log_event(cwd_path, app_name, 'critical', f"Fatal: {str(critical_error)}")
            cleanup_mei_folders()
            sys.exit(1)




