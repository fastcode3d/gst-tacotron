# -*- coding: utf-8 -*-
import os
# reload(sys)
# sys.setdefaultencoding('utf-8')
from synthesis_tools.text_tools import atc
from pypinyin import lazy_pinyin, load_phrases_dict
import pypinyin
import json

from synthesis_tools.load_config import config_file

import pkuseg

seg = pkuseg.pkuseg(user_dict='user_dict/user_dict')

WORK_DIR = os.getcwd()
# if not WORK_DIR.endswith("/tacotron"):
#     WORK_DIR = config_file.get("work_dir")

# origin
# "."
PUNCTUATION = ['？', '！', '“', '”', '；', '：', '（', "）", ":", ";", ",", "?", "!", "\"", "\'", "(", ")"]
PUNCTUATION1 = r'，、。？！;,?!'  # 断句分隔符
PUNCTUATION2 = r'“”；·：~～（）×"\':()*#'  # 其它符号

alpha_pronuce = {
    "A": "eeei1 ", "B": "bi4 ", "C": "sei4 ", "D": "di4 ", "E": "iii4 ", "F": "ai2f ", "G": "ji4 ", "H": "ei2ch ",
    "I": "aaai4 ", "J": "jei4 ", "K": "kei4 ", "L": "ai2l ", "M": "ai2m ", "N": "eeen1 ",
    "O": "ooou1 ", "P": "pi4 ", "Q": "kiu4 ", "R": "aaa4 ", "S": "aaai2s ", "T": "ti4 ", "U": "iiiu1 ", "V": "uuui1 ",
    "W": "da2bliu1 ", "X": "ai2ks ", "Y": "uuuai4 ", "Z": "zei4 "}

TRANSFORM_DICT = {'ju': 'jv', 'qu': 'qv', 'xu': 'xv', 'zi': 'zic',
                  'ci': 'cic', 'si': 'sic', 'zhi': 'zhih',
                  'chi': 'chih', 'shi': 'shih', 'ri': 'rih',
                  'yuan': 'yvan', 'yue': 'yve', 'yun': 'yvn',
                  'quan': 'qvan', 'xuan': 'xvan', 'juan': 'jvan',
                  'qun': 'qvn', 'xun': 'xvn', 'jun': 'jvn',
                  'iu': 'iou', 'ui': 'uei', 'un': 'uen',
                  'ya': 'yia', 'ye': 'yie', 'yao': 'yiao',
                  'you': 'yiou', 'yan': 'yian', 'yin': 'yin',
                  'yang': 'yiang', 'ying': 'ying', 'yong': 'yiong',
                  'wa': 'wua', 'wo': 'wuo', 'wai': 'wuai',
                  'wei': 'wuei', 'wan': 'wuan', 'wen': 'wuen',
                  'weng': 'wueng', 'wang': 'wuang'}


def json_phone():
    with open("user_dict/phone_map.json", "r") as rf:
        data = json.load(rf)
    return data


def json_load():
    with open(os.path.join(WORK_DIR, "user_dict/fault-tolerant_word.json"), "r") as rf:
        data = json.load(rf)
    return data


usr_phrase = json_load()
load_phrases_dict(usr_phrase)


def text2pinyin(syllables):
    temp = []
    for syllable in syllables:
        for p in PUNCTUATION:
            syllable = syllable.replace(p, "")
        try:
            syllable = atc.num2chinese(syllable)
            new_sounds = lazy_pinyin(syllable, style=pypinyin.TONE3)
            for e in new_sounds:
                temp.append(e)
        except:
            syllable = syllable.replace(".", "")
            # syllable = atc.num2chinese(syllable)
            for p in PUNCTUATION:
                syllable = syllable.replace(p, "")
            temp.append(syllable)
    return temp


def pinyinformat(syllable):
    '''format pinyin to mtts's format'''
    if not syllable[-1].isdigit() and str(syllable[-1]) not in "&，。":
        syllable = syllable + '5'
    # assert syllable[-1].isdigit()
    syl_no_tone = syllable[:-1]
    if syl_no_tone in TRANSFORM_DICT:
        syllable = syllable.replace(syl_no_tone, TRANSFORM_DICT[syl_no_tone])
    return syllable


