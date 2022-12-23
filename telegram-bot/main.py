import telebot
from telebot import types

API_TOKEN = ***
bot = telebot.TeleBot(API_TOKEN, threaded=False)
del_but = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start_message(message):
    # service = types.ReplyKeyboardMarkup(True, True)
    # service.row("🤖 Получить chat id")
    bot.send_message(message.chat.id, '👋 Привет')


@bot.message_handler(content_types=['getid'])
def text_message(message):
    bot.send_message(message.chat.id, 'This your chat id: '+str(message.chat.id))


bot.polling(none_stop=True)

# #Если бот будет падать при ожидании отклика
# # while True:
# #     try:
# #         bot.polling(none_stop=True)
# #
# #     except Exception as e:
# #         logger.error(e)  # или просто print(e) если у вас логгера нет,
# #         # или import traceback; traceback.print_exc() для печати полной инфы
# #         time.sleep(15)
#
