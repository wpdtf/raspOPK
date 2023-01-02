import pymysql
from datetime import datetime, date
from config import host, user, password, db_name
from config1 import host1, user1, password1, db_name1
from array import *


def sql133(sql_text):
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

def sql131(sql_text):
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

sql133("set names utf8;")

sql131("set names utf8;")


def whySemester(yearGroup):
    today = date.today()
    semesterGroup = int(today.strftime('%Y'))-int(yearGroup)
    if semesterGroup == 0:
        semesterGroup = 1
    elif semesterGroup == 1:
        if int(today.strftime('%m'))<=7:
            semesterGroup = 2
        else:
            semesterGroup = 3
    elif semesterGroup == 2:
        if int(today.strftime('%m'))<=7:
            semesterGroup = 4
        else:
            semesterGroup = 5
    elif semesterGroup == 3:
        if int(today.strftime('%m'))<=7:
            semesterGroup = 6
        else:
            semesterGroup = 7
    else:
        semesterGroup = 8
    return semesterGroup

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
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year']), 'semester':whySemester(a['year'])})
        else:
            if (int(today.strftime('%Y')) - a['year']) == (int(srok[0])) and int(today.strftime('%m'))<=7:
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year']), 'semester':whySemester(a['year'])})
            elif (int(today.strftime('%Y')) - a['year']) < (int(srok[0])):
                opk_group.append({'id':a['id'], 'spec':a['spec'], 'nameGroup':clearem(a['nameGroup']), 'srok':(int(today.strftime('%Y')) - a['year']), 'semester':whySemester(a['year'])})
    opk_group = sorted(opk_group, key=lambda x: x['nameGroup'])
    return opk_group

def f2(group,  sotr, spec, aud):
    sql133("truncate table opk_group;")
    sql133("truncate table opk_sotr;")
    sql133("truncate table opk_spec;")
    sql133("truncate table opk_aud;")
    for a in group:
        sql133(f"insert into opk_group values ({str(a['id'])}, {str(a['spec'])}, '{str(a['nameGroup'])}', {str(a['srok'])}, {a['semester']});")
    for a in sotr:
        sql133(f"insert into opk_sotr values ({str(a['id'])}, '{str(a['name'])}');")
    for a in spec:
        sql133(f"insert into opk_spec values ({str(a['id'])}, '{str(a['desc'])}', '{str(a['descs'])}');")
    for a in aud:
        sql133(f"insert into opk_aud values (null, '{str(a['descs'])}');")
    f3(group)

def f1():

    group = sql131("select distinct db.group.id, db.group.spec, concat(spec.descs, '-', substring(cast(db.group.year as char(4)), 3, 4), '-', cast(db.group.index as char(1))) as 'nameGroup', srok, year from db.group, spec where db.group.spec = spec.id;")

    sotr = sql131("select distinct sotr.id, CONCAT(surname, ' ',substring(name, 1, 1), '. ', substring(otchestvo, 1, 1), '.') as 'name' from db.group, sotr, spec, up, ups, ups_sotr where db.group.spec = spec.id and (db.group.year>(year(now())-5)) and spec.id<>24 and up.group=db.group.id and up.id=ups.up and ups.id=ups_sotr.ups and ups_sotr.sotr = sotr.id and sotr.id<>892 and sotr.id<>844 and sotr.flags= 1 ORDER BY name;")

    spec = sql131("select distinct spec.id, spec.desc, spec.descs FROM spec, db.group where db.group.spec = spec.id and (db.group.year>(year(now())-5)) and spec.id <> 24;")

    aud = sql131("select descs from aud;")

    f2(clear(group), sotr, spec, aud)


def f3(group):
    sql133(f"truncate table opk_disc_info;")
    for a in group:
        study_plan = sql131(f"select ups.n, disc.desc31, ups_sotr.id, ups_sotr.sotr from ups, up, disc, ups_sotr where ups.id=ups_sotr.ups and ups.up=up.id and up.group={a['id']} and sem={a['semester']} and up.disc=disc.id and ups.n<>1;")
        for b in study_plan:
            hourse = sql131(f"select count(*) as 'hours' from rasp where ups_sotr={b['id']} and date<=CURDATE();")
            sql133(f"insert into opk_disc_info values ({a['id']}, {b['sotr']}, '{b['desc31']}', {hourse[0]['hours']}, {int(b['n'])/2})")
