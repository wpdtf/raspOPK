# pip install requests fake_useragent BeautifulSoup4 lxml
import time
import json
import os
import shutil
from datetime import timedelta, date, datetime
from bs4 import BeautifulSoup

from bd import sql
from spam import spamRaspGroup, spamRaspSotr
#from CopyFull import f1

pars_number = [
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8"
]

def connect_to_IAS(url):
    import requests
    import json

    with open('cookies.json') as json_file:
        cookies_dict = json.load(json_file)

    session = requests.Session()

    for cookies in cookies_dict:
        session.cookies.set(**cookies)

    response = session.get(url).text

    EndtimeConnect = time.time()


    return response

def parsRasp(url):
    src = connect_to_IAS(url)
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find_all(class_="tabc")
    rasp = []

    i = 0
    for a in table:
        columns = a.find_all("tr")
        for b in columns:
            line = b.find_all("td")
            rasp.append([
            (date.today()+timedelta(days=i)).strftime("%Y-%m-%d"),
            line[0].text,
            line[1].text,
            line[2].text,
            line[3].text
            ])
        i+=1

    return rasp

def groupJson(WhatUpdate):
    group = sql(f"SELECT id, name_group FROM opk_group;")

    for a in group:
        id_group = a['id']
        raspPars = parsRasp(f"http://172.16.10.131/main.php?p=rasp&act=rtr&grp={id_group}")
        raspNew = []
        for a in raspPars:
            if a[1] in pars_number:
                    raspNew.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3], 'dateText' : a[0]})


        raspOld = sql(f"select para, disc, aud, sotr, dateText from opk_rasp_group_pars where id={id_group}")

        if raspNew!=raspOld:
            sql(f"delete from opk_rasp_group_pars where id={id_group}")
            for a in raspNew:
                sql(f"insert into opk_rasp_group_pars values ({id_group},'{a['para']}','{a['disc']}','{a['aud']}','{a['sotr']}', '{a['dateText']}');")

            for a in range(0, 2):
                raspWhatMessageNew = []
                for b in raspNew:
                    if b['dateText'] == (date.today()+timedelta(days=a)).strftime("%Y-%m-%d"):
                        raspWhatMessageNew.append({'para' : b['para'], 'disc' : b['disc'], 'aud' : b['aud'], 'sotr' : b['sotr'], 'dateText' : b['dateText']})

                raspWhatMessageOld = []
                for b in raspOld:
                    if b['dateText'] == (date.today()+timedelta(days=a)).strftime("%Y-%m-%d"):
                        raspWhatMessageOld.append({'para' : b['para'], 'disc' : b['disc'], 'aud' : b['aud'], 'sotr' : b['sotr'], 'dateText' : b['dateText']})

                if (raspWhatMessageNew != raspWhatMessageOld) and WhatUpdate:
                    spamRaspGroup(raspWhatMessageNew, id_group, a)
        time.sleep(1)


def sotrJson(WhatUpdate):
    sotr = sql(f"SELECT id FROM opk_sotr;")

    for a in sotr:
        id_sotr = a['id']
        raspPars = parsRasp(f"http://172.16.10.131/main.php?p=rasp&act=rtr&sot={id_sotr}")
        raspNew = []
        for a in raspPars:
            if a[1] in pars_number:
                    raspNew.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'groupName' : a[2], 'dateText' : a[0]})


        raspOld = sql(f"select para, disc, aud, groupName, dateText from opk_rasp_sotr_pars where id={id_sotr}")

        if raspNew!=raspOld:
            sql(f"delete from opk_rasp_sotr_pars where id={id_sotr}")
            for a in raspNew:
                sql(f"insert into opk_rasp_sotr_pars values ({id_sotr},'{a['para']}','{a['disc']}','{a['aud']}','{a['groupName']}', '{a['dateText']}');")

            for a in range(0, 2):
                raspWhatMessageNew = []
                for b in raspNew:
                    if b['dateText'] == (date.today()+timedelta(days=a)).strftime("%Y-%m-%d"):
                        raspWhatMessageNew.append({'para' : b['para'], 'disc' : b['disc'], 'aud' : b['aud'], 'groupName' : b['groupName'], 'dateText' : b['dateText']})

                raspWhatMessageOld = []
                for b in raspOld:
                    if b['dateText'] == (date.today()+timedelta(days=a)).strftime("%Y-%m-%d"):
                        raspWhatMessageOld.append({'para' : b['para'], 'disc' : b['disc'], 'aud' : b['aud'], 'groupName' : b['groupName'], 'dateText' : b['dateText']})

                if (raspWhatMessageNew != raspWhatMessageOld) and WhatUpdate:
                    spamRaspSotr(raspWhatMessageNew, '9999'+str(id_sotr), a)
        time.sleep(1)


def funcCopy():
    while (True):
        try:
            hours = int(datetime.today().strftime("%H"))
            if 13 >= hours >= 8:
                groupJson(True)
                sotrJson(True)
                time.sleep(300)
            elif 17 >= hours > 13:
                groupJson(True)
                sotrJson(True)
                time.sleep(600)
            elif 19 >= hours > 17:
                groupJson(True)
                sotrJson(True)
                time.sleep(900)
            elif 22 >= hours > 19:
                groupJson(True)
                sotrJson(True)
                time.sleep(1800)
            elif 5>= hours >3:
                groupJson(False)
                sotrJson(False)
                f1()
                time.sleep(10800)
            else:
                time.sleep(1800)
        except:
            groupJson(False)
            sotrJson(False)
            f1()


if __name__ == '__main__':
    funcCopy()
