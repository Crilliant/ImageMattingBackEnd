from flask import Flask, Response
from BluePoints.image_transfer import bp as transfer
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(transfer)

CORS(app, resource=r'/*')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
