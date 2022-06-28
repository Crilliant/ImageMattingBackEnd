from flask import Blueprint, request, jsonify
from config import *
from concurrent.futures import ThreadPoolExecutor
from server.tool import watercolor
from threading import Thread
from utils import *


bp = Blueprint('style_change_transfer', __name__, url_prefix='/api/style')


# TODO: 添加水彩效果转换
@bp.route('/watercolor')
def change_to_watercolor():
    return
