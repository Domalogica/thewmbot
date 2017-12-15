from flask import Flask, request, json

app = Flask(__name__)


@app.route('/server/param', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        print(request)
        return json.dumps("POST")
    else:
        print(request)
        return json.dumps("GET")

def run():
    app.run(host='194.67.217.180', port=8383)


# @app.route("/bot/param", methods=["POST"])
# def Bot():

#     response = {'method': 'not exist, error method'}

#     method = request.json.get('method')
#     param = request.json.get('param')

#     if method == 'addUser':
#         response = AddUser.addUser(param)

#     if method == 'start':
#         response = Start.start(param.get('telegram'), param.get('wm'))

#     if method == 'stop':
#         response = Stop.stop(int(param.get('telegram')), {'sender': 'bot'})

#     if method == 'setSettings':
#         response = SetSettings.setSettings(int(request.json.get('wm')), param)

#     if method == 'score':
#         response = module.get_score(param['telegram'])

#     if method == 'recall':
#         response = module.recalls(param)

#     if method == 'get_location':
#         response = module.get_location(param.get('city'))

#     if method == 'recommends':
#         response = module.get_location(param.get('city'))

#     return json.dumps(response)