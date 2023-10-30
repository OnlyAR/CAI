# @File Name:     config
# @Author :       Jun
# @date:          2023/10/25
# @Description :

import json
import os


def load_config():
    with open('../config.json', 'r', encoding='utf8') as f:
        conf = json.load(f)
    return conf


config = load_config()
