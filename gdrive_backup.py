#!/usr/bin/env python
import sys
assert sys.version_info >= (3, 0)
import os
from googleapiclient.http import MediaFileUpload
import gdrive_auth

BAKCUP_KEY = 'backup'
RESTORE_KEY = 'restore'
MIME_TYPE_FOLDER = "application/vnd.google-apps.folder"
WEBDATA_FOLDER_NAME = "web-server-backup"
DATA_FOLDER_NAME = "server-backup"

gdrive_service = gdrive_auth.get_gdrive_service()

def create_folder_if_missing(name):
    folder_id = None
    response = gdrive_service.files().list(q=f"mimeType='{MIME_TYPE_FOLDER}' and name='{name}'",
                                        spaces='appDataFolder',
                                        fields='nextPageToken, files(id, name)').execute()
    results = response.get('files', [])
    number_of_results = len(results)
    if number_of_results == 1:
        print(f"Folder {name} found in appData")
        folder_id = results[0].get('id')
    elif number_of_results > 1:
        raise SystemExit(5)
    else:
        # no folder found; create one
        folder_metadata = {
            "name": name,
            "mimeType": MIME_TYPE_FOLDER,
            'parents': ['appDataFolder']
        }
        # create the folder
        print(f"Creating {name} folder in appData")
        file = gdrive_service.files().create(body=folder_metadata, fields="id").execute()
        folder_id = file.get("id")

    print("Folder ID:", folder_id)
    return folder_id


def upload_file(name, folder, paths):
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": name,
        "parents": [folder],
        "appProperties": dict(paths=paths)
    }

    # # upload
    media = MediaFileUpload('test.txt', mimetype='*/*')
    file = gdrive_service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))

def backup():
    # Call the Drive v3 API
    webdata_folder_id = create_folder_if_missing(WEBDATA_FOLDER_NAME);
    data_folder_id = create_folder_if_missing(DATA_FOLDER_NAME);

    print(f'{WEBDATA_FOLDER_NAME} with id: {webdata_folder_id}')

    results = gdrive_service.files().list(spaces='appDataFolder',
                                   pageSize=10,
                                   fields="nextPageToken, files(id, name)").execute()
    for item in results.get('files', []):
        print(u'{0} ({1})'.format(item['name'], item['id']))

def check_root():
    try:
        os.rename('/etc/foo', '/etc/bar')
    except IOError as e:
        if (e[0] == errno.EPERM):
            print("not runing as root, might not be able to backup files you do not have access to")

def main():
    argv = sys.argv
    if 'backup' in argv and 'restpo':
        print(argv)
    if 'backup' in argv:
        print(argv)
    elif 'restore' in argv:
        print(argv)
        print('restore')
    else:
        print('usage:')
    print('restore' in argv)
    print('backup' in argv)
    # backup()

if __name__ == '__main__':
    main()
