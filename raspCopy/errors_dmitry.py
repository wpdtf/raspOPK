import telebot
import random
import time

bot = telebot.TeleBot("5608566941:AAEfvPnnO_7yzAA0B8Pl661AJQYILgUNkiY")



def spamsText(textErrors):
    bot.send_message(408663065, "-----------")
    if len(textErrors) > 4096:
        for x in range(0, len(textErrors), 4096):
            bot.send_message(408663065, textErrors[x:x+4096])
    else:
        bot.send_message(408663065, textErrors)
