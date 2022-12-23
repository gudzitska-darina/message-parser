'''Перед запуском телеграм-клиента нужно запустить бота и узнать chat id,
без него клиент не будет знать куда отправлять ошибки.
Запуск клиента осуществляется с консоли в формате python3 app.py chat_id.'''
from telethon import TelegramClient, events
import telebot
import requests
from pytz import timezone
from sys import argv
script, c_id = argv

#Константы для работы клиента и бота
API_TOKEN = ***
API_ID = ***
API_HASH = ***
#CHANNEL_SOURCE= ***
CHANNEL_SOURCE_TEST= ***
bot = telebot.TeleBot(API_TOKEN, threaded=False)
CHAT_ID = c_id

#Создание и отправка сообщения в бот с указаными ошибками
def create_message_bot(l, t):
        prefix = f"[{t}]\nNew message:"
        message = "\n"
        if len(l) == 0:
            bot.send_message(CHAT_ID, f"[{t}]\nError not found")
        else:
            for i in l:
                message += i + "\n"
            bot.send_message(CHAT_ID, prefix+message)


#Создание GET запроса на сайт и возврат словаря с реультатами запроса
def create_get_inquiry(message):
    params = {'text': message,
              'language': 'uk-UA'}
    resp = requests.get('https://languagetool.org/api/v2/check', params=params)
    return resp


#Обработка результата заброса и формирование текса сообщения
def create_text_mistekes(resp):
    result = []
    options = ""
    for i in resp.json()["matches"]:
        result.append(f"{i['shortMessage']}: {i['message']}\nМожливі виправлення:")
        for j in i['replacements']:
            options += j['value'] + ", "
        result.append(options)
    return result


#создание телеграм-клиента и обработка события нового сообщения
def telegram_parser(send_message_func = create_get_inquiry, loop=None):
    session = 'gazp'

    client = TelegramClient(session, API_ID, API_HASH, loop=loop)
    client.start()

    #@client.on(events.NewMessage(chats=CHANNEL_SOURCE))
    @client.on(events.NewMessage(chats=CHANNEL_SOURCE_TEST))
    async def handler(event):
        #Вывод результата парсинга канала в консоль
        if send_message_func is None:
            print(event.raw_text, '\n')
        #Запрос, создание сообщения и его отправка
        else:
            list_answer = send_message_func(event.raw_text)
            message_text = create_text_mistekes(list_answer)
            datetime_obj = event.date.astimezone(timezone('Europe/Kyiv'))
            create_message_bot(message_text, datetime_obj)

    return client

if __name__ == "__main__":

    client = telegram_parser()

    client.run_until_disconnected()

#Это нужно что бы бот не отключался после первого сообщения, а находтлся в режиме ожидания
bot.polling(none_stop=True, interval=0)