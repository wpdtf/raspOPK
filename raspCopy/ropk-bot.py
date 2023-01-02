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

text_perconalis = """
Настройки\n\nОписание возможностей:\n
🟦 - Измените стикер отправляемый вместе с расписанием\n
🟪 - Измените стикер поиска расписания, а так же отправляется при просмотре информации\n
🟧 - Измените стикер отображаемый при уведомлениях об изменении в расписании, он так же используется при просмотре звонков\n
🟩 - Измените заголовок отображаемый при уведомлениях об изменении в расписании\n
📌 - Удалит все изменения
"""
bot = telebot.TeleBot(config.token)

markupNone = types.InlineKeyboardMarkup(row_width=1)

markupRasp = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('✐ Расписание на сегодня', callback_data="bt1")
itemRasp2 = types.InlineKeyboardButton('✎ Расписание на завтра', callback_data="bt2")
itemRasp3 = types.InlineKeyboardButton('✐ Расписание через 2️⃣ дня', callback_data="bt3")
itemRasp4 = types.InlineKeyboardButton('✎ Расписание через 3️⃣ дня', callback_data="bt4")
itemRasp5 = types.InlineKeyboardButton('🔎 Найти расписание', callback_data="btGoogle")
itemRasp6 = types.InlineKeyboardButton('🧸 Дополнительно', callback_data="settings")
markupRasp.add(itemRasp1, itemRasp2, itemRasp3, itemRasp4, itemRasp5, itemRasp6)

markupSettings = types.InlineKeyboardMarkup(row_width=1)
markupSettings1 = types.InlineKeyboardButton('⚙️ Настройки', callback_data="personalis")
markupSettings2 = types.InlineKeyboardButton('📒 Информация', callback_data="InfoStudyPlan")
markupSettings3 = types.InlineKeyboardButton('🔔 Звонки', callback_data="collegeBell")
markupSettings4 = types.InlineKeyboardButton('👋 Отписаться', callback_data="goodbye")
markupSettings5 = types.InlineKeyboardButton('◀️ Назад', callback_data="Back")
markupSettings.add(markupSettings1, markupSettings2, markupSettings3, markupSettings4, markupSettings5)

markupBack = types.InlineKeyboardMarkup(row_width=1)
markupBack1 = types.InlineKeyboardButton('◀️ Назад', callback_data="Back")
markupBack.add(markupBack1)

markupPersonalis = types.InlineKeyboardMarkup(row_width=1)
markupPersonalis1 = types.InlineKeyboardButton('🟦 Расписание', callback_data="stS")
markupPersonalis2 = types.InlineKeyboardButton('🟪 Поиск', callback_data="stP")
markupPersonalis3 = types.InlineKeyboardButton('🟧 Уведомление', callback_data="stUw")
markupPersonalis4 = types.InlineKeyboardButton('🟩 Заголовок', callback_data="txUw")
markupPersonalis5 = types.InlineKeyboardButton('📌 Вернуть все как было', callback_data="backPers")
markupPersonalis6 = types.InlineKeyboardButton('◀️ Назад', callback_data="Back")
markupPersonalis.row(markupPersonalis1, markupPersonalis2)
markupPersonalis.row(markupPersonalis3, markupPersonalis4)
markupPersonalis.add(markupPersonalis5, markupPersonalis6)

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
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 0)
        elif call.data == "bt2":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 1)
        elif call.data == "bt3":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 2)
        elif call.data == "bt4":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            raspToday(call.message, call.from_user.id, 3)
        elif call.data == "InfoStudyPlan":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            infoStPlansWhy(call.message, call.from_user.id)
        elif call.data == "collegeBell":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            collegeBellMessage(call.message, call.from_user.id)
        elif call.data == "btGoogle":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = 'Поиск осуществляется по группам, преподавателям, а так же по аудиториям!', reply_markup = markupBack)
            bot.register_next_step_handler(call.message, googleRasp)
        elif call.data == "goodbye":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Вы уверены?", reply_markup=markupChoice)
        elif call.data == "No":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Расписание...", reply_markup=markupRasp)
        elif call.data == "Delete":
            delete(call.message, call.from_user.id)
        elif call.data == "Return":
            start(call.message, call.from_user.id)
        elif call.data == "Back":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Расписание...", reply_markup = markupRasp)
        elif call.data == "personalis":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = text_perconalis, reply_markup = markupPersonalis)
        elif call.data == "settings":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "🧸 Дополнительно", reply_markup = markupSettings)
        elif call.data == "stS":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            stickerToDay(call.message, call.from_user.id)
        elif call.data == "stUw":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            stickerUpdate(call.message, call.from_user.id)
        elif call.data == "stP":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            stickerGoogle(call.message, call.from_user.id)
        elif call.data == "txUw":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
            textUpdate(call.message, call.from_user.id)
        elif call.data == "backPers":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n\n" + call.message.text, reply_markup = markupNone)
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
    bot.send_message(message.chat.id, "Используются стандартные настройки!", reply_markup=markupPersonalis)

