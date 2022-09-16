import telebot
from array import *
from datetime import datetime, timedelta, date
from telebot import types
import json

import bd
import config

pars_number = [
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8",
"9"
]


bot = telebot.TeleBot(config.token)

markupNone = types.InlineKeyboardMarkup(row_width=1)

markupRasp = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('✐ Расписание на сегодня', callback_data="bt1")
itemRasp2 = types.InlineKeyboardButton('✎ Расписание на завтра', callback_data="bt2")
itemRasp3 = types.InlineKeyboardButton('👋 Отписаться', callback_data="goodbye")
markupRasp.add(itemRasp1, itemRasp2, itemRasp3)

markupChoice = types.InlineKeyboardMarkup(row_width=1)
markupChoice1 = types.InlineKeyboardButton('Да', callback_data="Delete")
markupChoice2 = types.InlineKeyboardButton('Нет', callback_data="No")
markupChoice.add(markupChoice1, markupChoice2)

markupReturn = types.InlineKeyboardMarkup(row_width=1)
markupReturn1 = types.InlineKeyboardButton('Вернуться', callback_data="Return")
markupReturn.add(markupReturn1)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "bt1":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 0)
        elif call.data == "bt2":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 1)
        elif call.data == "goodbye":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Вы уверены?", reply_markup=markupChoice)
        elif call.data == "No":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup=markupRasp)
        elif call.data == "Delete":
            delete(call.message, call.from_user.id)
        elif call.data == "Return":
            start(call.message, call.from_user.id)


def delete(message, id):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl_pibOxVlrF97Fx9YyvvT3BEBsuLfwACWxoAAtfNQEsqrm1lEw-otSQE")
    bd.sql(f"delete from bot_user where user_id = {id};")
    bot.send_message(message.chat.id, "Вы больше не подписаны.", reply_markup = markupReturn)

def raspToday(message, id, day):
    result = []
    result = bd.sql(f"select * from bot_user where user_id = {id};")
    if len(result)==1:
        result = result[0]['id_group']
        resultTest = str(result)
        if (resultTest[0:4] == "9999"):
            raspTodaySotr(message, resultTest[4:10], day)
        else:
            raspTodayGroup(message, resultTest, day)

def todaySotr(idSotr, message):
    try:
        rasp = []
        with open(f"sotr/sotr{idSotr}.json") as json_file:
            rasp = json.load(json_file)
    except:
        bot.send_message(message.chat.id, f"В расписании вас нет.", reply_markup = markupRasp)
    else:
        return rasp

def todayGroup(idGroup, message):
    try:
        with open(f"groups/group_{idGroup}.json") as json_file:
            rasp = json.load(json_file)
    except:
        bot.send_message(message.chat.id, f"В расписании вас нет.", reply_markup = markupRasp)
    else:
        return rasp

def raspTodaySotr(message, idSotr, day):
    raspsotr = todaySotr(idSotr, message)
    rasp = []

    for a in raspsotr:
        if a[0] == (date.today()+timedelta(days=day)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})

    if len(rasp)!=0:
        raspp = ""
        for a in rasp:
            if a['disc']=='- - - - - - - - - - - - - - - -':
                raspp = raspp + f"\n{a['para']} отменена"
            else:
                raspp = raspp + f"\n{a['para']} в {a['aud']} по {a['disc']} у группы {a['name_group']}"
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE")
        bot.send_message(message.chat.id, f"{(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} \n{raspp}", reply_markup = markupRasp)
    else:
        bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)

def raspTodayGroup(message, idGroup, day):
    raspgroup = todayGroup(idGroup, message)
    rasp = []

    for a in raspgroup:
        if a[0] == (date.today()+timedelta(days=day)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})

    if len(rasp)!=0:
        raspp = ""
        for a in rasp:
            if a['disc']=='- - - - - - - - - - - - - - - -':
                raspp = raspp + f"\n{a['para']} отменена"
            else:
                raspp = raspp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE")
        bot.send_message(message.chat.id, f"{(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} \n{raspp}", reply_markup = markupRasp)
    else:
        bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)


def start(message, id):
    result = []
    result = bd.sql(f"select user_id from bot_user where user_id = {id};")
    if len(result) == 0:
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl-hibN_62yFEAaAru8CywtkXQe-YGAACIRYAAu0vQUvRcTO_xqtmZiQE")
        bot.send_message(message.chat.id, "Привет, я бот... и я буду уведомлять вас о изменениях в расписании. \nУкажите группу или свою фамилию если вы преподаватель. \n\nГруппу укажите в формате 'ИСП-19-1' или 'ТМ-21'.")
        bot.register_next_step_handler(message, registration)
    else:
        bot.send_message(message.chat.id, "Меню", reply_markup = markupRasp)

def listSotr(message, resultSotr):
    text = ''
    for a in resultSotr:
        text = text + f"{a['name']}\n"
    bot.send_message(message.chat.id, f"{text} \nУточните.")
    bot.register_next_step_handler(message, registration)

def registration(message):
    resultGroup = []
    resultSotr = []
    resultGroup = bd.sql(f"select id from opk_group where name_group like '%{message.text}%';")
    resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{message.text}%';")
    if (len(resultGroup)==0 or len(resultGroup)>1) and len(resultSotr)==0:
        bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
        bot.register_next_step_handler(message, registration2)
    elif len(resultGroup)==1:
        bd.sql(f"insert into bot_user (user_id, id_group) values({message.from_user.id}, {resultGroup[0]['id']});")
        bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    elif len(resultSotr)>1:
        bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
        listSotr(message, resultSotr)
    elif len(resultSotr)==1:
        bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])});")
        bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)

def registration2(message):
    resultGroup = []
    resultSotr = []
    resultGroup = bd.sql(f"select id from opk_group where name_group like '%{message.text}%';")
    resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{message.text}%';")
    if (len(resultGroup)==0 or len(resultGroup)>1) and len(resultSotr)==0:
        bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
        bot.register_next_step_handler(message, registration)
    elif len(resultGroup)==1:
        bd.sql(f"insert into bot_user values({message.from_user.id}, {resultGroup[0]['id']});")
        bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    elif len(resultSotr)>1:
        bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
        listSotr(message, resultSotr)
    elif len(resultSotr)==1:
        bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])});")
        bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start(message, message.from_user.id)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    start(message, message.from_user.id)


try:
    bot.polling(none_stop=True)
except Exception as errors:
    print(f"Внимание ОШИБКА 😳")
    print(errors)
    bot.polling(none_stop=True)