def ch_pin_list(speech):
    phon_dict = json_phone()
    # print('拼音转换: ', speech)
    syllables = lazy_pinyin(speech, style=pypinyin.TONE3, errors=lambda x: list(x))
    # print('---------1 ', speech, '----------')
    syllables = text2pinyin(syllables)
    text = ' '.join(syllables)
    # # 去掉&
    # for alpha, pronuce in alpha_pronuce.items():
    #     text = text.replace(alpha, pronuce.strip())
    # pinyin = text.split(" ")
    # 去掉& end
    for alpha, pronuce in alpha_pronuce.items():
        text = text.replace(alpha, " " + pronuce + "& ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    text = text.replace("& &", "&")
    pinyin = text.split(" ")
    pinyin = [pinyinformat(x) if x not in "，。！？。.,!?" else x for x in pinyin]
    pinyin_list = [phon_dict.get(char) if char in phon_dict.keys() else char for char in pinyin]
    return pinyin_list


def ch2p(speech):
    pinyin_list = ch_pin_list(speech)
    pinyin = " ".join(pinyin_list)
    return pinyin


def ch2ch(speech):
    pinyin_list = ch_pin_list(speech)
    new_speech = list(speech)
    if os.path.exists('pinyin_to_common.json'):
        pinyin_to_common_dict = json.load(open('pinyin_to_common.json', encoding='utf-8'))
        for ind, s in enumerate(speech):
            py = pypinyin.lazy_pinyin(s, style=pypinyin.TONE3, errors=lambda x: list(x))[0]
            if py in pinyin_to_common_dict:
                new_speech[ind] = pinyin_to_common_dict[py]
    text = ' '.join(new_speech)
    for p in PUNCTUATION:
        text = text.replace(p, "")
    # 去掉&
    # for alpha, pronuce in alpha_pronuce.items():
    #     text = text.replace(alpha, alpha.lower())
    # chars_list = text.split(" ")
    # 去掉& end
    for alpha, pronuce in alpha_pronuce.items():
        text = text.replace(alpha, " " + alpha.lower() + " & ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    text = text.replace("& &", "&")
    chars_list = text.split(" ")
    try:
        assert len(chars_list) == len(pinyin_list)
    except:
        print('维度不一致!!')
        print('chars_list', chars_list)
        print('pinyin_list', pinyin_list)
    for ind, char in enumerate(chars_list):
        rep_num = len(pinyin_list[ind])
        chars_list[ind] = char * rep_num
    return ' '.join(chars_list), ' '.join(pinyin_list)


def ch2word(speech):
    pinyin_list = ch_pin_list(speech)
    pinyin_list = ' '.join(pinyin_list).split(' ')
    new_speech = seg.cut(speech)
    text = ' '.join(new_speech)
    for p in PUNCTUATION:
        text = text.replace(p, "")
    new_speech = text.split(' ')
    word_list = list()
    count = 0
    for word in new_speech:
        pinyin = pinyin_list[count]
        if word == '':
            word_list.append('')
            count += 1
            continue
        for w in word:
            word_list.append('\t'.join(len(pinyin) * [word]))
            count += 1
    if count < len(pinyin_list):
        word_list.append(pinyin_list[count])
    try:
        assert len(word_list) == len(pinyin_list)
    except:
        print('维度不一致!!', len(word_list), len(pinyin_list))
        print('chars_list', word_list)
        print('pinyin_list', pinyin_list)
    return ' '.join(word_list), ' '.join(pinyin_list)


def num2han(value):
    txt = value
    num_han = {0: '零', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    value = ''.join(x for x in value if x in "0123456789")
    value = ''.join(num_han.get(int(x)) if x in value else x for x in txt)
    value = value[2:-1]
    return value


def num2phone(value):
    txt = value
    num_phone = {0: '零', 1: '幺', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    value = ''.join(x for x in value if x in "0123456789")
    value = ''.join(num_phone.get(int(x)) if x in value else x for x in txt)
    # value = ''.join(num_han.get(int(x)) for x in value)
    value = value[2:-1]
    return value


def num2specialnum(value):
    txt = value
    num_han = {0: '零', 1: '一', 2: '两', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    value = ''.join(x for x in value if x in "0123456789")
    value = ''.join(num_han.get(int(x)) if x in value else x for x in txt)
    value = value[2:-1]
    return value


def num2spec_1_2(value):
    txt = value
    num_han = {0: '零', 1: '幺', 2: '两', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}
    value = ''.join(x for x in value if x in "0123456789")
    value = ''.join(num_han.get(int(x)) if x in value else x for x in txt)
    value = value[2:-1]
    return value


if __name__ == "__main__":
    # print(num2han(value="($010194567898)"))
    # print(ch2p(num2phone("010194567898")))
    # print(atc.num2chinese("3418.91"))
    # print(num2han("($2418.91)"))
    # print(ch2p(seg.cut("12334.55元")))
    # print(ch2ch("&".join(seg.cut("看了你的来信，我能想象，"))))
    # print(ch2word('看了你的来信，我能想象，'))
    print(ch2word('请问您是新M三八F七七的车主汪家霖吗'))
