import os
from config import image_upload_path, image_mask_path, image_download_path
from flask import Flask
from BluePoints.image_transfer import bp as image_bp
from BluePoints.background_transfer import bp as background_bp
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(image_bp)
app.register_blueprint(background_bp)

CORS(app, resource=r'/*')

if not os.path.exists(image_upload_path):
    os.makedirs(image_upload_path)
if not os.path.exists(image_mask_path):
    os.makedirs(image_mask_path)
if not os.path.exists(image_download_path):
    os.makedirs(image_download_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
