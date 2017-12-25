from flask import Flask, request, json
from settings import *
import telebot

# from main import message_id

app = Flask(__name__)

token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"
bot = telebot.TeleBot(token)

@app.route('/server/param', methods=['POST'])
def server():
	response = {'method': 'error'}
	param = request.json
	if param["method"] == 'stop':
		response = stop(param)
	if param["method"] == 'dispatch':
		response = dispatch(param)
	if param["method"] == 'start':
		response = start(param)
	return json.dumps(response)


def generator_menu(menu_list, dop=None):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    if dop is not None:
        user_markup.row(dop)
    return user_markup




def stop(param):
	bot.send_message(param["param"]["telegram"], param["param"]["data"], reply_markup=generator_menu(main_menu_list))
	return {'Success'}

# def dispatch(param):
# 	telegram = param['telegram']
# 	message = param['message']
# 	for ID in param['telegram']:
# 		bot.send_message(ID, message)
# 	return 'Success'

def start(param):
	bot.edit_message_text(chat_id=param["telegram"], message_id=message.message_id, text=param["score"])
	main.message_id.pop(param["telegram"])
	return {'Success'}



def run():
    app.run(host='194.67.217.180', port=8383)