from __future__ import print_function
import pandas as pd
import streamlit as st

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

GOOGLE_APPLICATION_CREDENTIALS = './credentials.json'

def search_file():
    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        files = []
        page_token = None
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                   'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                st.write(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        st.write(F'An error occurred: {error}')
        files = None

    return files

def connect_google_drive_api():
        
    # use Gdrive API to access Google Drive
    from pydrive2.auth import GoogleAuth
    from pydrive2.drive import GoogleDrive
    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script    
    
    drive = GoogleDrive(gauth)
    st.write('connect_google_drive_api!')
    return drive

connect_google_drive_api()
#data = pd.read_csv('/content/drive/MyDrive/winequality-white.csv')

#downloaded = connect_google_drive_api.drive.CreateFile({'id': data.get('id')})
#print('Downloaded content "{}"'.format(downloaded.GetContentString()))
#st.dataframe(data)

search_file()