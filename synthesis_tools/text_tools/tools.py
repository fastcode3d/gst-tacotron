# noinspection PyMethodMayBeStatic
def judge_sentence_len(txt, PUNCTUATION1=[]):
    for ch in PUNCTUATION1:
        txt = str(txt)
        txt = txt.replace(ch, ',')
    txt = txt.split(',')
    sentence_len = []
    for line in txt:
        sentence_len.append([line, len(line)])
    sentence_len = sorted(sentence_len, key=lambda i: -i[1])
    sentence, _ = zip(*sentence_len)
    max_len = len(sentence[0])
    return sentence, max_len
