import pymysql
import logging
import datetime as dt


def connectDb(dbName):
    try:
        mysqldb = pymysql.connect(
           host='127.0.0.1', 
           port=3306, 
           user='root', 
           passwd='19881027', 
           db=dbName, 
           charset='utf8')
        return mysqldb
    except Exception as e:
        logging.error('Fail to connection mysql {}'.format(str(e)))
    return None

def create_table():
    name=input("請輸入欄位一(str):")
    age=input("請輸入欄位二(int):")
    day=input("請輸入欄位三(datetime):")
    sql1 = 'CREATE TABLE users (id AUTO_INCREMENT PRIMARY KEY,,"+name+" VARCHAR(255),"+age+" int(99),"+day+" date);'
    print('table ok!')

def get_insert():
    name=input("請輸入欄位一:")
    age=input("請輸入欄位二:")
    #day=input("輸入日期時間(YYYY-MM-DD hh:mm:ss):")
    sql2 = "INSERT INTO users (id,"+name+","+age+",day)  VALUES (%s, %s,str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" %(name, age,dt.strftime("%Y-%m-%d %H:%M:%S"))
    # '"++"', "+age+", to_date("+birthday+"));
    #day=dt.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(sql2)
    data= cursor.fetchone()     
    return data

def get_staff_info_one():
    
    name=input("請輸入欄位一(str):")
    sql3="SELECT name,age,birthday FROM users WHERE name ='" + name + "'"
    cursor.execute(sql3)
    data= cursor.fetchone()     
    return data


#資料庫連線設定
db = connectDb('mytest')
#建立操作游標
cursor = db.cursor()
#SQL語法（查詢資料庫版本）
sql = 'SELECT VERSION()'
# sql1 = 'CREATE TABLE users (id AUTO_INCREMENT PRIMARY KEY,,name VARCHAR(255),age int(99),birthday date);'

# 'may', 16, '2023/04/10'
#item=int(input(""))
print("建一個table")
create_table()
print("寫一筆資料")
get_insert()
print("查詢資料")
get_staff_info_one()

#關閉連線
db.close()
