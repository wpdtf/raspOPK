import pymysql
from datetime import datetime, date
from config import host, user, password, db_name
from config1 import host1, user1, password1, db_name1
from array import *





def clear(group):
    opk_group = []
    def clearem(text):
        name = text
        if name[-1] == "0":
            name = name.split("-0")
            name=name[0]
        return name
    today = date.today()
    for a in group:
        srok = str(a['srok'])
        if a['year'] == int(today.strftime('%Y')):
            if int(today.strftime('%m'))>=8:
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year'])})
        else:
            if (int(today.strftime('%Y')) - a['year']) == (int(srok[0])) and int(today.strftime('%m'))<=7:
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year'])})
            elif (int(today.strftime('%Y')) - a['year']) < (int(srok[0])):
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year'])})
    opk_group = sorted(opk_group, key=lambda x: x['nameGroup'])
    return opk_group

def f2(group,  sotr, spec):
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
            finally:
                connection.close()

        except Exception as ex:
            print("no")
            print(ex)

        return cursor.fetchall()
    sql("truncate table opk_group;")
    sql("truncate table opk_sotr;")
    sql("truncate table opk_spec;")

    for a in group:
        sql(f"insert into opk_group values ({str(a['id'])}, {str(a['spec'])}, '{str(a['nameGroup'])}', {str(a['srok'])});")
    for a in sotr:
        sql(f"insert into opk_sotr values ({str(a['id'])}, '{str(a['name'])}');")
    for a in spec:
        sql(f"insert into opk_spec values ({str(a['id'])}, '{str(a['desc'])}', '{str(a['descs'])}');")


def f1():
    def sql(sql_text):
        try:
            connection = pymysql.connect(
                host = host1,
                user = user1,
                password=password1,
                database=db_name1,
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql_text)
                    connection.commit()
            finally:
                connection.close()

        except Exception as ex:
            print("no")
            print(ex)

        return cursor.fetchall()
    group = sql("select distinct db.group.id, db.group.spec, concat(spec.descs, '-', substring(cast(db.group.year as char(4)), 3, 4), '-', cast(db.group.index as char(1))) as 'nameGroup', srok, year from db.group, spec where db.group.spec = spec.id;")

    sotr = sql("select distinct sotr.id, CONCAT(surname, ' ',substring(name, 1, 1), '. ', substring(otchestvo, 1, 1), '.') as 'name' from db.group, sotr, spec, up, ups, ups_sotr where db.group.spec = spec.id and (db.group.year>(year(now())-5)) and spec.id<>24 and up.group=db.group.id and up.id=ups.up and ups.id=ups_sotr.ups and ups_sotr.sotr = sotr.id and sotr.id<>781 and sotr.id<>844 and sotr.id<>892 and sotr.id<>896 and sotr.id<>111 ORDER BY name;")

    spec = sql("select distinct spec.id, spec.desc, spec.descs FROM spec, db.group where db.group.spec = spec.id and (db.group.year>(year(now())-5)) and spec.id <> 24;")

    f2(clear(group), sotr, spec)


f1()
