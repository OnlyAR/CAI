# @File Name:     cache
# @Author :       Jun
# @date:          2023/10/27
# @Description :

import os
import json


def generate_cache_file(args):
    """
    Generate cache file if not exists.
    :return: cache file path
    """
    cache_file_path = os.path.join(args.cache_path, args.task, args.exp_name, args.ie_novel, 'cache.json')
    if not os.path.exists(os.path.dirname(cache_file_path)):
        os.makedirs(os.path.dirname(cache_file_path))
    if not os.path.exists(cache_file_path):
        with open(cache_file_path, 'w', encoding='utf8') as f:
            f.write('{}')
    return cache_file_path


def get_cache(args, prompt):
    cache_file_path = generate_cache_file(args)
    with open(cache_file_path, 'r', encoding='utf8') as f:
        cache = json.load(f)
    if prompt in cache:
        return cache[prompt]
    else:
        return None


def add_cache(args, prompt, response):
    cache_file_path = generate_cache_file(args)
    with open(cache_file_path, 'r', encoding='utf8') as f:
        cache = json.load(f)
    cache[prompt] = response
    with open(cache_file_path, 'w', encoding='utf8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)
