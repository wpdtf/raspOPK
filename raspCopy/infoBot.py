import telebot
from telebot import types
import random
import time

from errors_dmitry import spamsText

bot = telebot.TeleBot()

stickers = ['CAACAgIAAxkBAAEGD7FjRZ4g91p6FHBuTEQWo_IZlGuwBQAC8x0AAuAc8Ul6TVJ5LgzTAyoE',
'CAACAgIAAxkBAAEGD7NjRZ4q37HcP2aMq_HImnpdh1xHWwAC9CYAAqm84UmzOVOfUKmTyyoE',
'CAACAgIAAxkBAAEGD7VjRZ41R115BpPdzoRQGhFfs02qSAACFhIAAih6SUhHyUY6AAH61_MqBA',
'CAACAgIAAxkBAAEGD7djRZ4_ID_2IkjG5pRAKTM3LNsVMgAC9xMAAoT4SEgzY3LaVBSm1yoE',
'CAACAgIAAxkBAAEGD7ljRZ5N1F9--n3naitNFT4p1eV6hAACahsAAimKQEsKSwdB82j_byoE',
'CAACAgIAAxkBAAEGD7tjRZ5ojPpn-L7UTEgqLBwE7EUB0AAC-RUAAiexmUuB_XOFMbBf1CoE',
'CAACAgIAAxkBAAEGD8pjRaSoSDSuCZezuvzddzwSSNroowACgA4AAtR1CUrMgw4BzHWIqSoE',
'CAACAgIAAxkBAAEGD8hjRaSiJExk1-zCZynt_Y-tKS-K_QACmQADpsrIDJpsbCQdyOXRKgQ',
'CAACAgIAAxkBAAEGD8ZjRaSdqfTZMivNTjx5uIUdsPoJEAACyA0AAn_OkUphzMqBNLJMPSoE',
'CAACAgIAAxkBAAEGD8RjRaSczuRKXIx7upIkXxN6DhwYuQACsAwAAscrkUojJDJifVZBrSoE']



markupNone = types.InlineKeyboardMarkup(row_width=1)

markupRasp = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('статистика сообщений', callback_data="bt1")
itemRasp2 = types.InlineKeyboardButton('статистика обновлений', callback_data="bt2")
markupRasp.add(itemRasp1, itemRasp2)

markupClearMes = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('Очистить нумерацию', callback_data="clearMessage_")
itemRasp2 = types.InlineKeyboardButton('Назад', callback_data="back")
markupClearMes.add(itemRasp1, itemRasp2)

markupClearUpdate = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('Очистить нумерацию', callback_data="clearUpdate_")
itemRasp2 = types.InlineKeyboardButton('Назад', callback_data="back")
markupClearUpdate.add(itemRasp1, itemRasp2)

markupYesNo1 = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('Да', callback_data="clearMessage")
itemRasp2 = types.InlineKeyboardButton('Нет', callback_data="back")
markupYesNo1.add(itemRasp1, itemRasp2)

markupYesNo2 = types.InlineKeyboardMarkup(row_width=1)
itemRasp1 = types.InlineKeyboardButton('Да', callback_data="clearUpdate")
itemRasp2 = types.InlineKeyboardButton('Нет', callback_data="back")
markupYesNo2.add(itemRasp1, itemRasp2)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "bt1":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            staticMessage()
        elif call.data == "bt2":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Старое сообщение:\n" + call.message.text, reply_markup = markupNone)
            staticUpdate()
        elif call.data == "back":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Меню", reply_markup = markupRasp)
        elif call.data == "clearMessage_":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Отвечаешь?", reply_markup = markupYesNo1)
        elif call.data == "clearUpdate_":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "Отвечаешь?", reply_markup = markupYesNo2)
        elif call.data == "clearMessage":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "ок", reply_markup = markupNone)
            clearNum()
        elif call.data == "clearUpdate":
            bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.id, text = "ок", reply_markup = markupNone)
            clearUpdate()


def numMessage():
    messageFile = open('num.txt', 'r')
    numMessage = int(*messageFile)
    numMessage += 1
    messageFile.close()
    messageFile = open('num.txt', 'w')
    messageFile.write(str(numMessage))
    messageFile.close()


def clearNum():
    messageFile = open('num.txt', 'w')
    messageFile.write(str(0))
    messageFile.close()
    bot.send_message(408663065, f"Добби поработал хозяин", reply_markup = markupRasp)

def clearUpdate():
    updateFile = open('update.txt', 'w')
    updateFile.write(str(0))
    updateFile.close()
    bot.send_message(408663065, f"Добби поработал хозяин", reply_markup = markupRasp)


def staticMessage():
    messageFile = open('num.txt', 'r')
    numMessage = int(*messageFile)
    messageFile.close()
    bot.send_sticker(408663065, random.choice(stickers))
    bot.send_message(408663065, f"Добби поработал хозяин.\nВсего сообщений {numMessage}\n\n *сообщения*", reply_markup = markupClearMes)

def staticUpdate():
    updateFile = open('update.txt', 'r')
    numUpdate = int(*updateFile)
    updateFile.close()
    bot.send_sticker(408663065, random.choice(stickers))
    bot.send_message(408663065, f"Добби поработал хозяин.\nВсего уведомлений отправлено {numUpdate}\n\n *уведомлений*", reply_markup = markupClearUpdate)


def numUpdate():
    updateFile = open('update.txt', 'r')
    numUpdate = int(*updateFile)
    numUpdate += 1
    updateFile.close()
    updateFile = open('update.txt', 'w')
    updateFile.write(str(numUpdate))
    updateFile.close()



def start(message, id):
    if id != 408663065:
        bot.send_message(message.chat.id, "Работает только с особыми людьми.")
    else:
        bot.send_sticker(408663065, random.choice(stickers))
        bot.send_message(408663065, "Добби готов работать.", reply_markup = markupRasp)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    start(message, message.from_user.id)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    start(message, message.from_user.id)


def funcStart1():
    try:
        spamsText(f"опаньки, log`s онлайн привет")
        bot.polling(none_stop=True)
    except BaseException as errors:
        spamsText(f"Бот отвалился *особый*\n{errors}")
        funcStart2()

def funcStart2():
    try:
        spamsText(f"опаньки, log`s онлайн привет")
        bot.polling(none_stop=True)
    except BaseException as errors:
        spamsText(f"Бот отвалился *особый*\n{errors}")
        funcStart1()

if __name__ == '__main__':
    funcStart1()
