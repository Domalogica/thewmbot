from flask import Flask, request, json
from settings import *

app = Flask(__name__)


@app.route('/server/param', methods=['POST'])
def server():
    method = request.json.get('method')
    param = request.json.get('param')
    if method == 'stop':
    	response = stop(param)
    if method == 'dispatch':
       response = dispatch(param)
	if method == 'upscore':
		response = upscore(param)
	return json.dumps(response)

def stop(param):
	telegram = param['telegram']
	bot.send_message(telegram, text_welcome, reply_markup=generator_menu(main_menu_list))
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
	bot.send_message(telegram, text_welcome, reply_markup=generator_menu(main_menu_list))
	return 'Success'



def run():
    app.run(host='194.67.217.180', port=8383)