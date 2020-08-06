import os
import sys
import uuid
APP_NAME = 'gdrive_backup'
FINGERPRINT_PATH_UNIX = os.path.expanduser("~") + '/.config/' + APP_NAME
FINGERPRINT_PATH_WIN = '%PROGRAMDATA%\\' + APP_NAME+ '\config'
FILENAME = 'fingerprint'
PATH = (FINGERPRINT_PATH_UNIX if os.name == 'posix' else FINGERPRINT_PATH_WIN) + os.path.sep
FILE_PATH=PATH + FILENAME

def read_fingerprint():
    try:
        file = open(FILE_PATH, "r")
        fingerprint_id = file.read()
        file.close()
    except IOError:
        # no file found; might be new system that didn't do any backups yet
        fingerprint_id = __write_fingerprint()
    return fingerprint_id


def __write_fingerprint():
    try:
        fingerprint_id = str(uuid.uuid4())
        file = open(FILE_PATH, "w")
        file.write(fingerprint_id)
        file.close()
        print(f"created fingerprint {fingerprint_id} for this machine")
    except IOError:
        print("Can't create fingerprint file for some reason... terminating")
        sys.exit()
    return fingerprint_id
