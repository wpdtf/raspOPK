import telebot
from array import *
from datetime import datetime, timedelta, date
from telebot import types
import json

from bd import sql
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
itemRasp3 = types.InlineKeyboardButton('✐ Расписание через 2️⃣ дня', callback_data="bt3")
itemRasp4 = types.InlineKeyboardButton('✎ Расписание через 3️⃣ дня', callback_data="bt4")
itemRasp5 = types.InlineKeyboardButton('🔎 Найти расписание', callback_data="btGoogle")
itemRasp6 = types.InlineKeyboardButton('🧸 Дополнительно', callback_data="settings")
markupRasp.add(itemRasp1, itemRasp2, itemRasp3, itemRasp4, itemRasp5, itemRasp6)


def spamRaspGroup(raspNew, idGroup, dateNum):
    if len(raspNew)!=0:
        textRasp=f"Изменение в расписании на {(date.today()+timedelta(days=dateNum)).strftime('%d-%m-%Y')}\n"
        for a in raspNew:
            if a['disc']!= '- - - - - - - - - - - - - - - -':
                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
            else:
                textRasp = textRasp + f"\n{a['para']} отменена"
    else:
        textRasp=f"Пары {(date.today()+timedelta(days=dateNum)).strftime('%d-%m-%Y')} отменены!"

    resultUsers = sql(f"select * from bot_user where id_group = {idGroup};")
    for a in resultUsers:
        bot.send_sticker(a['user_id'], a['sticker_Update']) #408663065
        bot.send_message(a['user_id'], f"{a['text_Update']}\n{textRasp}", reply_markup = markupRasp) #408663065

def spamRaspSotr(raspNew, idSotr, dateNum):
    if len(raspNew)!=0:
        textRasp=f"Изменение в расписании на {(date.today()+timedelta(days=dateNum)).strftime('%d-%m-%Y')}\n"
        for a in raspNew:
            if a['disc']!= '- - - - - - - - - - - - - - - -':
                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
            else:
                textRasp = textRasp + f"\n{a['para']} отменена"
    else:
        textRasp=f"Пары {(date.today()+timedelta(days=dateNum)).strftime('%d-%m-%Y')} отменены!"

    resultUsers = sql(f"select * from bot_user where id_group = {idSotr};")
    for a in resultUsers:
        bot.send_sticker(a['user_id'], a['sticker_Update']) #408663065
        bot.send_message(a['user_id'], f"{a['text_Update']}\n{textRasp}", reply_markup = markupRasp) #408663065
