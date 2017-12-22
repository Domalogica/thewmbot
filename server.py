from flask import Flask, request, json
from settings import *
import telebot

app = Flask(__name__)

token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"
bot = telebot.TeleBot(token)

@app.route('/server/param', methods=['POST'])
def server():
	method = request.json.get('method')
	param = request.json.get('param')
	print(method)
	print("\n")
	print(param)
	if method == 'stop':
		response = stop(param)
	if method == 'dispatch':
		response = dispatch(param)
	if method == 'start':
		response = start(param)
	return json.dumps(response)

param = {'method': 'start', 'param': '', 'situation': False, 'score': ''}
def generator_menu(menu_list, dop=None):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    if dop is not None:
        user_markup.row(dop)
    return user_markup


def stop(param):
	bot.send_message(param["telegram"], param["data"], reply_markup=generator_menu(main_menu_list))
	return 'Success'

# def dispatch(param):
# 	telegram = param['telegram']
# 	message = param['message']
# 	for ID in param['telegram']:
# 		bot.send_message(ID, message)
# 	return 'Success'

def start(param):
	bot.send_message(param["telegram"], param["score"])
	return 'Success'



def run():
    app.run(host='194.67.217.180', port=8383)