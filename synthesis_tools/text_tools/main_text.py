from .data_deal import date_time_deal
from .special_num import main as special_main


def text_normalize(get_text):
    get_txt = date_time_deal(text=get_text)
    get_txt = special_main(text=get_txt)
    # get_txt = get_txt.strip("。").strip("？").strip("，").strip(".").strip("?").strip(",")
    split_sentence = get_txt.split(',')
    inputs = []
    for x in split_sentence:
        inputs.append(x)
    total_len = sum([len(j) for j in split_sentence])
    return get_txt, inputs, total_len
