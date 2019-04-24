import re
from synthesis_tools.text_tools.chinese2pinyin import num2phone, num2han, num2specialnum, num2spec_1_2


def get_num_exclamation(text=None):
    """
    :param text: 里面含有($***)
    :return: 处理掉($***), 按位读取，一二三四五六七八九十
    """
    khcon_reg = re.compile(r'\((\$.*?)\)')
    text = re.sub(khcon_reg, lambda x: num2han(x.group(0)), text)
    return text


def get_num_phone(text=None):
    """
    :param text: 里面含有(#***)
    :return: 处理掉(#***) 一读幺
    """
    khcon_reg = re.compile(r'\((#.*?)\)')
    text = re.sub(khcon_reg, lambda x: num2phone(x.group(0)), text)
    return text


def get_num_2_two(text=None):
    """
    :param text: 里面含有(@***)
    :return: 处理掉(@***) 二读两
    """
    khcon_reg = re.compile(r'\((@.*?)\)')
    text = re.sub(khcon_reg, lambda x: num2specialnum(x.group(0)), text)
    return text


def get_num_1_yao_2_two(text=None):
    """
    :param text: 里面含有(!***)
    :return: 处理掉(!***) 一读幺, 二读两
    """
    khcon_reg = re.compile(r'\((!.*?)\)')
    text = re.sub(khcon_reg, lambda x: num2spec_1_2(x.group(0)), text)
    return text


def main(text):
    # 处理($ )
    text = get_num_exclamation(text)
    # 处理(# )
    text = get_num_phone(text)
    # 处理($ )
    text = get_num_2_two(text)
    # 处理(! )
    text = get_num_1_yao_2_two(text=text)
    # print(text)
    return text


if __name__ == "__main__":
    test = main(text="成立于($2017)年8月8日")
    print(test)
