# -*- coding: utf-8 -*-
import telebot
import cherrypy
import requests, json
from settings import *
import threading
import server 
from requests.exceptions import ConnectionError
import logging
import xlwt
import os
from datetime import datetime, timedelta
import copy



def response(param):
    return param["status"]

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'out.log')

logging.info('Started')
t = threading.Thread(target=server.run)
t.start()


token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"

# WEBHOOK_HOST = '194.67.217.180'
# WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
# WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % token

bot = telebot.TeleBot(token)

# Наш вебхук-сервер
# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             # Эта функция обеспечивает проверку входящего сообщения
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)

class MethodGet:
    def __init__(self, method):
        self.request = {"method": "", "param": {}}
        self.request.update({"method": method})

    def transfer(self):
        try:
            print(self.request)
            response = requests.get('http://194.67.217.180:8484/get_state', json=self.request)
            logging.debug(response.text)
        except ConnectionError as e:
            logging.error(self.request)
            logging.error(u'ConnectionError')
            response = {'param': "Извините, произошла ошибка, мы работаем над её устранением. Пожалуйста, повторите попытку позже.", 'situation': False}
        else:
            response = json.loads(response.content.decode("utf-8"))
        return response

    def param(self, **kwargs):
        self.request["param"] = kwargs
        return True

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


@bot.message_handler(regexp='Адреса водоматов')
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
    result = result["score"] / 400
    logging.info(message.text)
    bot.send_message(message.chat.id, str(result)[:5:] + " литров", reply_markup=generator_menu(main_menu_list))


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
            "username": message.chat.first_name,
            "review": message.text
        }
        a.param(**recall)
        result = a.transfer()
        bot.send_message(message.chat.id, text_review_answer, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Подключиться к водомату')
def handle_start(message):
    logging.info(message.text)
    a = MethodGet("get_last_connection")
    get_last_connection = {
        "telegram": message.from_user.id
    }
    a.param(**get_last_connection)
    result = a.transfer()
    wm = result["wm"]
    if wm != 0 and wm.isdigit:
        sent = bot.send_message(message.chat.id, text_id, reply_markup=generator_menu([wm] + back_menu_list))
        bot.register_next_step_handler(sent, startWM)
    else:
        sent = bot.send_message(message.chat.id, text_id, reply_markup=generator_menu(back_menu_list))
        bot.register_next_step_handler(sent, startWM)
    
# @bot.callback_query_handler(func=lambda call: True)
# def callback_data(call):
#     a = Method("start")
#     Start = {
#         "telegram": call.message.chat.id,
#         "wm": int(call.data)
#     }
#     a.param(**Start)
#     result = a.transfer()
#     if result["situation"]:
#         a = Method("score")
#         Score = {
#             "telegram": call.message.chat.id
#         }
#         a.param(**Score)
#         result1 = a.transfer()
#         result1 = str(result1["score"] / 400)
#         send = bot.send_message(call.message.chat.id, response(result) + text_water + str(result1)[:5:] + " литров", reply_markup=generator_menu(stop_menu_list))
#     else:
#         bot.send_message(call.message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))



def startWM(message):
    if message.text.isdigit():
        a = Method("start")
        Start = {
            "telegram": message.chat.id,
            "username": message.chat.first_name,
            "wm": int(message.text)
        }
        a.param(**Start)
        result = a.transfer()
        if result["situation"]:
            a = Method("score")
            Score = {
                "telegram": message.chat.id
            }
            a.param(**Score)
            result1 = a.transfer()
            result1 = str(result1["score"] / 400)
            send = bot.send_message(message.chat.id, response(result) + text_water + str(result1)[:5:] + " литров", reply_markup=generator_menu(stop_menu_list))
            # chatID = message.chat.id
            # server.message_id.update({chatID: {'message_id': send.message_id}})
        else:
            bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))
    elif message.text == "Назад":
        bot.send_message(message.chat.id, text_welcome, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Остановить')
def handle_start(message):
    logging.info(message.text)
    a = Method("stop")
    Stop = {
        "telegram": message.chat.id,
        "username": message.chat.first_name
    }
    a.param(**Stop)
    result = a.transfer()
    a = Method("score")
    Score = {
        "telegram": message.chat.id
    }
    a.param(**Score)
    result1 = a.transfer()
    result1 = str(result1["score"] / 400)
    bot.send_message(message.chat.id, "Ваш баланс: " + str(result1)[:5:] + " литров", reply_markup=generator_menu(stop_menu_list))
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Личный кабинет')
def handle_start(message):
    logging.info(message.text)
    a = MethodGet("get_admins")
    result = a.transfer()
    print(result['param'])
    if message.chat.id in result['param']:
        bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(personal_menu_list + admin_menu_list + back_menu_list))
    else:
        bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(personal_menu_list + back_menu_list))


