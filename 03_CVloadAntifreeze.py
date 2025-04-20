import os
import subprocess, time, psutil


def get_loaders(cwd_path):
    exes = [f for f in os.listdir(cwd_path) if f.split('.')[-1] == 'exe']
    hiSDloaders = [f for f in exes if 'hiSDloader' in f]
    hiFTPDloaders = [f for f in exes if 'hiFTPDloader' in f]
    loaders = hiSDloaders + hiFTPDloaders
    return loaders


def start_loaders(cwd_path, loaders):
    process = []
    for p in range(len(loaders)):
        proc = subprocess.Popen([os.path.join(cwd_path, loaders[p])], cwd=cwd_path)
        process.append(proc)
    return process


def kill_loaders(process):
    for proc in process:
        pobj = psutil.Process(proc.pid)
        for c in pobj.children(recursive=True):
            c.kill()
        pobj.kill()


if __name__ == '__main__':

    cwd_path = os.getcwd()
    loaders = get_loaders(cwd_path)
    process = start_loaders(cwd_path, loaders)

    while True:
        time.sleep(10800)
        kill_loaders(process)
        process = start_loaders(cwd_path, loaders)

    # try:
    # except KeyboardInterrupt:
    #     print('done')





