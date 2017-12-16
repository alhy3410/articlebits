import pymysql.cursors
from credentials import password,user

connection = pymysql.connect(host='localhost',
                             user=user,
                             password=password,
                             db='news_scanner',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
