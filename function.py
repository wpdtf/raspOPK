from werkzeug.exceptions import abort
from flask import Flask, render_template
from datetime import datetime, timedelta, date
from bd import sql
import json



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


def whatPlatform(request):
    users = request.headers.get('User-Agent')
    if users.find("Android") != -1:
        return f"/static/css/styleMobil.css"
    elif users.find("iPhone") != -1:
        return f"/static/css/styleMobil.css"
    else:
        return f"/static/css/style.css"


def raspTodaySotr(idSotr):
    try:
        rasp = []
        rasp = sql(f"select para, disc, aud, groupName, dateText from opk_rasp_sotr_pars where id={idSotr} ORDER BY dateText, para;")
        return rasp
    except:
        return []

def raspTodayGroup(idGroup):
    try:
        rasp =[]
        rasp = sql(f"select para, disc, aud, sotr, dateText from opk_rasp_group_pars where id={idGroup} ORDER BY dateText, para;")
        return rasp
    except:
        return []

def raspTodayAud(Aud):
    try:
        rasp = []
        rasp = sql(f"select aud, para, dateText, sotr, opk_group.name_group, disc from opk_group, opk_rasp_group_pars, opk_aud where opk_rasp_group_pars.id=opk_group.id and aud=opk_aud.name and opk_aud.id={Aud} ORDER BY dateText, para;")
        return rasp
    except:
        return []

def Days(day):
    day = int((datetime.now()+timedelta(days=day)).strftime("%d"))
    return day

def Month(day):
    month = int((datetime.now()+timedelta(days=day)).strftime("%m"))
    if month == 1:
        month = "января"
    elif month == 2:
        month = "февраля"
    elif month == 3:
        month = "марта"
    elif month == 4:
        month = "апреля"
    elif month == 5:
        month = "мая"
    elif month == 6:
        month = "июня"
    elif month == 7:
        month = "июля"
    elif month == 8:
        month = "августа"
    elif month == 9:
        month = "сентября"
    elif month == 10:
        month = "октября"
    elif month == 11:
        month = "ноября"
    elif month == 12:
        month = "декабря"
    return month
