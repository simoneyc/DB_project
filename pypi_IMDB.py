import requests
from itertools import groupby
import json
import pandas as pd
import os
import getpass
import logging
import traceback
import datetime
import pymysql
import csv

# 設定資料庫連接資訊
db_config = {
    'host': 'localhost',
    'user': 'root@localhost',
    'password': 'your_password',
    'database': 'your_database',
}

# 開啟資料庫連接
connection = pymysql.connect(**db_config)

# 創建游標
cursor = connection.cursor()

# CSV 檔案路徑
csv_file_path = 'imdb_top250_movies.csv'

# 開啟 CSV 檔案
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # 讀取 CSV
    csv_reader = csv.reader(csvfile)
    
    # 迭代每一列
    for row in csv_reader:
        # 將資料插入到資料庫
        cursor.execute("INSERT INTO movies (column1, column2, ..., columnN) VALUES (%s, %s, ..., %s)", row)

# 提交更改
connection.commit()

# 關閉游標和連接
cursor.close()
connection.close()