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
	if method == 'upscore':
		response = upscore(param)
	return json.loads(response.content.decode("utf-8"))



def response(param):
	print(param)
    return param["param"]


def stop(param):
	param = response(param)
	bot.send_message(param["telegram"], param["data"], reply_markup=generator_menu(main_menu_list))
	return 'Success'

def dispatch(param):
	telegram = param['telegram']
	message = param['message']
	for ID in telegram:
		bot.send_message(ID, message)
	return 'Success'

def upscore(param):
	telegram = param['telegram']
	bot.edited_message()
	bot.send_message(telegram, text_welcome)
	return 'Success'



def run():
    app.run(host='194.67.217.180', port=8383)