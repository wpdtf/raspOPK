from werkzeug.exceptions import abort
from flask import Flask, render_template
from datetime import datetime, timedelta, date
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
        with open(f"raspCopy/sotr/sotr{idSotr}.json") as json_file:
            rasp = json.load(json_file)
    except:
        return []
    else:
        return rasp

def raspTodayGroup(idGroup):
    try:
        with open(f"raspCopy/groups/group_{idGroup}.json") as json_file:
            rasp = json.load(json_file)
    except:
        return []
    else:
        return rasp

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
