#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    并查集
    哈斯图
"""
from collections import Counter

import jieba
import jieba.posseg
from pyhanlp import *

tokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
stop_word_dict = JClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
# viterbi, dat, crf, perceptron, nshort
crf_seg = HanLP.newSegment('crf')


def read_novel_hanlp(file):
    all_part_speech_list = []
    role_list = []
    with open(file, encoding='UTF-8') as f:
        for line in f:
            # filter the empty line
            line = line.strip()
            line = line.replace(' ', '')
            if line:
                # ====== CRF ======
                line_part_speech_list = crf_seg.seg(line)
                # enable stopwords
                stop_word_dict.apply(line_part_speech_list)
                line_part_speech_list = [(str(j.word), str(j.nature)) for j in line_part_speech_list]
                # print(line_part_speech_list)

                # ====== NLP tokenizer ======
                # line_part_speech_list = tokenizer.analyze(line).translateLabels().__str__().split(' ')
                # # convert to tuple list
                # line_part_speech_list = [(j.split('/')[0], j.split('/')[1]) for j in line_part_speech_list]
                # print(line_part_speech_list)

                # filter the word whose length is less than 2
                line_part_speech_list = list(filter(lambda x: len(x[0]) > 1, line_part_speech_list))
                # extract the people's names
                role_list += list(filter(lambda x: x[1].startswith('nr') or x[1] == 'n', line_part_speech_list))
                all_part_speech_list += line_part_speech_list
        return all_part_speech_list, role_list


def read_novel_jieba(file):
    all_part_speech_list = []
    with open(file, encoding='UTF-8') as f:
        for line in f:
            # filter the empty line
            line = line.strip()
            if line:
                line_part_speech_list = jieba.posseg.lcut(line)
                # filter the word whose length is less than 2
                line_part_speech_list = list(filter(lambda x: len(x.word) > 1, line_part_speech_list))
                all_part_speech_list += line_part_speech_list
    return all_part_speech_list


if __name__ == '__main__':
    all_list, roles = read_novel_hanlp('惟我独仙.txt')
    # print(tokenizer.analyze('冥英王楞楞的道：“他，他真的放过了你。  ”'))
    # ll = read_novel_jieba('惟我独仙.txt')
    roles = Counter(roles)
    # filter some elements whose appearing times is less than or equal 10
    roles = {i: roles[i] for i in roles if roles[i] > 10}
    print(roles)
    # due to dict comprehension, dict has already been unordered, so order the dict again, which will output a list
    roles = sorted(roles.items(), key=lambda i: i[1], reverse=True)
    # regenerate the dict
    roles = {i[0]: i[1] for i in roles}
    print(roles)
