import telebot
import time
import json

from array import *
from datetime import datetime, timedelta, date
from telebot import types
from errors_dmitry import spamsText
from infoBot import numMessage

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

#bot = telebot.TeleBot("5220654021:AAGu5TgZwwgPVVh94Ppcr7qkD9Z9XXO8a8o")
bot = telebot.TeleBot(config.token)

markupNone = types.InlineKeyboardMarkup(row_width=1)

markupRasp = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('✐ Расписание на сегодня', callback_data="bt1")
itemRasp2 = types.InlineKeyboardButton('✎ Расписание на завтра', callback_data="bt2")
itemRasp3 = types.InlineKeyboardButton('🔎 Найти расписание ', callback_data="bt3")
itemRasp4 = types.InlineKeyboardButton('🌹 Персонализация', callback_data="personalis")
itemRasp5 = types.InlineKeyboardButton('👋 Отписаться', callback_data="goodbye")
markupRasp.add(itemRasp1, itemRasp2, itemRasp3, itemRasp4, itemRasp5)

markupBack = types.InlineKeyboardMarkup(row_width=1)
markupBack1 = types.InlineKeyboardButton('◀️ Назад', callback_data="Back")
markupBack.add(markupBack1)

markupPersonalis = types.InlineKeyboardMarkup(row_width=1)
markupPersonalis1 = types.InlineKeyboardButton('Стикер расписания', callback_data="stS")
markupPersonalis3 = types.InlineKeyboardButton('Стикер уведомления', callback_data="stUw")
markupPersonalis4 = types.InlineKeyboardButton('Стикер поиска расписания', callback_data="stP")
markupPersonalis5 = types.InlineKeyboardButton('Текст уведомления', callback_data="txUw")
markupPersonalis6 = types.InlineKeyboardButton('🚫 Вернуть все как было', callback_data="backPers")
markupBack1 = types.InlineKeyboardButton('◀️ Назад', callback_data="Back")
markupPersonalis.add(markupPersonalis1, markupPersonalis3, markupPersonalis4, markupPersonalis5, markupPersonalis6, markupBack1)

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
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 0)
        elif call.data == "bt2":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 1)
        elif call.data == "bt3":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = 'Введите название группы или имя преподавателя', reply_markup = markupBack)
            bot.register_next_step_handler(call.message, googleRasp)
        elif call.data == "goodbye":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Вы уверены?", reply_markup=markupChoice)
        elif call.data == "No":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup=markupRasp)
        elif call.data == "Delete":
            numMessage()
            delete(call.message, call.from_user.id)
        elif call.data == "Return":
            numMessage()
            start(call.message, call.from_user.id)
        elif call.data == "Back":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup = markupRasp)
        elif call.data == "personalis":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Персонализация", reply_markup = markupPersonalis)
        elif call.data == "stS":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerToDay(call.message, call.from_user.id)
        elif call.data == "stUw":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerUpdate(call.message, call.from_user.id)
        elif call.data == "stP":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerGoogle(call.message, call.from_user.id)
        elif call.data == "txUw":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            textUpdate(call.message, call.from_user.id)
        elif call.data == "backPers":
            numMessage()
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            backPersonal(call.message, call.from_user.id)

def userInfo(message):
    try:
        result = bd.sql(f"select * from bot_user where user_id = {message.chat.id};")
        if len(result)!=0:
            return result[0]
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка функции ЮзерИнфо!")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка функции ЮзерИнфо!\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)


def backPersonal(message, id):
    result = bd.sql(f"update bot_user set sticker_ToDay = 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', sticker_Update = 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', sticker_Google = 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', text_Update = 'Что-то новенькое!' where user_id = {message.chat.id};")
    numMessage()
    bot.send_message(message.chat.id, "Все, теперь будет использоваться то, что выбрали разработчики", reply_markup=markupPersonalis)

def stickerToDay(message, id):
    numMessage()
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerToDayComplet1, id)

def stickerToDayComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_ToDay = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerToDayComplet2, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerToDayComplet2, id)

def stickerToDayComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_ToDay = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerToDayComplet1, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerToDayComplet1, id)


def stickerUpdate(message, id):
    numMessage()
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerUpdateComplet1, id)

def stickerUpdateComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Update = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerUpdateComplet2, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerUpdateComplet2, id)

def stickerUpdateComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Update = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerUpdateComplet1, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerUpdateComplet1, id)


def stickerGoogle(message, id):
    numMessage()
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerGoogleComplet1, id)

def stickerGoogleComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Google = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerGoogleComplet2, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerGoogleComplet2, id)

def stickerGoogleComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Google = '{message.sticker.file_id}' where user_id = {id};")
        numMessage()
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            numMessage()
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerGoogleComplet1, id)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerGoogleComplet1, id)


def textUpdate(message, id):
    numMessage()
    bot.send_message(message.chat.id, "Пришлите текст, и я буду его показывать во время уведомлений о изменении вашего расписания\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, textUpdateComplet1, id)

def textUpdateComplet1(message, id):
    if message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            textUser = message.text
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            textUser=textUser.replace('\n', "")
            bd.sql(f"update bot_user set text_Update = '{textUser}' where user_id = {id};")
            numMessage()
            bot.send_message(message.chat.id, "Отлично, теперь именно этот текст ты и будешь видеть", reply_markup=markupPersonalis)
    else:
        numMessage()
        bot.send_message(message.chat.id, "Что то не похоже это на текст, попробуйте еще раз\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, textUpdateComplet2, id)

def textUpdateComplet2(message, id):
    if message.content_type == "text":
        if (message.text).lower() == "стоп":
            numMessage()
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            textUser = message.text
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            textUser=textUser.replace('\n', "")
            bd.sql(f"update bot_user set text_Update = '{textUser}' where user_id = {id};")
            numMessage()
            bot.send_message(message.chat.id, "Отлично, теперь именно этот текст ты и будешь видеть", reply_markup=markupPersonalis)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на текст, попробуйте еще раз\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, textUpdateComplet1, id)


def delete(message, id):
    numMessage()
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl_pibOxVlrF97Fx9YyvvT3BEBsuLfwACWxoAAtfNQEsqrm1lEw-otSQE")
    bd.sql(f"delete from bot_user where user_id = {id};")
    bot.send_message(message.chat.id, "Вы больше не подписаны.", reply_markup = markupReturn)

def googleRasp(message):
    try:
        userI = userInfo(message)
        resultGroup = []
        resultSotr = []
        if message.content_type != "text":
            numMessage()
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEF2zRjJN78c1f0062NMdHzFQp6u8gAAacAAlcAA61lvBRnR88ypdn8ZykE')
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов", reply_markup = markupBack)
            bot.register_next_step_handler(message, googleRasp2)
        else:
            textUser = message.text;
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
            resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
            if (len(resultGroup)==0 or len(resultGroup)>1) and (len(resultSotr)==0 or len(resultSotr)>1):
                numMessage()
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEF2zRjJN78c1f0062NMdHzFQp6u8gAAacAAlcAA61lvBRnR88ypdn8ZykE')
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов", reply_markup = markupBack)
                bot.register_next_step_handler(message, googleRasp2)
            elif len(resultGroup)==1:
                raspgroup = todayGroup(resultGroup[0]['id'], message)
                rasp = []
                raspp1 = ""
                raspp2 = ""
                for a in raspgroup:
                    if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
                if len(rasp)!=0:
                    raspp1 = f'{(date.today()+timedelta(days=0)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp1 = raspp1 + f"\n{a['para']} отменена"
                        else:
                            raspp1 = raspp1 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                rasp = []

                for a in raspgroup:
                    if a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})

                if len(rasp)!=0:
                    raspp2 = f'{(date.today()+timedelta(days=1)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp2 = raspp2 + f"\n{a['para']} отменена"
                        else:
                            raspp2 = raspp2 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"

                if len(raspp1)!=0 or len(raspp2)!=0:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Расписание - {textUser} \n\n{raspp1}\n\n{raspp2}", reply_markup = markupRasp)
                else:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Пар у {textUser} нет.", reply_markup = markupRasp)
            elif len(resultSotr)==1:
                raspsotr = todaySotr(resultSotr[0]['id'], message)
                rasp = []
                raspp1 = ""
                raspp2 = ""
                for a in raspsotr:
                    if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'sotr' : a[2]})
                if len(rasp)!=0:
                    raspp1 = f'{(date.today()+timedelta(days=0)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp1 = raspp1 + f"\n{a['para']} отменена"
                        else:
                            raspp1 = raspp1 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                rasp = []

                for a in raspsotr:
                    if a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'sotr' : a[2]})

                if len(rasp)!=0:
                    raspp2 = f'{(date.today()+timedelta(days=1)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp2 = raspp2 + f"\n{a['para']} отменена"
                        else:
                            raspp2 = raspp2 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"

                if len(raspp1)!=0 or len(raspp2)!=0:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Расписание - {textUser} \n\n{raspp1}\n\n{raspp2}", reply_markup = markupRasp)
                else:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Пар у {textUser} нет.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка поиска 1!")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка поиска 1!\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)

