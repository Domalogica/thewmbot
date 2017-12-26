from flask import Flask, request, json
from settings import *
import telebot

# from main import message_id

app = Flask(__name__)

token = "321273335:AAEPNNqf3TFGmmekxF4pKzgDEO90Isl6d3k"
bot = telebot.TeleBot(token)

message_id = {}

@app.route('/server/param', methods=['POST'])
def server():
	response = {'method': 'error'}
	param = request.json
	print(param)
	if param["method"] == 'stop':
		response = stop(param)
	if param["method"] == 'dispatch':
		response = dispatch(param)
	if param["method"] == 'status':
		response = status(param)
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
	message_id.pop(param["param"]["telegram"])
	return ['Success']

# def dispatch(param):
# 	telegram = param['telegram']
# 	message = param['message']
# 	for ID in param['telegram']:
# 		bot.send_message(ID, message)
# 	return 'Success'



def start(param):
	print(param)
	bot.send_message(param["param"]["telegram"], text_get, reply_markup=generator_menu(stop_menu_list))
	userID = message.from_user.id
	message_id.update({userID: {'message_id': message.chat.id}})
	return ['Success']

def status(param):
	print(message_id)
	bot.edit_message_text(chat_id=param["param"]["telegram"], message_id=message_id[param["param"]["telegram"]]["message_id"], text=param["param"]["score"])
	message_id.pop(param["param"]["telegram"])
	return ['Success']



def run():
    app.run(host='194.67.217.180', port=8383)