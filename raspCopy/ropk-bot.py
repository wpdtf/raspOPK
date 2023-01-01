import telebot
import time
import json

from array import *
from datetime import datetime, timedelta, date
from telebot import types
from errors_dmitry import spamsText

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
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 0)
        elif call.data == "bt2":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 1)
        elif call.data == "bt3":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = 'Введите название группы или имя преподавателя', reply_markup = markupBack)
            bot.register_next_step_handler(call.message, googleRasp)
        elif call.data == "goodbye":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Вы уверены?", reply_markup=markupChoice)
        elif call.data == "No":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup=markupRasp)
        elif call.data == "Delete":

            delete(call.message, call.from_user.id)
        elif call.data == "Return":

            start(call.message, call.from_user.id)
        elif call.data == "Back":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup = markupRasp)
        elif call.data == "personalis":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Персонализация", reply_markup = markupPersonalis)
        elif call.data == "stS":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerToDay(call.message, call.from_user.id)
        elif call.data == "stUw":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerUpdate(call.message, call.from_user.id)
        elif call.data == "stP":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            stickerGoogle(call.message, call.from_user.id)
        elif call.data == "txUw":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            textUpdate(call.message, call.from_user.id)
        elif call.data == "backPers":

            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            backPersonal(call.message, call.from_user.id)

def userInfo(message):
    try:
        result = bd.sql(f"select * from bot_user where user_id = {message.chat.id};")
        if len(result)!=0:
            return result[0]
    except BaseException as errors:

        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка функции ЮзерИнфо!")
        print(message.chat.id)
        print(message.text)
        print(errors)
        errorsText = f"Ошибка функции ЮзерИнфо!\n{message.chat.id}\n{message.text}\n{errors}"
        spamsText(errorsText)


def backPersonal(message, id):
    result = bd.sql(f"update bot_user set sticker_ToDay = 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', sticker_Update = 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', sticker_Google = 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', text_Update = 'Что-то новенькое!' where user_id = {message.chat.id};")
    bot.send_message(message.chat.id, "Используется стандартная персонализация!", reply_markup=markupPersonalis)

def stickerToDay(message, id):
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerToDayComplet1, id)

def stickerToDayComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_ToDay = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerToDayComplet2, id)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerToDayComplet2, id)

def stickerToDayComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_ToDay = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerToDayComplet1, id)
    else:

        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerToDayComplet1, id)


def stickerUpdate(message, id):
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerUpdateComplet1, id)

def stickerUpdateComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Update = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerUpdateComplet2, id)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerUpdateComplet2, id)

def stickerUpdateComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Update = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerUpdateComplet1, id)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerUpdateComplet1, id)


def stickerGoogle(message, id):
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerGoogleComplet1, id)

def stickerGoogleComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Google = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerGoogleComplet2, id)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerGoogleComplet2, id)

def stickerGoogleComplet2(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_Google = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":

            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
            bot.register_next_step_handler(message, stickerGoogleComplet1, id)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на стикер, используйте только то, что предлагает телеграмм\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, stickerGoogleComplet1, id)


