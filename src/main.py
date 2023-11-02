# @File Name:     main
# @Author :       Jun
# @date:          2023/10/25
# @Description :
import argparse
import os

import loguru
import langchain
from langchain.cache import SQLiteCache

import ie

logger = loguru.logger


def parse_argument():
    parser = argparse.ArgumentParser()
    # general args
    parser.add_argument('--exp_name', type=str, default=None)
    parser.add_argument('--task', type=str, default='ie')
    parser.add_argument('--debug', action='store_true', default=False)

    # api args
    parser.add_argument('--engine', type=str, default='gpt-3.5-turbo')

    # data paths
    parser.add_argument('--data_path', type=str, default='../data')
    parser.add_argument('--out_path', type=str, default='../out')
    parser.add_argument('--cache_path', type=str, default='../cache')
    parser.add_argument('--log_path', type=str, default='../log')
    parser.add_argument('--max_token', type=int, default=2048)

    # ie args
    parser.add_argument('--ie_novel', type=str, default=None)
    parser.add_argument('--summary', type=str, default='mapreduce')
    return parser.parse_args()


def make_dirs(args):
    task_name = args.task
    exp_name = args.exp_name
    log_path = os.path.join(args.log_path, task_name)
    cache_path = os.path.join(args.cache_path)
    out_path = os.path.join(args.out_path, task_name, exp_name)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    if not os.path.exists(out_path):
        os.makedirs(out_path)


def set_logger(args):
    log_path = os.path.join(args.log_path, args.task, "{}.log".format(args.exp_name))
    loguru.logger.add(log_path)


def main():
    args = parse_argument()

    if args.exp_name is None:
        raise ValueError('Experiment name is not specified, --exp_name is required.')

    make_dirs(args)
    set_logger(args)
    langchain.llm_cache = SQLiteCache(database_path=os.path.join(args.cache_path, "langchain.db"))

    if args.task == 'ie':
        ie.run(args)
    else:
        raise ValueError('Task name is not correct.')


if __name__ == "__main__":
    main()
