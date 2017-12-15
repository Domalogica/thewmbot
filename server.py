from flask import Flask, request

app = Flask(__name__)


@app.route('/server/param', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")

def run():
    app.run(host='194.67.217.180', port=8383)