@bot.message_handler(regexp='Назад')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='Админ панель')
def handle_start(message):
    logging.info(message.text)
    a = MethodGet("get_admins")
    result = a.transfer()
    print(result['param'])
    if message.chat.id in result['param']:
        bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(admin_menu_stat + back_menu_list))
    else:
        bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(main_menu_list))


@bot.message_handler(regexp='За сутки')
def handle_start(message):
    logging.info(message.text)
    #за сутки
    before = datetime.today() - timedelta(days=1)
    before = str(before)[:19]
    now = str(datetime.today())[:19]

    data = {
      'method': 'get_state',
      'param':{
      'from': before,
      'to': now
      }
    }

    response = requests.get('http://194.67.217.180:8484/get_state', json=data)
    response = json.loads(response.content.decode("utf-8"))
    # Write to the sheet of the workbook 

    wmsession = {}
    sheet = {}
    book = xlwt.Workbook(encoding="utf-8")

    for session in response:
        wm = session["wm"]
        try:
            if wmsession[wm]:
                if wmsession[wm]["totalPaid"] != session["totalPaid"] or wmsession[wm]["totalHardCash"] != session["totalHardCash"]:
                    sheet = wmsession[wm]["sheet"]
                    properties = {
                        "index": wmsession[wm]["index"] + 1,
                        "totalPaid": str(session["totalPaid"]),
                        "totalHardCash": str(session["totalHardCash"]),
                        "updated": str(session["updated"])
                    }
                    wmsession.update({wm: properties})

                    index = wmsession[wm]["index"]
                    sheet.write(index, 0, str(wmsession[wm]["totalPaid"]))
                    sheet.write(index, 1, str(wmsession[wm]["totalHardCash"]))
                    sheet.write(index, 2, str(wmsession[wm]["updated"]))
        except KeyError as e:
            ID = "ID " + str(wm)
            sheet.update({wm: book.add_sheet(ID)})
            sheet[wm].write(0, 0, "Продажи")
            sheet[wm].write(0, 1, "Наличка в водомате")
            sheet[wm].write(0, 2, "Дата/время")
            sheet[wm].write(1, 0, str(session["totalPaid"]))
            sheet[wm].write(1, 1, str(session["totalHardCash"]))
            sheet[wm].write(1, 2, str(session["updated"]))
            properties = {
                "sheet": sheet,
                "index": 1,
                "totalPaid": str(session["totalPaid"]),
                "totalHardCash": str(session["totalHardCash"]),
                "updated": str(session["updated"])
            }
            wmsession.update({wm: properties})
            print(wmsession)

    book.save("state.xls")
    path = os.curdir + "/state.xls"
    bot.send_document(message.chat.id, open(path, 'rb'), reply_markup=generator_menu(back_menu_list))


