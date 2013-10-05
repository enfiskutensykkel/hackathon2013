from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route("/", methods=["POST"])
def receive_quote():
    print request.json
    return jsonify({'debug': 'hello world'})


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)