def stickerToDay(message, id):
    bot.send_message(message.chat.id, "Пришлите стикер, и я его запомню)\n\nНу или напишите стоп")
    bot.register_next_step_handler(message, stickerToDayComplet1, id)

def stickerToDayComplet1(message, id):
    if message.content_type == "sticker":
        bd.sql(f"update bot_user set sticker_ToDay = '{message.sticker.file_id}' where user_id = {id};")
        bot.send_message(message.chat.id, "Отлично, теперь именно этот стикер ты и будешь видеть", reply_markup=markupPersonalis)
    elif message.content_type == "text":
        if (message.text).lower() == "стоп":
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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

            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_message(message.chat.id, text_perconalis, reply_markup=markupPersonalis)
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
            bot.send_sticker(message.chat.id, userI['sticker_Google'])
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!", reply_markup = markupBack)
            bot.register_next_step_handler(message, googleRasp2)
        else:
            textUser = message.text;
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
            resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
            resultAud = bd.sql(f"select id from opk_aud where name like '{textUser}';")
            if (len(resultGroup)==0 or len(resultGroup)>1) and (len(resultSotr)==0 or len(resultSotr)>1) and (len(resultAud)==0 or len(resultAud)>1):
                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!", reply_markup = markupBack)
                bot.register_next_step_handler(message, googleRasp2)
            elif len(resultGroup)==1:
                raspNew = todayGroup(resultGroup[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['sotr']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['sotr']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            elif len(resultSotr)==1:
                raspNew = todaySotr(resultSotr[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['groupName']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['groupName']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            elif len(resultAud)==1:
                raspNew = todayAud(textUser)
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для <b>{textUser}</b>\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> по <b>{a['disc']}</b> у <b>{a['name_group']}</b> c <b>{a['sotr']}</b>"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> по <b>{a['disc']}</b> у <b>{a['name_group']}</b> c <b>{a['sotr']}</b>"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            else:
                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!", reply_markup = markupBack)
                bot.register_next_step_handler(message, googleRasp2)
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
            bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!")
            bot.register_next_step_handler(message, googleRasp)
        else:
            textUser = message.text;
            textUser=textUser.replace("%", "")
            textUser=textUser.replace("'", "")
            textUser=textUser.replace('"', "")
            resultGroup = bd.sql(f"select id from opk_group where name_group like '%{textUser}%';")
            resultSotr = bd.sql(f"select id, name from opk_sotr where name like '%{textUser}%';")
            resultAud = bd.sql(f"select id from opk_aud where name like '{textUser}';")
            if (len(resultGroup)==0 or len(resultGroup)>1) and (len(resultSotr)==0 or len(resultSotr)>1) and (len(resultAud)==0 or len(resultAud)>1):
                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'ТМ-21' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!")
                bot.register_next_step_handler(message, googleRasp)
            elif len(resultGroup)==1:
                raspNew = todayGroup(resultGroup[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['sotr']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['sotr']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            elif len(resultSotr)==1:
                raspNew = todaySotr(resultSotr[0]['id'])
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для {textUser}\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['groupName']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['groupName']}</b>"
                            else:
                                textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            elif len(resultAud)==1:
                raspNew = todayAud(textUser)
                if len(raspNew)!=0:
                    dateNul = raspNew[0]['dateText']
                    textRasp=f"Расписание для <b>{textUser}</b>\n\n{dateNul}"
                    for a in raspNew:
                        if dateNul == a['dateText']:
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> по <b>{a['disc']}</b> у <b>{a['name_group']}</b> c <b>{a['sotr']}</b>"
                        else:
                            dateNul = a['dateText']
                            textRasp = textRasp + f"\n\n{a['dateText']}"
                            if a['disc']!= '- - - - - - - - - - - - - - - -':
                                textRasp = textRasp + f"\n<b>{a['para']}</b> по <b>{a['disc']}</b> у <b>{a['name_group']}</b> c <b>{a['sotr']}</b>"
                else:
                    textRasp=f"Пары для {textUser} отсутствуют!"

                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
            else:
                bot.send_sticker(message.chat.id, userI['sticker_Google'])
                bot.send_message(message.chat.id, "Совпадений не обнаружено. \n\nВ формате 'ИСП-19-1' или 'исп-19-1' \nФамилию указывайте без инициалов\nАудиторию указывайте так как в расписании!", reply_markup = markupBack)
                bot.register_next_step_handler(message, googleRasp1)
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

def todayAud(Aud):
    try:
        rasp = []
        rasp = bd.sql(f"select aud, para, dateText, sotr, opk_group.name_group, disc from opk_group, opk_rasp_group_pars where opk_rasp_group_pars.id=opk_group.id and aud={Aud} ORDER BY dateText, para;")
        return rasp
    except:
        return []

def infoStPlansWhy(message, id):
    try:
        userI = userInfo(message)
        userIG = userI['id_group']
        resultTest = str(userIG)
        if (resultTest[0:4] == "9999"):
            resultStudy = bd.sql(f"select opk_disc_info.*, opk_sotr.name as 'WhatNames', opk_group.name_group as 'Names' from opk_disc_info, opk_sotr, opk_group where id_sotr={resultTest[4:10]} and id_sotr=opk_sotr.id and id_group=opk_group.id;")
        else:
            resultStudy = bd.sql(f"select opk_disc_info.*, opk_group.name_group as 'WhatNames', opk_sotr.name as 'Names' from opk_disc_info, opk_group, opk_sotr where id_group={resultTest} and id_group=opk_group.id and id_sotr=opk_sotr.id;")
        messageText = "Информация для - "+resultStudy[0]['WhatNames']+"\nВ текущем семестре будут следующие пары:\n\n"
        for a in resultStudy:
            messageText = messageText + a['nameDisc']+"\n"+ a['Names'] +"\nПрошло - "+str(a['countHourseCurrent'])+ ", всего - "+str(a['countHourseTotal'])+"\n\n"
        bot.send_sticker(message.chat.id, userI['sticker_Google'])
        bot.send_message(message.chat.id, messageText)
        bot.send_message(message.chat.id, "Расписание...", reply_markup = markupRasp)
    except BaseException as errors:
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка вывода информации")
        errorsText = f"Ошибка вывода информации\n{message.chat.id}"
        spamsText(errorsText)

def collegeBellMessage(message, id):
    def CheckMinusOdin(text):
        if text == "-1":
            return ""
        else:
            return "("+text+")"

    try:
        userI = userInfo(message)
        resultStudy = bd.sql(f"select * from time;")
        messageText1 = "Звонки ОПК СТИ НИТУ МИСИС\n\nБудни:\n\n"
        for a in resultStudy:
            if a['hourUP_b']!="-1":
                messageText1 = messageText1 + a['title_column'] + CheckMinusOdin(a['title_dicription']) + " "
                messageText1 = messageText1 + a['hourUP_b']+":"+a['minutUP_b']+" - " + a['hourEND_b']+":"+a['minutEND_b']
                messageText1 = messageText1 + "\n\n"
        messageText2 = "Звонки ОПК СТИ НИТУ МИСИС\n\nСуббота:\n\n"
        for a in resultStudy:
            if a['hourUP_s']!="-1":
                messageText2 = messageText2 + a['title_column'] + CheckMinusOdin(a['title_dicription']) + " "
                messageText2 = messageText2 + a['hourUP_s']+":"+a['minutUP_s']+" - " + a['hourEND_s']+":"+a['minutEND_s']
                messageText2 = messageText2 + "\n\n"
        bot.send_sticker(message.chat.id, userI['sticker_Update'])
        bot.send_message(message.chat.id, messageText1)
        bot.send_message(message.chat.id, messageText2)
        bot.send_message(message.chat.id, "Расписание...", reply_markup = markupRasp)
    except BaseException as errors:
        bot.send_message(message.chat.id, f"Возникла непредвиденная ошибка. Приносим извинения за неудобства!\nИнформация об ошибке передана разработчикам.", reply_markup = markupRasp)
        print("❗️------------------------❗️ Ошибка вывода информации")
        errorsText = f"Ошибка вывода информации\n{message.chat.id}"
        spamsText(errorsText)

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
                        textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['groupName']}</b>"
                    else:
                        textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
        else:
            textRasp=f"Пары {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} отсутствуют!"

        bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
        bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
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
                        textRasp = textRasp + f"\n<b>{a['para']}</b> в <b>{a['aud']}</b> по <b>{a['disc']}</b> у <b>{a['sotr']}</b>"
                    else:
                        textRasp = textRasp + f"\n<b>{a['para']}</b> отменена"
        else:
            textRasp=f"Пары {(date.today()+timedelta(days=day)).strftime('%d-%m-%Y')} отсутствуют!"

        bot.send_sticker(message.chat.id, userI['sticker_ToDay'])
        bot.send_message(message.chat.id, textRasp, parse_mode="HTML", reply_markup = markupRasp)
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
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEl-hibN_62yFEAaAru8CywtkXQe-YGAACIRYAAu0vQUvRcTO_xqtmZiQE")
        bot.send_message(message.chat.id, "Расписание...", reply_markup = markupRasp)

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
            bot.send_message(message.chat.id, "Готово! \n\nРасписание....", reply_markup = markupRasp)
        elif len(resultSotr)>1:

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nРасписание....", reply_markup = markupRasp)
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
            bot.send_message(message.chat.id, "Готово! \n\nРасписание...", reply_markup = markupRasp)
        elif len(resultSotr)>1:

            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFz7RjHsw7N1qT3JSAq4wvuC31mB0dawACVwADrWW8FGdHzzKl2fxnKQQ")
            bot.send_message(message.chat.id, "Обнаружено множество совпадений.")
            listSotr(message, resultSotr)
        elif len(resultSotr)==1:

            bd.sql(f"insert into bot_user values({message.from_user.id}, {'9999' + str(resultSotr[0]['id'])}, 'CAACAgIAAxkBAAEEnU9icOU-sQs8pOcsqPgoCwfvCJu4EAAC_hcAAjG5QEszsE9qcKtvTCQE', 'CAACAgIAAxkBAAEF2zBjJN34Kqt7QDNUza9BDbIJgvLIPgACcxQAAhAZQEswb27LcML6ZCkE', 'CAACAgIAAxkBAAEF2zZjJN_JaBHugtLMIsfvOud9M1XF3wACRQADWbv8JfvUpDThE_jrKQQ', 'Что-то новенькое!');")
            bot.send_message(message.chat.id, "Готово! \n\nРасписание...", reply_markup = markupRasp)
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
