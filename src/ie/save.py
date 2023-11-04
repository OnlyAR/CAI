# @File Name:     save
# @Author :       Jun
# @date:          2023/11/3
# @Description :

import os


def save_to_text_file(text, filename, args):
    with open(os.path.join(args.out_path, filename), 'w', encoding='utf8') as f:
        f.write(text + "\n")
