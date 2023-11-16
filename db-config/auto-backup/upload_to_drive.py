import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from datetime import datetime, timedelta

datetime_now = datetime.now().strftime('%d%m%Y %H:%M:%S')


def writeLog(status, message):
    path_file_log = f'{os.path.abspath(sys.argv[0])[:-2]}log'
    result = f'[{datetime_now}] {status}: {message}\n'

    with open(path_file_log, 'a') as file_log:
        file_log.write(result)
    
    print(result)


def counting_days(items):
    try:
        under_seven_days = []
        over_seven_days = []

        for item in items:
            tgl = item['name'].split('-')[1].split('.')[0]
            tgl_obj = datetime.strptime(tgl, "%d%m%Y")
            tgl_range = tgl_obj + timedelta(days=7)
            tgl_today = datetime.now()

            if tgl_range < tgl_today:
                over_seven_days.append(item)
            else:
                under_seven_days.append(item)

        return over_seven_days, under_seven_days
    except Exception as e:
        writeLog('Gagal counting days', e)


def deleteLocalFiles(path, filenames):
    try:
        for filename in filenames:
            os.remove(f"{path}/{filename['name']}")
    except Exception as e:
        writeLog('Gagal delete local files', e)


def uploadFile(service, folder_id):
    try:
        upload_path_file = '.'
        upload_filename = 'DbAbsensi-'

        cloud_files = [
            {'name': file['name']} for file in getAllCloudFiles(service, folder_id)
        ]
        local_files = [
            {'name': file} for file in os.listdir(upload_path_file) if upload_filename in file
        ]

        filesNotInCloud = [
            item for item in local_files if item not in cloud_files
        ]
        filesInCloud = [
            item for item in local_files if item in cloud_files
        ]

        deleteLocalFiles(upload_path_file, filesInCloud)

        over_seven_days, under_seven_days = counting_days(filesNotInCloud)

        deleteLocalFiles(upload_path_file, over_seven_days)

        for file in under_seven_days:
            file_metadata = {
                'name': file['name'],
                'parents': [folder_id]
            }

            media_file = MediaFileUpload(
                f'{upload_path_file}/{file["name"]}',
                mimetype='application/sql',
                resumable=True
            )

            service.files().create(body=file_metadata, media_body=media_file).execute()

    except Exception as e:
        writeLog(f'Gagal upload file: {e}')


def createFolder(service, folder_name):
    try:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'spaces': 'drive'
        }

        result = service.files().create(body=folder_metadata).execute()
        return result['id']
    except Exception as e:
        writeLog('Gagal create folder', e)


def getFolderId(service, folder_name):
    try:
        results = service.files().list(
            fields="nextPageToken, files(id, name)",
            q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false",
        ).execute()

        items = results.get('files')

        if not items:
            return None

        return items[0]['id']
    except Exception as e:
        writeLog('Gagal get folder id', e)


def getAllCloudFiles(service, folder_id):
    try:
        result = service.files().list(
            fields="files(id, name, parents)",
            q=f"parents='{folder_id}' and trashed=false"
        ).execute()
        return result.get('files')
    except Exception as e:
        writeLog('Gagal get all cloud files', e)


def getExpiredFiles(service, folder_id):
    try:
        result = service.files().list(
            fields="files(id, name, parents)",
            q=f"parents='{folder_id}' and trashed=false"
        ).execute()

        items = result.get('files')

        if items.__len__() <= 7:
            return None
        else:
            over_seven_days, _ = counting_days(items)
            return [item['id'] for item in over_seven_days]
    except Exception as e:
        writeLog('Gagal get expired files', e)


def deleteCloudFile(service, file_id):
    try:
        result = service.files().update(
            fileId=file_id,
            body={'trashed': True}
        ).execute()

        return result
    except Exception as e:
        writeLog('Gagal delete cloud file', e)


def getCredentials():
    try:
        creds = None
        path_file_client_secret = 'client_secret_desktop_app.json'
        path_file_token = 'token.json'

        SCOPES = [
            'https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive.file'
        ]

        if os.path.exists(path_file_token):
            creds = Credentials.from_authorized_user_file(
                path_file_token, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    path_file_client_secret,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(path_file_token, 'w') as token:
                token.write(creds.to_json())

        return creds
    except Exception as e:
        writeLog('Gagal get credentials', e)


def main():
    creds = getCredentials()
    folder_name = 'backup-db-absensi'

    try:
        service = build('drive', 'v3', credentials=creds)

        folder_id = getFolderId(service, folder_name)
        if folder_id is None:
            folder_id = createFolder(service, folder_name)

        uploadFile(service, folder_id)

        files_id = getExpiredFiles(service, folder_id)

        if files_id is not None:
            for file_id in files_id:
                deleteCloudFile(service, file_id)

        writeLog('Success', 'Done')

    except Exception as e:
        writeLog('Error', e)


if __name__ == '__main__':
    main()