def textUpdate(message, id):
    bot.send_message(message.chat.id, "Пришлите текст, и я буду его показывать во время уведомлений о изменении вашего расписания\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, textUpdateComplet1, id)

def textUpdateComplet1(message, id):
    if message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            textUser = message.text
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            textUser=textUser.replace('\n', "")
            bd.sql(f"update bot_user set text_Update = '{textUser}' where user_id = {id};")
            bot.send_message(message.chat.id, "Отлично, теперь именно этот текст ты и будешь видеть", reply_markup=markupPersonalis)
    else:

        bot.send_message(message.chat.id, "Что то не похоже это на текст, попробуйте еще раз\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, textUpdateComplet2, id)

def textUpdateComplet2(message, id):
    if message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, "Персонализация", reply_markup=markupPersonalis)
        else:
            textUser = message.text
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            textUser=textUser.replace('\n', "")
            bd.sql(f"update bot_user set text_Update = '{textUser}' where user_id = {id};")
            bot.send_message(message.chat.id, "Отлично, теперь именно этот текст ты и будешь видеть", reply_markup=markupPersonalis)
    else:
        bot.send_message(message.chat.id, "Что то не похоже это на текст, попробуйте еще раз\n\nНу или напишите стоп")
        bot.register_next_step_handler(message, textUpdateComplet1, id)


def delete(message, id):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl_pibOxVlrF97Fx9YyvvT3BEBsuLfwACWxoAAtfNQEsqrm1lEw-otSQE")
    bd.sql(f"delete from bot_user where user_id = {id};")
    bot.send_message(message.chat.id, "Вы больше не подписаны.", reply_markup = markupReturn)

def googleRasp(message):
    try:
        userI = userInfo(message)
        resultGroup = []
        resultSotr = []
        if message.content_type != "text":
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
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEF2zRjJN78c1f0062NMdHzFQp6u8gAAacAAlcAA61lvBRnR88ypdn8ZykE')
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов", reply_markup = markupBack)
                bot.register_next_step_handler(message, googleRasp2)
            elif len(resultGroup)==1:
                raspNew = todayGroup(resultGroup[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)

            elif len(resultSotr)==1:
                raspNew = todaySotr(resultSotr[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)
    except BaseException as errors:
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

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
                bot.register_next_step_handler(message, googleRasp)
            elif len(resultGroup)==1:
                raspNew = todayGroup(resultGroup[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)
            elif len(resultSotr)==1:
                raspNew = todaySotr(resultSotr[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
                            else:
                                textRasp = textRasp + f"\n{a['para']} отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)
    except BaseException as errors:
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
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка расписания!")
        print(day)
        print(id)
        print(errors)
        errorsText = f"Ошибка расписания!\n{message.chat.id}\n{id}\n{day}\n{errors}"
        spamsText(errorsText)

def todaySotr(idSotr):
    try:
        rasp = []
        rasp = bd.sql(f"select para, disc, aud, groupName, dateText from opk_rasp_sotr_pars where id={idSotr} ORDER BY dateText, para;")
        return rasp
    except:
        return []


def todayGroup(idGroup):
    try:
        rasp =[]
        rasp = bd.sql(f"select para, disc, aud, sotr, dateText from opk_rasp_group_pars where id={idGroup} ORDER BY dateText, para;")
        return rasp
    except:
        return []

def raspTodaySotr(message, idSotr, day):
    try:
        userI = userInfo(message)
        raspNew = todaySotr(idSotr)
        if len(raspNew)!=0:
            textRasp=f"Расписание на {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')}\n"
            for a in raspNew:
                if a['dateText']==(date.today()+timedelta(days=day)).strftime('%Y-%m-%d'):
                    if a['disc']!= '- - - - - - - - - - - - - - - -':
                        textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['groupName']}"
                    else:
                        textRasp = textRasp + f"\n{a['para']} отменена"
        else:
            textRasp=f"Пары {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} отсутствуют!"

        bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
        bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)
    except BaseException as errors:
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка расписания групп")
        print(day)
        print(idGroup)
        print(errors)
        errorsText = f"Ошибка расписания групп\n{message.chat.id}\n{idGroup}\n{day}\n{errors}"
        spamsText(errorsText)

def raspTodayGroup(message, idGroup, day):
    try:
        userI = userInfo(message)
        raspNew = todayGroup(idGroup)
        if len(raspNew)!=0:
            textRasp=f"Расписание на {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')}\n"
            for a in raspNew:
                if a['dateText']==(date.today()+timedelta(days=day)).strftime('%Y-%m-%d'):
                    if a['disc']!= '- - - - - - - - - - - - - - - -':
                        textRasp = textRasp + f"\n{a['para']} в {a['aud']} по {a['disc']} у {a['sotr']}"
                    else:
                        textRasp = textRasp + f"\n{a['para']} отменена"
        else:
            textRasp=f"Пары {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} отсутствуют!"

        bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
        bot.send_message(message.chat.id, textRasp, reply_markup = markupRasp)
    except BaseException as errors:
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

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
            bot.register_next_step_handler(message, registration2)
        elif len(resultGroup)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {resultGroup[0]['id']}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
        elif len(resultSotr)>1:

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    except BaseException as errors:

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

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов")
            bot.register_next_step_handler(message, registration)
        elif len(resultGroup)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {resultGroup[0]['id']}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
        elif len(resultSotr)>1:

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nМеню.", reply_markup = markupRasp)
    except BaseException as errors:

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
