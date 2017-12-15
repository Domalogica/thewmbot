from flask import Flask

app = Flask(__name__)


@app.route('/server/param', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        print("POST")
    else:
        print("GET")

if __name__ == '__main__':
    app.run(host='194.67.217.180', port=8383)
