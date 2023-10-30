# @File Name:     openai
# @Author :       Jun
# @date:          2023/10/25
# @Description :

import random
import traceback

import loguru
import openai
import tiktoken
from tenacity import retry, stop_after_attempt

from config import config

logger = loguru.logger

GPT_MODEL_MAX_TOKEN_DICT = {
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-0301": 4096,
    "gpt-4": 8192,
    "gpt-4-0314": 8192,
}


def build_api_key_list():
    api_keys = []
    for key in config['openai']['api_keys']:
        api_keys.append(key['key'])
    return api_keys


api_pool = build_api_key_list()


@retry(stop=stop_after_attempt(5))
def call_openai_engine(engine='gpt-3.5-turbo',
                       system="",
                       prompt="",
                       stop_tokens=None):
    openai.api_key = random.choice(api_pool)
    try:
        if engine in GPT_MODEL_MAX_TOKEN_DICT:
            sample = openai.ChatCompletion.create(
                model=engine,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=config['openai']['temperature'],
                timeout=config['openai']['timeout'],
                # stop=stop_tokens,
            )
        else:
            raise ValueError("Unknown GPT model type")
    except Exception as e:
        logger.error(f'Retrying querying OpenAI {engine}...')
        logger.error(f"api-key: {openai.api_key}")
        logger.error(traceback.format_exc())
        raise e
    return sample


def encoding(text: str, engine='gpt-3.5-turbo'):
    encoder = tiktoken.encoding_for_model(engine)
    return encoder.encode(text)


def decoding(embedding: list, engine='gpt-3.5-turbo'):
    decoder = tiktoken.encoding_for_model(engine)
    return decoder.decode(embedding)


def get_openai_generation(engine, openai_api_response):
    if openai_api_response is None:
        return None
    if engine in GPT_MODEL_MAX_TOKEN_DICT:
        """An example chat API response looks as follows:
            {
                'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
                'object': 'chat.completion',
                'created': 1677649420,
                'model': 'gpt-3.5-turbo',
                'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
                'choices': [
                    {
                        'message': {
                            'role': 'assistant',
                            'content': 'The 2020 World Series was played in Arlington, ...'},
                        'finish_reason': 'stop',
                        'index': 0
                    }
                ]
            }
        """
        generated_content = openai_api_response['choices'][0]['message']['content']
    else:
        raise ValueError('Unknown GPT model type')
    return generated_content
