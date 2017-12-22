from flask import Flask, request, json
from settings import *
import telebot

app = Flask(__name__)

token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"
bot = telebot.TeleBot(token)

@app.route('/server/param', methods=['POST'])
def server():
	method = request.json.get('method')
	print(method)
	if method == 'stop':
		response = stop(method)
	if method == 'dispatch':
		response = dispatch(method)
	if method == 'start':
		response = start(method)
	return json.dumps(response)


def generator_menu(menu_list, dop=None):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    if dop is not None:
        user_markup.row(dop)
    return user_markup


def stop(method):
	bot.send_message(method["telegram"], method["param"], reply_markup=generator_menu(main_menu_list))
	return 'Success'

# def dispatch(param):
# 	telegram = param['telegram']
# 	message = param['message']
# 	for ID in param['telegram']:
# 		bot.send_message(ID, message)
# 	return 'Success'

def start(method):
	bot.send_message(method["telegram"], method["score"])
	return 'Success'



def run():
    app.run(host='194.67.217.180', port=8383)