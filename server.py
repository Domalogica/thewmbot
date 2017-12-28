from flask import Flask, request, json
from settings import *
import telebot

message_id = {}

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
	# if param["method"] == 'status':
	# 	response = status(param)
	return json.dumps(response)


def generator_menu(menu_list, dop=None):
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for item in menu_list:
        user_markup.row(item)
    if dop is not None:
        user_markup.row(dop)
    return user_markup




def stop(param):
	bot.send_message(param["param"]["telegram"], param["param"]["status"], reply_markup=generator_menu(main_menu_list))
	# message_id.pop(param["param"]["telegram"])
	return ['Success']

# def dispatch(param):
# 	telegram = param['telegram']
# 	message = param['message']
# 	for ID in param['telegram']:
# 		bot.send_message(ID, message)
# 	return 'Success'



# def start(param):
# 	print(param)
# 	if result["situation"]:
# 	    bot.send_message(message.chat.id, response(result) + text_water, reply_markup=generator_menu(stop_menu_list))
# 	else:
# 	    bot.send_message(message.chat.id, response(result), reply_markup=generator_menu(main_menu_list))
# 	print("START")
# 	bot.send_message(param["param"]["telegram"], text_get)
# 	print("START")
#     # chatID = param["param"]["telegram"]
#     # server.message_id.update({chatID: {'message_id': message.message_id}})
# 	return ['Success']

# def status(param):
# 	telegram = param["param"]["telegram"]
# 	print(param)
# 	print(message_id[telegram]['message_id'])
# 	liters = str(param["param"]["score"] / 400) + " литров"
# 	bot.delete_message(chat_id=telegram, message_id=message_id[telegram]['message_id'])
# 	send = bot.send_message(param["param"]["telegram"], text_water + liters, reply_markup=generator_menu(stop_menu_list))
# 	chatID = telegram
# 	message_id.update({chatID: {'message_id': send.message_id}})
# 	return ['Success']



def run():
    app.run(host='194.67.217.180', port=8383)







