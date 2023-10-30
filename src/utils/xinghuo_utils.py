# @File Name:     xinghuo_utils.py
# @Author :       Jun
# @date:          2023/10/30
# @Description :

import random
import traceback

import loguru
import tiktoken
from tenacity import retry, stop_after_attempt

from config import config
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

logger = loguru.logger

MODEL_MAX_TOKEN_DICT = {
    "v1.5": 4096,
    "v2": 8192,
    "v3": 8192,
}

MODEL_DOMAIN_DICT = {
    "v1.5": "general",
    "v2": "general2",
    "v3": "general3",
}

MODEL_URL_DICT = {
    "v1.5": "ws://spark-api.xf-yun.com/v1.1/chat",
    "v2": "ws://spark-api.xf-yun.com/v2.1/chat",
    "v3": "ws://spark-api.xf-yun.com/v3.1/chat",
}


def build_auth(model):
    cur_time = datetime.now()
    date = format_date_time(mktime(cur_time.timetuple()))
    tmp = "host: " + "spark-api.xf-yun.com" + "\n"
    tmp += "date: " + date + "\n"
    tmp += "GET " + "/v1.1/chat" + " HTTP/1.1"

