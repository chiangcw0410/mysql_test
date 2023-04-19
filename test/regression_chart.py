
import os
import warnings
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
 

# Title
st.header("Streamlit Machine Learning App")



def col():
   with col1:
      option1 = st.selectbox(
    '   How would you choose?X:',
       (df.columns))
      st.write('You selected X is:', option1)
      df_result_search1 = df[option1]
      st.dataframe(df_result_search1)


   with col2:
      option2 = st.selectbox(
       'How would you choose?Y:',
       (df.columns))
      st.write('You selected Y is:', option2)
      df_result_search2 = df[option2]
      st.dataframe(df_result_search2)
   st.subheader('訓練集劃分')
   number = st.number_input("請輸入訓練集所佔比例：",min_value=0.5,max_value=0.9,value=0.8,step=0.1)
   split = int(number * len(df))
   st.write("選擇的數據集大小：",len(df))
   st.write("訓練集大小：",split)
   st.write("預測集大小：",len(df)-split)

   st.line_chart(data = df,x=option1,y=option2)
   try:
      st.subheader('線性回歸圖')

      Linear(df, option1, option2, split)
   except ValueError:
       st.write('Cannot make linear regression! Please change values.')
       



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


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

uploaded_csv = st.file_uploader('選擇您要上傳的CSV檔')

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.header('您所上傳的CSV檔內容：')
     
    with st.expander("內容顯示"):
       st.dataframe(df)
    
    col1, col2 = st.columns(2)
    col()
    
    

    



