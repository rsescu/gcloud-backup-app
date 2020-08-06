#!/usr/bin/env python
import sys
assert sys.version_info >= (3, 0)
import os
from zipfile import ZipFile
import uuid
import fingerprint as fgp
from gdrive import GDriveClient

BAKCUP_KEY = 'backup'
RESTORE_KEY = 'restore'




def check_root():
    if os.geteuid() != 0:
        print("Not running as root, please be mindful of permissions")


def pack_files(file_list):
    random_id = str(uuid.uuid4())
    with ZipFile(random_id + '.zip', 'w') as zip_obj:
        # Add multiple files to the zip
        for file in file_list:
            zip_obj.write(file)
        zip_obj.close()
    return random_id


def unpack_files(archive_name):
    # path = ""
    with ZipFile(archive_name, 'r') as zip_obj:
        # Extract all the contents of zip file in current directory
        zip_obj.extractall()


def main():
    client = GDriveClient('credentials.json')
    client.read()
    # argv = sys.argv
    # if BAKCUP_KEY in argv and RESTORE_KEY in argv:
    #     print("Must either run in backup mode or restore mode.\nFor usage details run --help")
    #     sys.exit()
    # # read fingerprint
    # fingerprint = fgp.read_fingerprint()
    # print("fingeprint acquired")
    # if 'backup' in argv:
    #     print(argv)
    #     generated_id = pack_files(argv[2:])
    #     print(generated_id)
    # elif 'restore' in argv:
    #     print('restore')
    #     # should get id from cloud
    #     unpack_files(argv[2])
    # else:
    #     print('usage:')
    #
    # print('restore' in argv)
    # print('backup' in argv)
    # gdrive_auth.get_gdrive_service()

    # backup()


if __name__ == '__main__':
    main()
