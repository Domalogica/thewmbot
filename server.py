from flask import Flask, request, json

app = Flask(__name__)


@app.route('/server/param', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        print("POST")
        return json.dumps("POST")
    else:
        print("GET")
        return json.dumps("GET")

def run():
    app.run(host='194.67.217.180', port=8383)
