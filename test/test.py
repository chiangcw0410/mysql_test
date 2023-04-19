# -*- coding: utf-8 -*-
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import pymysql
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:chiangcw@localhost/python?charset=utf8')
uploaded_file = st.file_uploader("请选择要上传的csv格式表格！")
if uploaded_file is not None:
	df1 = pd.read_csv(uploaded_file)
	AgGrid(df1)
	df1.to_sql(name=str(uploaded_file.name).replace(".csv",""), con=engine, chunksize=1000, if_exists='replace', index=None)
	st.success("上传成功！")

	db = pymysql.connect(host="localhost", user="root", password="abcde", database="python", charset="utf8")
	sql="select * from "+str(uploaded_file.name).replace(".csv","")
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()
	df2=pd.read_sql(sql,con=db)
	st.success("数据库中的表格内容如下")
	st.dataframe(df2)
else:
	st.warning("请上传表格！")