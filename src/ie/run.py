# @File Name:     run
# @Author :       Jun
# @date:          2023/10/25
# @Description :
import json
import os

import loguru

from ie.extractor import extract_description, extract_dialogue

logger = loguru.logger


def write_to_file(text, filename):
    with open(filename, 'w', encoding='utf8') as f:
        f.write(text + "\n")


def data_prepare(args):
    data_path = args.data_path
    novel_name = args.ie_novel

    if novel_name is None:
        raise ValueError('IE file is not specified, --ie_file is required.')
    with open(os.path.join(data_path, 'ie', novel_name, "content.txt"), 'r', encoding='utf8') as f:
        text = f.read()
    with open(os.path.join(data_path, 'ie', novel_name, "info.json"), 'r', encoding='utf8') as f:
        info = json.load(f)
    return text, info


def run(args):
    text, global_info = data_prepare(args)
    logger.info(f'Extracting information from {args.ie_novel}...')

    logger.info(f'Generating summary from {args.ie_novel}...')
    description = extract_description(text, global_info, args)

    write_to_file(json.dumps(description, ensure_ascii=False, indent=4),
                  os.path.join(args.out_path, args.task, args.exp_name, 'summary.txt'))
    logger.info(f'Extracting dialogue from {args.ie_novel}...')
    dialogues = extract_dialogue(text, global_info, args)
    write_to_file(json.dumps(dialogues, ensure_ascii=False, indent=4),
                  os.path.join(args.out_path, args.task, args.exp_name, 'dialogue.json'))
    logger.info(f'All done!')
