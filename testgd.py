from pydrive2.auth import GoogleAuth
import os
from pydrive2.drive import GoogleDrive
import csv
import json
import pandas as pd

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)

#file1 = drive.CreateFile({'title': 'winequality-red.csv'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
#file1.SetContentString('Hello World!') # Set content of the file from given string.
#file1.Upload()
test_list=[]
with open('winequality-red.csv', 'r') as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
          test_list.append(row)
file1 = drive.CreateFile({'title': 'test.csv', 'mimeType':'application/csv'})
for i in  test_list:
   file1.SetContentString(i)
   file1.Upload()
"""
file4 = drive.CreateFile({'title':'appdata.json', 'mimeType':'application/json'})
file4.SetContentString('{"firstname": "John", "lastname": "Smith"}')
file4.Upload() # Upload file.
file4.SetContentString('{"firstname": "Claudio", "lastname": "Afshar"}')
file4.Upload() # Update content of the file.
"""
"""
file5 = drive.CreateFile({'title':'appdata.csv', 'mimeType':'application/csv'})
file5.SetContentString('No, Name, Score')
file5.Upload() # Upload file.
file5.SetContentString('1, Tom, 87.3')
file5.Upload() # Update content of the file.
"""
print("=================================")
#列出文件
# Auto-iterate through all files that matches this query
select=''
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
  print('title: %s, id: %s' % (file1['title'], file1['id']))
  if 'csv' in file1['title'] :
    file1.GetContentFile(file1['title'])
    file2 = drive.CreateFile({'id': file1['id']})
    try:
      file2.GetContentFile(file1['title'])
      with open(file1['title'], 'r') as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
          print(row)
      
    except Exception as e:
      print(e, type(e))
  elif 'json' in file1['title'] :
    file1.GetContentFile(file1['title'])
    file2 = drive.CreateFile({'id': file1['id']})
    try:
      file2.GetContentFile(file1['title'])
      with open(file1['title']) as f:
           data = json.load(f)
           print(data.keys())
           print(data.values())
      
    except Exception as e:
      print(e, type(e))
  elif 'txt' in file1['title'] :
    content = file1.GetContentString(file1['title'])
    print(content)

print("=================================")
#創建文件夾
def create_folder(parent_folder_id, subfolder_name):
  newFolder = drive.CreateFile({'title': subfolder_name, "parents": [{"kind": "drive#fileLink", "id": \
  parent_folder_id}],"mimeType": "application/vnd.google-apps.folder"})
  newFolder.Upload()
  return newFolder

#通過文件標題返回文件 ID 
def get_id_of_title(title,parent_directory_id):
  foldered_list=drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
  for file in foldered_list:
    if(file['title']==title):
      return file['id']
    return None
