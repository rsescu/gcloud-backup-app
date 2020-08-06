from googleapiclient.http import MediaFileUpload

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from fingerprint import PATH
from pathlib import Path


class GDriveClient:
    __MIME_TYPE_FOLDER = "application/vnd.google-apps.folder"
    __WEBDATA_FOLDER_NAME = "web-server-backup"
    __DATA_FOLDER_NAME = "server-backup"

    def __init__(self, credentials_file) -> None:
        super().__init__()
        self.gdrive = Drive(credentials_file).service

    # def backup(self):
        # Call the Drive v3 API
        # webdata_folder_id = self.__create_folder_if_missing(WEBDATA_FOLDER_NAME)
        # data_folder_id = create_folder_if_missing(DATA_FOLDER_NAME)
        #
        # print(f'{WEBDATA_FOLDER_NAME} with id: {webdata_folder_id}')
        #
        # results = gdrive_service.files().list(spaces='appDataFolder',
        #                                       pageSize=10,
        #                                       fields="nextPageToken, files(id, name)").execute()
        # for item in results.get('files', []):
        #     print(u'{0} ({1})'.format(item['name'], item['id']))

    def read(self):
        # Call the Drive v3 API
        webdata_folder_id = self.__create_folder_if_missing(self.__WEBDATA_FOLDER_NAME)
        data_folder_id = self.__create_folder_if_missing(self.__DATA_FOLDER_NAME)

        print(f'{self.__WEBDATA_FOLDER_NAME} with id: {webdata_folder_id}')

        results = self.gdrive.files().list(spaces='appDataFolder',
                                           pageSize=10,
                                           fields="nextPageToken, files(id, name)").execute()
        for item in results.get('files', []):
            print(u'{0} ({1})'.format(item['name'], item['id']))

    def upload_file(self, file, name, folder, paths):
        # TODO look up file versioning

        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": name,
            "parents": [folder],
            "appProperties": dict(paths=paths)
        }

        # # upload
        media = MediaFileUpload(file, mimetype='*/*')
        file = self.gdrive.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def __create_folder_if_missing(self, name):
        folder_id = None
        response = self.gdrive.files().list(q=f"mimeType='{GDriveClient.__MIME_TYPE_FOLDER}' and name='{name}'",
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
                "mimeType": GDriveClient.__MIME_TYPE_FOLDER,
                'parents': ['appDataFolder']
            }
            # create the folder
            print(f"Creating {name} folder in appData")
            file = self.gdrive.files().create(body=folder_metadata, fields="id").execute()
            folder_id = file.get("id")

        print("Folder ID:", folder_id)
        return folder_id




class Drive:
    __SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
                'https://www.googleapis.com/auth/drive.appdata']
    __TOKEN_PICKLE_NAME = 'token.pickle'

    def __init__(self, credentials_file) -> None:
        super().__init__()
        self.credentials_file = credentials_file
        self.service = self.__get_gdrive_service()

    # TODO figure our folder creation for pickle

    def __get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_pickle = PATH + Drive.__TOKEN_PICKLE_NAME
        Path(PATH).mkdir(parents=True, exist_ok=True)
        if os.path.exists(token_pickle):
            with open(token_pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, Drive.__SCOPES)
                creds = flow.run_console()
            # Save the credentials for the next run
            with open(token_pickle, 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)
