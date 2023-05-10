import os
import sys
import streamlit as st
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import mlflow
from mlflow.tracking.client import MlflowClient
import joblib
from sqlalchemy import create_engine
import pymysql
import mysql.connector as connection
import seaborn as sns
import datetime

# Title
st.header("Streamlit Machine Learning App")


class MultiApp:
    def __init__(self):
        self.apps = []
        self.app_dict = {}

    def add_app(self, title, func):
        if title not in self.apps:
            self.apps.append(title)
            self.app_dict[title] = func

    def run(self):
        title = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda title: str(title))
        self.app_dict[title]()



def foo():
    st.title("Page1")
    
    st.session_state.uploaded_csv = st.file_uploader('選擇您要上傳的CSV檔')
    if st.session_state.uploaded_csv is not None:
       st.header('您所上傳的CSV檔內容：')
       #global df
       df = pd.read_csv(st.session_state.uploaded_csv)
       st.session_state.file_name = st.session_state.uploaded_csv.name
       st.write(st.session_state.file_name)
       #input_csv=df.to_dict(orient = 'records')
       with st.expander("內容顯示"):
          st.dataframe(df)
          st.session_state.df=df
       st.session_state.col1, st.session_state.col2 = st.columns(2)
       col()
    
    #input_csv=df
    
    
    
def bar():
    st.title("Page2")
    #try:
    #global input_df
    #input_df=pd.DataFrame(input_csv)
    #try:
    Linear(st.session_state.df, st.session_state.input_x,st.session_state.input_y, st.session_state.input_split)
    input_testx = st.number_input('Insert x:')
    input_testy = st.number_input('Insert y:')
    a = np.array([[input_testx,input_testy]]) 
    c=a.reshape(-1, 1)
    if st.button('Predict'):
        cost = inference(c)
        st.write('The result is:')
        st.text(cost)
        getresultQuery()
    if st.button('Save'):
       insertDataset()
    title = st.text_input('What time do you want delete?')
    if st.button('Delete'):
       deleteDataset(title)
    if st.button('Show Data'):
       getresultQuery()
    query = st.text_input('What time do you want query?')
    if st.button('Select'):
       result=QueryData(query)

    #if st.button('To CSV'):
    #   st.session_state.result_dataFrame.to_csv('Test.csv')
    #   st.write("CSV OK!")
    #except ValueError:
       #st.write('Cannot make linear regression! Please change values.')
    


    
def col():
   
   #st.session_state.input_df=pd.DataFrame(input_csv)
   with st.session_state.col1:
      option1 = st.selectbox(
    '   How would you choose?X:',
       (st.session_state.df.columns))
      st.write('You selected X is:', option1)
      with st.expander("內容顯示"):
        df_result_search1 = st.session_state.df[option1]
        st.dataframe(df_result_search1)
   with st.session_state.col2:
      option2 = st.selectbox(
       'How would you choose?Y:',
       (st.session_state.df.columns))
      st.write('You selected Y is:', option2)
      with st.expander("內容顯示"):
        df_result_search2 = st.session_state.df[option2]
        st.dataframe(df_result_search2)
   st.subheader('訓練集劃分')
   number = st.number_input("請輸入訓練集所佔比例：",min_value=0.5,max_value=0.9,value=0.8,step=0.1)
   split = int(number * len(st.session_state.df))
   st.write("選擇的數據集大小：",len(st.session_state.df))
   st.write("訓練集大小：",split)
   st.write("預測集大小：",len(st.session_state.df)-split)
   st.session_state.input_x = option1
   st.session_state.input_y = option2
   st.session_state.input_split = split
   st.line_chart(data = st.session_state.df,x=st.session_state.input_x,y=st.session_state.input_y)
   

   
       