def googleRasp2(message):
    try:
        userI = userInfo(message)
        resultGroup = []
        resultSotr = []
        if message.content_type != 'text':
            numMessage()
            bot.send_sticker(message.chat.id, userI['sticker_Google'])
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
            bot.register_next_step_handler(message, googleRasp)
        else:
            textUser = message.text;
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
            resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
            if (len(resultGroup)==0 or len(resultGroup)>1) and len(resultSotr)==0:
                numMessage()
                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
                bot.register_next_step_handler(message, googleRasp)
            elif len(resultGroup)==1:
                raspgroup = todayGroup(resultGroup[0]['id'], message)
                rasp = []
                raspp1 = ""
                raspp2 = ""
                for a in raspgroup:
                    if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
                if len(rasp)!=0:
                    raspp1 = f'{(date.today()+timedelta(days=0)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp1 = raspp1 + f"\n{a['para']} отменена"
                        else:
                            raspp1 = raspp1 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                rasp = []

                for a in raspgroup:
                    if a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})

                if len(rasp)!=0:
                    raspp2 = f'{(date.today()+timedelta(days=1)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp2 = raspp2 + f"\n{a['para']} отменена"
                        else:
                            raspp2 = raspp2 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"

                if len(raspp1)!=0 or len(raspp2)!=0:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Расписание - {textUser} \n\n{raspp1}\n\n{raspp2}", reply_markup = markupRasp)
                else:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Пар у {textUser} нет.", reply_markup = markupRasp)
            elif len(resultSotr)==1:
                raspsotr = todaySotr(resultSotr[0]['id'], message)
                rasp = []
                raspp1 = ""
                raspp2 = ""
                for a in raspsotr:
                    if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'sotr' : a[2]})
                if len(rasp)!=0:
                    raspp1 = f'{(date.today()+timedelta(days=0)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp1 = raspp1 + f"\n{a['para']} отменена"
                        else:
                            raspp1 = raspp1 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                rasp = []

                for a in raspsotr:
                    if a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
                        if a[1] in pars_number:
                            rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'sotr' : a[2]})

                if len(rasp)!=0:
                    raspp2 = f'{(date.today()+timedelta(days=1)).strftime("%d-%m-%Y")}'
                    for a in rasp:
                        if a['disc']=='- - - - - - - - - - - - - - - -':
                            raspp2 = raspp2 + f"\n{a['para']} отменена"
                        else:
                            raspp2 = raspp2 + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"

                if len(raspp1)!=0 or len(raspp2)!=0:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Расписание - {textUser} \n\n{raspp1}\n\n{raspp2}", reply_markup = markupRasp)
                else:
                    numMessage()
                    bot.send_sticker(message.chat.id, userI['sticker_Google'])
                    bot.send_message(message.chat.id, f"Пар у {textUser} нет.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка поиска 2!")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка поиска 2!\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)

def raspToday(message, id, day):
    try:
        result = []
        result = bd.sql(f"select * from bot_user where user_id = {id};")
        if len(result)==1:
            result = result[0]['id_group']
            resultTest = str(result)
            if (resultTest[0:4] == "9999"):
                raspTodaySotr(message, resultTest[4:10], day)
            else:
                raspTodayGroup(message, resultTest, day)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка расписания!")
        print(day)
        print(id)
        print(errors)
        errorsText = f"Ошибка расписания!\n{message.chat.id}\n{id}\n{day}\n{errors}"
        spamsText(errorsText)

def todaySotr(idSotr, message):
    try:
        rasp = []
        with open(f"sotr/sotr{idSotr}.json") as json_file:
            rasp = json.load(json_file)
    except:
        return []
    else:
        if rasp is not None:
            return rasp
        else:
            numMessage()
            bot.send_message(message.chat.id, f"Ошибка просмотра расписания.", reply_markup = markupRasp)

def todayGroup(idGroup, message):
    try:
        with open(f"groups/group_{idGroup}.json") as json_file:
            rasp = json.load(json_file)
    except:
        return []
    else:
        if rasp is not None:
            return rasp
        else:
            numMessage()
            bot.send_message(message.chat.id, f"Ошибка просмотра расписания.", reply_markup = markupRasp)

def raspTodaySotr(message, idSotr, day):
    try:
        userI = userInfo(message)
        raspsotr = todaySotr(idSotr, message)
        rasp = []
        if len(raspsotr) != 0:
            for a in raspsotr:
                if a[0] == (date.today()+timedelta(days=day)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        rasp.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
        else:
            numMessage()
            bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)

        if len(rasp)!=0:
            raspp = ""
            for a in rasp:
                if a['disc']=='- - - - - - - - - - - - - - - -':
                    raspp = raspp + f"\n{a['para']} отменена"
                else:
                    raspp = raspp + f"\n{a['para']} в {a['aud']} по {a['disc']} у группы {a['name_group']}"
            numMessage()
            bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
            bot.send_message(message.chat.id, f"{(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} \n{raspp}", reply_markup = markupRasp)
        else:
            numMessage()
            bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
            bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка расписания сотрудников")
        print(day)
        print(idSotr)
        print(errors)
        errorsText = f"Ошибка расписания сотрудников\n{message.chat.id}\n{idSotr}\n{day}\n{errors}"
        spamsText(errorsText)

