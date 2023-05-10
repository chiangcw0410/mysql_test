import csv
import pandas as pd
from io import StringIO
from urllib import request
import streamlit as st

url = st.text_input('google 文件網址, 記得改為 public 發布後, 才能讓程式爬取')#"google 文件網址, 記得改為 public 發布後, 才能讓程式爬取"

def read_file(self, filename):
  self.response.write('Reading the full file contents:\n')

  gcs_file = gcs.open(filename)
  contents = gcs_file.read()
  gcs_file.close()
  self.response.write(contents)



if st.button('read url'):
    s = request.urlopen(url).read().decode('utf8')  # 1 读取数据串

    dfile = StringIO(s)      # 2 将字符串转换为 StringIO对象，使其具有文件属性 
    creader = csv.reader(dfile)  # 3 将流 转换为可迭代的 reader（csv row）
    dlists=[rw for rw in creader]  # 4 其他转换、操作
    st.dataframe(dlists)