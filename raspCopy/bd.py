import pymysql
from config import host, user, password, db_name
from array import *

def sql(sql_text):
    try:
        connection = pymysql.connect(
            host = host,
            user = user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_text)
                connection.commit()
                global resullt
                resullt = cursor.fetchall()
        finally:
            connection.close()

    except Exception as ex:
        print("no")
        print(ex)

    return resullt

sql("set names utf8;")
