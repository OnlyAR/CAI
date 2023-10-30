# @File Name:     extracter
# @Author :       Jun
# @date:          2023/10/27
# @Description :
import json
import re

import loguru

from ie.novel_processor import split_by_chapter, split_by_tokens
from utils.cache import get_cache, add_cache
from utils.openai_utils import call_openai_engine, get_openai_generation, encoding

logger = loguru.logger


def split_chapters_by_tokens(chapters, max_token):
    new_chapters = []
    for chapter in chapters:
        token_len = len(encoding(chapter))
        if token_len > max_token:
            logger.warning(f'Chapter length {token_len} exceeds max token {max_token}.')
            new_chapters += split_by_tokens(chapter, max_token)
        else:
            new_chapters.append(chapter)
    return new_chapters


def build_prompt(template, info: dict):
    r = {k: v for k, v in template.items()}
    for key in template:
        for k, v in info.items():
            r[key] = r[key].replace("${" + k + "}", v)
        if re.search(r'\${.*}', r[key]):
            miss = re.findall(r'\${(.*)}', r[key])
            raise ValueError(f'Key {miss} in template is not replaced.')
    return r


def process_request(system, prompt, args):
    response_text = get_cache(args, system + "##" + prompt)
    if response_text is not None:
        logger.info(f'Get response from cache: {response_text}')
        return response_text
    try:
        response = call_openai_engine(engine=args.engine, system=system, prompt=prompt)
        if response is None:
            raise ValueError('OpenAI response is None.')

        response_text = get_openai_generation('gpt-3.5-turbo', response)
        add_cache(args, system + "##" + prompt, response_text)
        return response_text
    except json.decoder.JSONDecodeError:
        logger.error(response_text)
        logger.error('OpenAI response is not a valid json.')
        return ""
    except Exception as e:
        logger.error(f'Error querying OpenAI {args.engine} prompt: {prompt}...')
        logger.error(e)
        return ""


def extract_description_refine(text, info, template, args):
    """
    (Refine)
    Extract description of a character.
    :return: a dict of descriptions
             {role: [description1, description2, ...]}
    """
    first_template = template['description']
    left_template = template['refine_description']
    chapters = split_by_chapter(text, args.ie_novel)
    chapters = split_chapters_by_tokens(chapters, args.max_token)

    roles = info['roles']
    above = ""
    descriptions = {}
    for role in roles:
        descriptions[role] = None
        for chapter in chapters:
            temp_info = {k: v for k, v in info.items() if isinstance(v, str)}
            temp_info['role'] = role
            temp_info['text'] = chapter
            temp_info['above'] = above
            if descriptions[role] is None:
                temp_template = build_prompt(first_template, temp_info)
            else:
                temp_template = build_prompt(left_template, temp_info)
            system = temp_template['system']
            prompt = temp_template['prompt']
            logger.info(f'Querying OpenAI {args.engine}, info: {temp_info}\n')
            above = process_request(system=system, prompt=prompt, args=args).strip()
            descriptions[role] = above
    return descriptions


def extract_description_mapreduce(text, info, template, args):
    """
    (MapReduce)
    Extract description of a character.
    :return: a dict of descriptions
             {role: [description1, description2, ...]}
    """
    template = template['description']
    chapters = split_by_chapter(text, args.ie_novel)
    chapters = split_chapters_by_tokens(chapters, args.max_token)

    roles = info['roles']
    descriptions = {}
    for role in roles:
        descriptions[role] = []
        for chapter in chapters:
            temp_info = {k: v for k, v in info.items() if isinstance(v, str)}
            temp_info['role'] = role
            temp_info['text'] = chapter
            temp_template = build_prompt(template, temp_info)
            system = temp_template['system']
            prompt = temp_template['prompt']
            logger.info(f'Querying OpenAI {args.engine}, info: {temp_info}\n')
            descriptions[role].append(process_request(system=system, prompt=prompt, args=args).strip())
    return descriptions


def summary_description_mapreduce(descriptions, info, template, args):
    """
    (MapReduce)
    Summary description of a character.
    :return: a string of description
    """
    template = template['summary']
    summary = {}
    for k, v in descriptions.items():
        role = k
        descriptions = v
        temp_info = {k: v for k, v in info.items() if isinstance(v, str)}
        temp_info['role'] = role
        temp_info['text'] = '\n'.join(descriptions)
        temp_template = build_prompt(template, temp_info)
        system = temp_template['system']
        prompt = temp_template['prompt']
        logger.info(f'Querying OpenAI {args.engine}, info: {temp_info}\n')
        summary[k] = process_request(system=system, prompt=prompt, args=args).strip()
    return summary


def extract_dialogue(text, info, template, args):
    """
    Extract dialogs of a character.
    :return: a list of dialogs
             [dialog1, dialog2, ...]
    """
    dialogues = []
    chapters = split_by_chapter(text, args.ie_novel)
    chapters = split_chapters_by_tokens(chapters, args.max_token)
    for chapter in chapters:
        temp_info = {k: v for k, v in info.items() if isinstance(v, str)}
        temp_info['text'] = chapter
        temp_template = build_prompt(template, temp_info)
        system = temp_template['system']
        prompt = temp_template['prompt']
        logger.info(f'Querying OpenAI {args.engine}, info: {temp_info}\n')
        dialogues.append(process_request(system=system, prompt=prompt, args=args).strip())
    return dialogues