def raspTodayGroup(message, idGroup, day):
    try:
        userI = userInfo(message)
        raspgroup = todayGroup(idGroup, message)
        rasp = []
        if len(raspgroup) != 0:
            for a in raspgroup:
                if a[0] == (date.today()+timedelta(days=day)).strftime("%d-%m-%Y"):
                    if a[1] in pars_number:
                        rasp.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
        else:
            numMessage()
            bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)
        if len(rasp)!=0:
            raspp = ""
            for a in rasp:
                if a['disc']=='- - - - - - - - - - - - - - - -':
                    raspp = raspp + f"\n{a['para']} отменена"
                else:
                    raspp = raspp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
            numMessage()
            bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
            bot.send_message(message.chat.id, f"{(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} \n{raspp}", reply_markup = markupRasp)
        else:
            numMessage()
            bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
            bot.send_message(message.chat.id, f"Пар нет.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка расписания групп")
        print(day)
        print(idGroup)
        print(errors)
        errorsText = f"Ошибка расписания групп\n{message.chat.id}\n{idGroup}\n{day}\n{errors}"
        spamsText(errorsText)

def start(message, id):
    result = []
    result = bd.sql(f"select user_id from bot_user where user_id = {id};")
    if len(result) == 0:
        numMessage()
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl-hibN_62yFEAaAru8CywtkXQe-YGAACIRYAAu0vQUvRcTO_xqtmZiQE")
        bot.send_message(message.chat.id, "Привет, я бот... и я буду уведомлять вас о изменениях в расписании. \nУкажите группу или свою фамилию если вы преподаватель. \n\nГруппу укажите в формате 'ИСП-19-1' или 'ТМ-21'.")
        bot.register_next_step_handler(message, registration)
    else:
        bot.send_message(message.chat.id, "Меню", reply_markup = markupRasp)

def listSotr(message, resultSotr):
    text = ''
    for a in resultSotr:
        text = text + f"{a['name']}\n"
    numMessage()
    bot.send_message(message.chat.id, f"{text} \nУточните.")
    bot.register_next_step_handler(message, registration)

def registration(message):
    try:
        resultGroup = []
        resultSotr = []
        textUser = message.text;
        textUser=textUser.replace("%", "")
        textUser=textUser.replace("'", "")
        textUser=textUser.replace('"', "")
        resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
        resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
        if (len(resultGroup)==0 or len(resultGroup)>1) and len(resultSotr)==0:
            numMessage()
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
            bot.register_next_step_handler(message, registration2)
        elif len(resultGroup)==1:
            numMessage()
            bd.sql(f"insert into bot_user values({message.from_user.id}, {resultGroup[0]['id']}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
        elif len(resultSotr)>1:
            numMessage()
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:
            numMessage()
            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка регистрации 1")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка регистрации 1\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)

def registration2(message):
    try:
        resultGroup = []
        resultSotr = []
        textUser = message.text;
        textUser=textUser.replace("%", "")
        textUser=textUser.replace("'", "")
        textUser=textUser.replace('"', "")
        resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
        resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
        if (len(resultGroup)==0 or len(resultGroup)>1) and len(resultSotr)==0:
            numMessage()
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
            bot.register_next_step_handler(message, registration)
        elif len(resultGroup)==1:
            numMessage()
            bd.sql(f"insert into bot_user values({message.from_user.id}, {resultGroup[0]['id']}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
        elif len(resultSotr)>1:
            numMessage()
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:
            numMessage()
            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    except BaseException as errors:
        numMessage()
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка регистрации 2")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка регистрации 2\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start(message, message.from_user.id)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    start(message, message.from_user.id)

def funcStart1():
    try:
        spamsText(f"фур фур фур фур фур *прикинь работаем*")
        bot.polling(none_stop=True)
    except BaseException as errors:
        spamsText(f"Бот отвалился\n{errors}")
        funcStart2()

def funcStart2():
    try:
        spamsText(f"фур фур фур фур фур *прикинь работаем*")
        bot.polling(none_stop=True)
    except BaseException as errors:
        spamsText(f"Бот отвалился\n{errors}")
        funcStart1()

funcStart1()
