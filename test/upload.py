import streamlit as st
import pandas as pd

st.title("Upload CSV project")

uploaded_csv = st.file_uploader('選擇CSV檔')

if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv,encoding='utf-8')
    st.header('CSV檔內容：')
    st.dataframe(df)