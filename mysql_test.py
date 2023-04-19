import streamlit as st
import pandas as pd
import pymysql
import mysql.connector

connect_db = pymysql.connect(host = 'localhost', port=3306, user='root', passwd='19881027', charset='utf8',db='mytest')

with connect_db.cursor() as cursor:
    sql = """
    CREATE TABLE IF NOT EXISTS Member(
    Nid int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name varchar(20),
    Age int(6),
    Date date
    );
    """
    # 執行 SQL指令
    cursor.execute(sql)
    # 提交至SQL
    connect_db
connect_db.close()

st.title('mySQL testing')
#在網頁呈現 h1 大小的文字
st.header('mysql')


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from mytable;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")






text_input = st.text_input("Insert a text")
st.write("You entered: ", text_input)
number = st.number_input('Insert a number')
st.write('The current number is ', number)
d = st.date_input('Insert your birthday')
st.write('Your birthday is:', d)
#在網頁將pandas的DF顯示出來
df = pd.DataFrame(dict(a=[1, 2, 4], b=[3, 1, 7]))
st.dataframe(df) 
st.line_chart(df)