@bot.message_handler(regexp='За неделю')
def handle_start(message):
    logging.info(message.text)


    #за неделю
    before = datetime.today() - timedelta(days=7)
    before = str(before)[:19]
    now = str(datetime.today())[:19]

    # Initialize a workbook 
    book = xlwt.Workbook(encoding="utf-8")

    # Add a sheet to the workbook 
    sheet1 = book.add_sheet("Python Sheet 1") 


    data = {
      'method': 'get_state',
      'param':{
      'from': before,
      'to': now
      }
    }




    try:
        response = requests.get('http://194.67.217.180:8484/get_state', json=data)
        response = json.loads(response.content.decode("utf-8"))
        # Write to the sheet of the workbook 
        sheet1.write(0, 0, "Номер водомата")
        sheet1.write(0, 1, "Продажи")
        sheet1.write(0, 2, "Наличка в водомате")
        sheet1.write(0, 3, "Дата/время")
        a = "0"
        b = "0"
        c = "0"
        d = "0"
        j = 1
        
        di = {}

        for x in response:
            try:
                if di[x["wm"]]:
                    if x["totalPaid"] != di[x['wm']]["totalPaid"] or x["totalHardCash"] != di[x['wm']]["totalHardCash"]:
                        i = 0;
                        sheet1.write(j, i, str(x["wm"]))
                        i+=1
                        sheet1.write(j, i, str(x["totalPaid"]))
                        i+=1
                        sheet1.write(j, i, str(x["totalHardCash"]))
                        i+=1
                        sheet1.write(j, i, str(x["updated"][0]) + "." + str(x["updated"][1]) + "." + str(x["updated"][2]) + " " + str(x["updated"][3]) + ":" + str(x["updated"][4]))
                        j+=1
                        di[x['wm']].update({"totalPaid": x["totalPaid"], "totalHardCash": x["totalHardCash"]})
            except KeyError:
                i = 0;
                sheet1.write(j, i, str(x["wm"]))
                i+=1
                sheet1.write(j, i, str(x["totalPaid"]))
                i+=1
                sheet1.write(j, i, str(x["totalHardCash"]))
                i+=1
                sheet1.write(j, i, str(x["updated"][0]) + "." + str(x["updated"][1]) + "." + str(x["updated"][2]) + " " + str(x["updated"][3]) + ":" + str(x["updated"][4]))
                j+=1


                sheet1 = book.add_sheet("Python Sheet 1") 
                sheet1.write(0, 0, "Продажи")
                sheet1.write(0, 1, "В кассе")
                sheet1.write(0, 2, "Дата")
                di.update({x["wm"]: {"totalPaid": x["totalPaid"], "totalHardCash": x["totalHardCash"]}})
                print(di)

    except Exception as e:
        print(e)

    book.save("state.xls")
    path = os.curdir + "/state.xls"
    bot.send_document(message.chat.id, open(path, 'rb'), reply_markup=generator_menu(back_menu_list))


@bot.message_handler(regexp='^Статистика$')
def handle_start(message):
    logging.info(message.text)
    bot.send_message(message.chat.id, text_get, reply_markup=generator_menu(my_stat + back_menu_list))


@bot.message_handler(regexp='Текущее состояние')
def handle_start(message):
    logging.info(message.text)
    a = MethodGet("statistic")
    result = a.transfer()
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(back_menu_list))


@bot.message_handler(regexp='Активные водоматы')
def handle_start(message):
    logging.info(message.text)
    a = MethodGet("connected_vodomats")
    result = a.transfer()
    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(back_menu_list))




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
        "telegram": message.chat.id,
        "username": message.chat.first_name,
        "X": message.location.latitude,
        "Y": message.location.longitude
    }
    logging.info(message.text)
    a.param(**recommends)
    result = a.transfer()
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
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
# cherrypy.config.update({
#     'server.socket_host': WEBHOOK_LISTEN,
#     'server.socket_port': WEBHOOK_PORT,
#     'server.ssl_module': 'builtin',
#     'server.ssl_certificate': WEBHOOK_SSL_CERT,
#     'server.ssl_private_key': WEBHOOK_SSL_PRIV
# })

# Собственно, запуск!
# cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})



logging.info('Finished')


bot.polling(none_stop=True, interval = 0)