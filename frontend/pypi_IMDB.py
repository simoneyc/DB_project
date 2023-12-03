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

# �]�w��Ʈw�s����T
db_config = {
    'host': 'localhost',
    'user': 'root@localhost',
    'password': 'your_password',
    'database': 'your_database',
}

# �}�Ҹ�Ʈw�s��
connection = pymysql.connect(**db_config)

# �Ыش��
cursor = connection.cursor()

# CSV �ɮ׸��|
csv_file_path = 'imdb_top250_movies.csv'

# �}�� CSV �ɮ�
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # Ū�� CSV
    csv_reader = csv.reader(csvfile)
    
    # ���N�C�@�C
    for row in csv_reader:
        # �N��ƴ��J���Ʈw
        cursor.execute("INSERT INTO movies (column1, column2, ..., columnN) VALUES (%s, %s, ..., %s)", row)

# ������
connection.commit()

# ������ЩM�s��
cursor.close()
connection.close()