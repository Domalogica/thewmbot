# -*- coding: utf-8 -*-
import telebot
import cherrypy
import requests, json
from settings import *
import threading
import server 
from requests.exceptions import ConnectionError
import logging

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'out.log')

logging.info('Started')
t = threading.Thread(target=server.run)
t.start()


token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"

WEBHOOK_HOST = '194.67.217.180'
WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % token

bot = telebot.TeleBot(token)


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

class Method:
    def __init__(self, method):
        self.request = {"method": "", "param": {}}
        self.request.update({"method": method})

    def transfer(self):
        try:
            response = requests.post('http://194.67.217.180:8484/bot/param', json=self.request)
            logging.debug(response.text)
        except ConnectionError as e:
            logging.error(self.request)
            logging.error(u'ConnectionError')
            response = {'param': "Извините, произошла ошибка, мы работаем над её устранением. Пожалуйста, повторите попытку позже.", 'situation': False}
        else:
            response = json.loads(response.content.decode("utf-8"))
        print(response)
        return response

    def param(self, **kwargs):
        self.request["param"] = kwargs
        return True



def generator_menu(menu_list, dop=None):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    if dop is not None:
        user_markup.row(dop)
    return user_markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    a = Method("addUser")
    AddUser = {
        "telegram": message.from_user.id,
        "username": message.chat.first_name
    }
    a.param(**AddUser)
    result = a.transfer()
    bot.send_message(message.chat.id, text_welcome, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Ближайшие водоматы')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, wada, reply_markup=generator_menu(back_menu_list))
    bot.send_message(message.chat.id, f, reply_markup=generator_menu(back_menu_list))


@bot.message_handler(regexp='Баланс')
def handle_start(message):
    a = Method("score")
    Score = {
        "telegram": message.from_user.id
    }
    a.param(**Score)
    result = a.transfer()
    print(result)
    result = result["score"] / 400
    logging.info(message.text)
    bot.send_message(message.chat.id, str(result) + " литров", reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Оставить отзыв')
def handle_start(message):
    logging.info(message.text)
    sent = bot.send_message(message.chat.id, text_review, reply_markup=generator_menu(back_menu_list))
    bot.register_next_step_handler(sent, feedback)


def feedback(message):
    logging.info(message.text)
    if message.text == "Назад":
        bot.send_message(message.chat.id, text_welcome, reply_markup=generator_menu(main_menu_list))
    else:
        a = Method("recall")
        recall = {
            "telegram": message.from_user.id,
            "review": message.text
        }
        a.param(**recall)
        result = a.transfer()
        print(result)
        bot.send_message(message.chat.id, text_review_answer, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Подключиться к водомату')
def handle_start(message):
    logging.info(message.text)
    items = [521, 321, 121]
    keypad = telebot.types.InlineKeyboardMarkup()
    for r in items:
        button = telebot.types.InlineKeyboardButton(text=r, callback_data=r)
        keypad.add(button)
    sent = bot.send_message(message.chat.id, "Быстрое подключение", reply_markup=keypad)
    bot.register_next_step_handler(sent, callback_data)
    sent = bot.send_message(message.chat.id, text_id, reply_markup=generator_menu(back_menu_list))
    bot.register_next_step_handler(sent, startWM)


def callback_data(call):
    a = Method("start")
    Start = {
        "telegram": call.message.chat.id,
        "wm": int(call.data)
    }
    a.param(**Start)
    result = a.transfer()
    print(result)
    if result["situation"]:
        bot.send_message(call.message.chat.id, response(result) + text_water, reply_markup=generator_menu(stop_menu_list))
    else:
        bot.send_message(call.message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))
    return True

def response(param):
    return param["param"]


def startWM(message):
    logging.info(message.text)
    if message.sticker:
        bot.send_message(message.chat.id, command_error, reply_markup=generator_menu(main_menu_list))
    elif message.text.isdigit():
        a = Method("start")
        Start = {
            "telegram": message.from_user.id,
            "wm": int(message.text)
        }
        a.param(**Start)
        result = a.transfer()
        print(result)
        if result["situation"]:
            bot.send_message(message.chat.id, response(result) + text_water, reply_markup=generator_menu(stop_menu_list))
        else:
            bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))
    elif message.text != "Назад":
        bot.send_message(message.chat.id, command_error, reply_markup=generator_menu(main_menu_list))
    else:
        bot.send_message(message.chat.id, text_welcome, reply_markup=generator_menu(main_menu_list))
    return True 

@bot.message_handler(regexp='Остановить')
def handle_start(message):
    logging.info(message.text)
    a = Method("stop")
    Stop = {
        "telegram": message.from_user.id
    }
    print(message.from_user.id)
    a.param(**Stop)
    result = a.transfer()
    print(result)
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Личный кабинет')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(personal_menu_list + back_menu_list))


@bot.message_handler(regexp='Назад')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='^Статистика$')
def handle_start(message):
    logging.info(message.text)
    a = Method("monitoring")
    monitoring = {
        "telegram": message.from_user.id
    }
    a.param(**monitoring)
    result = a.transfer()
    print(result)
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(stat + back_menu_list))


@bot.message_handler(regexp='Моя статистика')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(my_stat + back_menu_list))



@bot.message_handler(regexp='Статистика по водоматам')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(stat_menu + back_menu_list))


# @bot.message_handler(regexp='Рекомендовать место')
# def handle_start(message):
#     button = types.KeyboardButton(text='Рекомендовать место', request_location=True)
#     keypad.add(button)
#     bot.send_message(message.chat.id, location, reply_markup=generator_menu(back_menu_list))


@bot.message_handler(content_types=['location'])
def handle_start(message):
    a = Method("recommends")
    recommends = {
        "telegram": message.from_user.id,
        "X": message.location.latitude,
        "Y": message.location.longitude
    }
    logging.info(message.text)
    a.param(**recommends)
    result = a.transfer()
    print(result)
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Количество продаж за сутки')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(stat + back_menu_list))


@bot.message_handler(regexp='Количество продаж через бот')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(stat + back_menu_list))


@bot.message_handler(regexp='Обратная связь')
def handle_start(message):
    logging.info(message.text)
    keypad = generator_menu(feedback_menu)
    button = telebot.types.KeyboardButton(text='Рекомендовать место', request_location=True)
    keypad.add(button)
    button = telebot.types.KeyboardButton(text='Назад')
    keypad.add(button)
    bot.send_message(message.chat.id, text_get, reply_markup=keypad)



# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

logging.info('Finished')