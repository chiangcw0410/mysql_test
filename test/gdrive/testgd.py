from pydrive2.auth import GoogleAuth
import os
from pydrive2.drive import GoogleDrive
import csv
import json
import pandas as pd
from tqdm import tqdm
import io

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.

drive = GoogleDrive(gauth)


"""
test_list=[]
with open('winequality-red.csv','r', newline='') as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
          test_list.append(row)
          
file1 = drive.CreateFile({'title':'test.csv', 'mimeType':'application/csv'})
file1.SetContentString(str(test_list))
file1.Upload()
"""

"""

file4 = drive.CreateFile({'title':'appdata.json', 'mimeType':'application/json'})
file4.SetContentString('{"firstname": "John", "lastname": "Smith"}')
file4.Upload() # Upload file.
"""

"""

file5 = drive.CreateFile({'title':'appdata.csv', 'mimeType':'application/csv'})
file5.SetContentString('No, Name, Score')
file5.Upload() # Upload file.
"""
print("=================================")
#列出文件
# Auto-iterate through all files that matches this query
select=''
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
  print('title: %s, id: %s' % (file1['title'], file1['id']))
  if 'csv' in file1['title'] :# 讀取csv
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
  elif 'json' in file1['title'] :# 讀取json
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
  elif 'txt' in file1['title'] :# 讀取txt
    content = file1.GetContentString(file1['title'])
    print(content)

print("=================================")
