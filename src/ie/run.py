# @File Name:     run
# @Author :       Jun
# @date:          2023/10/25
# @Description :
import json
import os

import loguru

from ie.extracter import (extract_description_mapreduce, summary_description_mapreduce,
                          extract_description_refine, extract_dialogue)

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
    with open("../config.json", "r", encoding="utf8") as f:
        template_name_dict = json.load(f)['ie_template']
    template_dict = {}
    for k, v in template_name_dict.items():
        with open(os.path.join('../template/ie', v + '.json'), 'r', encoding='utf8') as f:
            template_dict[k] = json.load(f)
    return text, info, template_dict


def run(args):
    text, global_info, template_dict = data_prepare(args)
    logger.info(f'Extracting information from {args.ie_novel}...')

    logger.info(f'Generating summary from {args.ie_novel}...')
    if args.summary == 'mapreduce':
        description_dict = extract_description_mapreduce(text, global_info, template_dict, args)
        description = summary_description_mapreduce(description_dict, global_info, template_dict, args)
        description = "\n".join([f'{k}: {v}' for k, v in description.items()])
    elif args.summary == 'refine':
        description = extract_description_refine(text, global_info, template_dict, args)
    else:
        raise ValueError(f'Unknown summary method {args.summary}.')

    write_to_file(description, os.path.join(args.out_path, args.task, args.exp_name, 'summary.txt'))
    logger.info(f'Extracting dialogue from {args.ie_novel}...')
    dialogues = extract_dialogue(text, global_info, template_dict['dialog'], args)
    write_to_file(json.dumps(dialogues, ensure_ascii=False, indent=4),
                  os.path.join(args.out_path, args.task, args.exp_name, 'dialogue.json'))
