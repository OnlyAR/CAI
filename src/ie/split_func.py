# @File Name:     split_func
# @Author :       Jun
# @date:          2023/10/27
# @Description :
import os
import re


class Splitter:
    name = None

    def split(self, text):
        pass


class Yuni(Splitter):
    name = "与你"

    def split(self, text):
        # 章节号是形如 "\n一、\n" 的字符串
        num_zh = ['一', '二', '三', '四', '五', '六', '七', '八', '九', "十"]
        chapter_num = re.findall(r'[{}]、\n'.format(''.join(num_zh)), text)
        chapter_num = [text.find(chapter_num[i]) for i in range(len(chapter_num))]
        chapter_num.append(len(text))
        chapters = [text[chapter_num[i]:chapter_num[i + 1]] for i in range(len(chapter_num) - 1)]
        return chapters


class Zhihu1(Splitter):
    name = "知乎1"

    def split(self, text):
        # 章节号是形如 "\n12\n" 的字符串
        chapter_num = re.findall(r'\d+\n', text)
        chapter_num = [text.find(chapter_num[i]) for i in range(len(chapter_num))]
        chapter_num.append(len(text))
        chapters = [text[chapter_num[i]:chapter_num[i + 1]] for i in range(len(chapter_num) - 1)]
        return chapters