def Linear(df, option1, option2, split):
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=[option1, option2])

    for i in range(0,len(data)):
         new_data[option1][i] = data[option1][i]
         new_data[option2][i] = data[option2][i]

    #split into train and validation
    train = new_data[:split]
    valid = new_data[split:]

    x_train = train.drop(option1, axis=1)
    y_train = train[option1]
    x_valid = valid.drop(option1, axis=1)
    y_valid = valid[option1]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    
    # Use the experiment notebook path to get the experiment ID
    experiment_name = 'my-example'
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="my-example") as run:
     model = LinearRegression()
     model.fit(x_train,y_train)

     preds = model.predict(x_valid)
     rmse = np.sqrt(np.mean(np.power((np.array(y_valid)-np.array(preds)),2)))

     valid['Predictions'] = 0
     valid['Predictions'] = preds

     valid.index = new_data[split:].index
     train.index = new_data[:split].index

     append_data = DataFrame(data={option1:[],'Predictions':[]})

     append_data[option1] = train[option1]
     #append_data[option2] = train[option2]
     append_data['Predictions'] = train[option1]

     pic = pd.concat([append_data[[option1,'Predictions']],valid[[option1,'Predictions']]],axis=0)
     joblib.dump(model, "lr_model.sav")

     st.line_chart(pic)
     (rmse, mae, r2) = eval_metrics(y_valid, preds)
     mlflow.log_param("alpha", alpha)
     mlflow.log_param("l1_ratio", l1_ratio)
     mlflow.log_metric("rmse", rmse)
     mlflow.log_metric("r2", r2)
     mlflow.log_metric("mae", mae)
     st.write("  RMSE: %s" % rmse)
     st.write("  MAE: %s" % mae)
     st.write("  R2: %s" % r2)
     mlflow.sklearn.log_model(model, "mymodel")
     st.session_state.lr_list=[]
     st.session_state.lr_list.append(st.session_state.file_name)
     st.session_state.lr_list.append(rmse)
     st.session_state.lr_list.append(mae)
     st.session_state.lr_list.append(r2)
     st.session_state.lr_list.append(datetime.datetime.now())
     st.write(st.session_state.lr_list)
     


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2



def inference(num1):
    model=joblib.load('lr_model.sav')
    result=model.predict(num1)
    return result

def getresultQuery():
    #資料表相關操作
    
    conn=getsqlconnection()
    sql = "SELECT * FROM lrdata;"
    df=pd.read_sql(sql,conn)
    st.dataframe(df)

def insertDataset():
    conn=getsqlconnection()
    cursor = conn.cursor()
    sql = """INSERT INTO lrdata(DATA_NAME,
         RMSE, MAE, R2,TEST_TIME)
        VALUES (%s, %s, %s, %s, %s )"""
    try:
       cursor.execute(sql,st.session_state.lr_list)
       conn.commit()
    except:
       conn.rollback()
    conn.close()

def deleteDataset(text):
    conn=getsqlconnection()
    cursor = conn.cursor()
    sql = "DELETE FROM lrdata WHERE TEST_TIME=%s"
    text=(str(text),)
    try:
       cursor.execute(sql,text)
       conn.commit()
    except:
       conn.rollback()
    conn.close()

def QueryData(text):
    conn=getsqlconnection()
    cursor = conn.cursor()
    sql = """SELECT * FROM lrdata 
             WHERE TEST_TIME = %s""" 
    cursor.execute(sql,text)
    df = pd.DataFrame(cursor.fetchall(),columns=('DATA_NAME','RMSE', 'MAE','R2','TEST_TIME'))
    st.dataframe(df)
    #st.write(df['TEST_TIME'])
    conn.close()
    

def createData():
    # 使用cursor()方法获取操作游标 
    conn=getsqlconnection()
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE IF EXISTS lrdata")
    sql = """CREATE TABLE lrdata (
         DATA_NAME  CHAR(20) NOT NULL,
         RMSE  FLOAT,
         MAE FLOAT,  
         R2 FLOAT,
         TEST_TIME
         )"""
    try:
       cursor.execute(sql)
       conn.commit()
    except:
       conn.rollback()
    conn.close()

def getsqlconnection():
   # 資料庫設定
   db_settings = {
    "host": "127.0.0.1",#"localhost"
    "port": 3306,
    "user": "root",
    "password": "19881027",
    "db": "mytest",
    "charset": "utf8"
    }
   try:
       # 建立Connection物件
       conn = pymysql.connect(**db_settings)
       
       # 建立Cursor物件
       return conn
   except Exception as ex:
       print(ex)


app = MultiApp()

app.add_app("Page1", foo)
app.add_app("Page2", bar)
app.run()