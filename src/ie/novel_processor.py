# @File Name:     novel_processor
# @Author :       Jun
# @date:          2023/10/27
# @Description :

import loguru

from ie import split_func
from utils.openai_utils import encoding, decoding

logger = loguru.logger


def split_by_chapter(text, name):
    splitter = None
    for cls in split_func.__dict__.values():
        if hasattr(cls, 'name') and getattr(cls, 'name') == name:
            splitter = cls()
            break
    if splitter is None:
        logger.error(f'No splitter named {name} is found.')
        raise ValueError(f'No splitter named {name} is found.')
    return splitter.split(text)


def split_by_tokens(text, max_token):
    embedding = encoding(text)
    text_list = []
    while len(embedding) > max_token:
        text_list.append(embedding[:max_token])
        embedding = embedding[max_token:]
    text_list.append(embedding)
    text_list = [decoding(t) for t in text_list]
    return text_list
