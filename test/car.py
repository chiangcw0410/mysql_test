import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

uploaded_csv = st.file_uploader('選擇您要上傳的CSV檔')

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.header('您所上傳的CSV檔內容：')
    st.dataframe(df)


option1 = st.selectbox(
    'How would you choose?X:',
    ('car_ID','symboling','CarName','fueltype','aspiration','doornumber',
       'carbody','drivewheel','enginelocation','wheelbase','carlength','carwidth',
       'carheight','curbweight','enginetype','cylindernumber','enginesize','fuelsystem',
       'boreratio','stroke','compressionratio','horsepower','peakrpm','citympg','highwaympg','price'))



st.write('You selected X is:', option1)
df_result_search1 = df[option1]
st.dataframe(df_result_search1)

option2 = st.selectbox(
    'How would you choose? Y:',
    ('car_ID','symboling','CarName','fueltype','aspiration','doornumber',
       'carbody','drivewheel','enginelocation','wheelbase','carlength','carwidth',
       'carheight','curbweight','enginetype','cylindernumber','enginesize','fuelsystem',
       'boreratio','stroke','compressionratio','horsepower','peakrpm','citympg','highwaympg','price'))



st.write('You selected Y is:', option2)
df_result_search2 = df[option2]
st.dataframe(df_result_search2)
