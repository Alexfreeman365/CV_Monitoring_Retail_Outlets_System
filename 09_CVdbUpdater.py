import os
import shutil
from datetime import datetime
import time
import sys


def create_txt_source_path_request(text_note_path):
    if os.path.exists(text_note_path):
        pass
    else:
        f = open(text_note_path, 'x')
        f.close()


def get_source_db_path(text_note_path):
    source_db_path = str()
    if os.path.exists(text_note_path):
        source_db_path = open(text_note_path, 'rb').read().decode('utf8')
    return source_db_path


# Get file modified time
def getmtime(path):
    return (datetime.fromtimestamp(os.path.getmtime(path))).strftime("%y%m%d%H%M")


def source_file_path(source_db_path, file_name):
    return os.path.join(source_db_path, file_name)


if __name__ == '__main__':
    text_note_path = os.path.join(os.getcwd(), 'CVdbUpdater_Source_path.txt')
    create_txt_source_path_request(text_note_path)
    source_db_path = get_source_db_path(text_note_path)

    if len(source_db_path) != 0:
        if os.path.exists(os.path.join(os.getcwd(), 'db')):
            pass
        else:
            os.mkdir(os.path.join(os.getcwd(), 'db'))

        if len(source_db_path) != 0:
            file_list = [f for f in os.listdir(source_db_path) if
                         os.path.isfile(source_file_path(source_db_path, f))]

            if len(file_list) != 0:
                [shutil.copy2(source_file_path(source_db_path, f), os.path.join(os.getcwd(), 'db'))
                 for f in file_list]

                last_mod_time = max([getmtime(source_file_path(source_db_path, f))
                                    for f in file_list if os.path.isfile(source_file_path(source_db_path, f))])

                while True:
                    time.sleep(5)
                    try:
                        file_list = [f for f in os.listdir(source_db_path) if
                                     os.path.isfile(source_file_path(source_db_path, f))]

                        cur_mod_time = max([getmtime(source_file_path(source_db_path, f))
                                            for f in file_list if os.path.isfile(source_file_path(source_db_path, f))])

                        if cur_mod_time > last_mod_time:
                            [shutil.copy2(source_file_path(source_db_path, f), os.path.join(os.getcwd(), 'db'))
                             for f in file_list]
                            last_mod_time = cur_mod_time
                    except:
                        pass

        else:
            sys.exit(0)
    else:
        sys.exit(0)



