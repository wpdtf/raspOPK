# pip install requests fake_useragent BeautifulSoup4 lxml
import time
import json
import os
import shutil
from datetime import timedelta, date, datetime
from bs4 import BeautifulSoup

from bd import sql
from spam import spamBOT
from CopyFull import f1

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
            (date.today()+timedelta(days=i)).strftime("%d-%m-%Y"),
            line[0].text,
            line[1].text,
            line[2].text,
            line[3].text
            ])
        i+=1

    return rasp

def groupJson(activTest):
    group = sql(f"SELECT id FROM opk_group;")


    for a in group:
        id_group = a['id']
        rasp = parsRasp(f"http://172.16.10.131/main.php?p=rasp&act=rtr&grp={id_group}")
        with open(f"groups/group_{id_group}.json") as json_file:
            rasp_no_update = json.load(json_file)

        if rasp_no_update!=rasp:
            raspgroup1_no_update = []
            raspgroup2_no_update = []

            raspgroup1_update = []
            raspgroup2_update = []
            for a in rasp_no_update:
                if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspgroup1_no_update.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
                elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspgroup2_no_update.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})

            for a in rasp:
                if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspgroup1_update.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
                elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspgroup2_update.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})

            if raspgroup1_no_update!=raspgroup1_update and activTest:
                spamBOT(rasp, 0, f"{id_group}")
            if raspgroup2_no_update!=raspgroup2_update and activTest:
                spamBOT(rasp, 1, f"{id_group}")

        with open(f"groups/group_{id_group}.json", 'w') as file:
            json.dump(rasp, file, indent=4, ensure_ascii=False)
        time.sleep(1)

def sotrJson(activTest):
    sotr = sql(f"SELECT id FROM opk_sotr;")

    for a in sotr:
        id_sotr = a['id']
        rasp = parsRasp(f"http://172.16.10.131/main.php?p=rasp&act=rtr&sot={id_sotr}")
        with open(f"sotr/sotr{id_sotr}.json") as json_file:
            rasp_no_update = json.load(json_file)

        if rasp_no_update!=rasp:
            raspsotr1_no_update = []
            raspsotr2_no_update = []

            raspsotr1_update = []
            raspsotr2_update = []
            for a in rasp_no_update:
                if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspsotr1_no_update.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
                elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspsotr2_no_update.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})

            for a in rasp:
                if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspsotr1_update.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
                elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        raspsotr2_update.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})

            if raspsotr1_no_update!=raspsotr1_update and activTest:
                spamBOT(rasp, 0, f"9999{id_sotr}")
            if raspsotr2_no_update!=raspsotr2_update and activTest:
                spamBOT(rasp, 1, f"9999{id_sotr}")

        with open(f"sotr/sotr{id_sotr}.json", 'w') as file:
            json.dump(rasp, file, indent=4, ensure_ascii=False)
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
                shutil.rmtree('groups/')
                shutil.rmtree('sotr/')
                os.mkdir("groups")
                os.mkdir("sotr")
                groupJson(False)
                sotrJson(False)
                f1()
                time.sleep(10800)
            else:
                time.sleep(1800)
        except:
            shutil.rmtree('groups/')
            shutil.rmtree('sotr/')
            os.mkdir("groups")
            os.mkdir("sotr")
            groupJson(False)
            sotrJson(False)
            f1()


if __name__ == '__main__':
    funcCopy()
