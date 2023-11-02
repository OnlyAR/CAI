# @File Name:     openai_utils
# @Author :       Jun
# @date:          2023/10/31
# @Description :
import random

import loguru
import tiktoken
from langchain.chat_models import ChatOpenAI

from config import config

logger = loguru.logger


def build_api_key_list():
    api_keys = []
    for key in config['openai']['api_keys']:
        api_keys.append(key['key'])
    return api_keys


api_pool = build_api_key_list()


def encoding(text: str, engine=config['openai']['engine']):
    encoder = tiktoken.encoding_for_model(engine)
    return encoder.encode(text)


def decoding(embedding: list, engine=config['openai']['engine']):
    decoder = tiktoken.encoding_for_model(engine)
    return decoder.decode(embedding)


def token_length(text: str, engine=config['openai']['engine']):
    return len(encoding(text, engine))


def openai_llm():
    return ChatOpenAI(temperature=config['openai']['temperature'],
                      model_name=config['openai']['engine'],
                      openai_api_key=random.choice(api_pool),
                      request_timeout=config['openai']['timeout'])
