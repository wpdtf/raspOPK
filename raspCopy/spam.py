import telebot
from array import *
from datetime import datetime, timedelta, date
from telebot import types
import json

import bd
import config

bot = telebot.TeleBot(config.token)

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

markupRasp = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('✐ Расписание на сегодня', callback_data="bt1")
itemRasp2 = types.InlineKeyboardButton('✎ Расписание на завтра', callback_data="bt2")
itemRasp3 = types.InlineKeyboardButton('🔎 Найти расписание ', callback_data="bt3")
itemRasp4 = types.InlineKeyboardButton('🌹 Персонализация', callback_data="personalis")
itemRasp5 = types.InlineKeyboardButton('👋 Отписаться', callback_data="goodbye")
markupRasp.add(itemRasp1, itemRasp2, itemRasp3, itemRasp4, itemRasp5)


def spamBOT(raspgroupUpdate, day, id):
    print(f"Получен id - {id}")
    if (id[0:4] == "9999"):
        sotr = 1
    else:
        sotr = 0
    result = []
    result = bd.sql(f"select * from bot_user where id_group = {id};")
    print(f"Получены пользователи {result}")
    if len(result)!=0:
        for a in result:
            spam(raspgroupUpdate, day, a['user_id'], sotr, a['sticker_Update'], a['text_Update'])

def spam(raspgroupUpdate, day, id, sotr, stickUpd, textUpd):
    rasp = []
    for a in raspgroupUpdate:
        if a[0] == (date.today()+timedelta(days=day)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                if sotr == 1:
                    if a[3] == '- - - - - - - - - - - - - - - -':
                        rasp.append({'para' : a[1], 'disc' : 'Отменена', 'aud' : ' ', 'sotr' : ' '})
                    else:
                        rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'sotr' : a[2]})
                else:
                    if a[2] == '- - - - - - - - - - - - - - - -':
                        rasp.append({'para' : a[1], 'disc' : 'Отменена', 'aud' : ' ', 'sotr' : ' '})
                    else:
                        rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
    if len(rasp)!=0:
        raspp = ""
        for a in rasp:
            if a['disc']!= 'Отменена':
                raspp = raspp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
            else:
                raspp = raspp + f"\n{a['para']} отменена"
        try:
            bot.send_sticker(id, stickUpd)
            bot.send_message(id, f"{textUpd}\nИзменение в расписании на {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} \n{raspp}", reply_markup = markupRasp)
        except:
            print(f'Ошибка отправки - {id}')
    else:
        try:
            bot.send_sticker(id, "CAACAgIAAxkBAAEF1t5jI1cnKOUdbnrdvpeue02nI7bM9AACSQADWbv8JdEhPCKZYpwFKQQ")
            bot.send_message(id, f"Пары {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} отменены!", reply_markup = markupRasp)
        except:
            print(f'Ошибка отправки - {id}')
