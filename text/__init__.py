import re
from text import cleaners
from text.symbols import symbols

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id_pinyin = {s: i for i, s in enumerate(symbols)}
_id_to_symbol_pinyin = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')


# _pad = '[PAD]'
# _eos = '[SEP]'
# _unk = '[UNK]'


# 加载bert字典
def vocab_parse(path):
    """
    从path加载voc
    :param path:
    :return:
    """
    symbol_to_id = dict()
    id_to_symbol = dict()
    count = 0
    for line in open(path):
        line = line.strip().replace('\n', '')
        if line == '':
            continue
        symbol_to_id[line] = count
        id_to_symbol[count] = line
        count += 1
    return symbol_to_id, id_to_symbol


_symbol_to_id_text, _id_to_symbol_text = vocab_parse('voc_bert.txt')


def text_to_sequence(text, cleaner_names, mode='pinyin', separator=''):
    '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

      The text can optionally have ARPAbet sequences enclosed in curly braces embedded
      in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

      Args:
        text: string to convert to a sequence
        cleaner_names: names of the cleaner functions to run the text through
        mode:

      Returns:
        List of integers corresponding to the symbols in the text
    '''
    sequence = []

    # Check for curly braces and treat their contents as ARPAbet:
    while len(text):
        m = _curly_re.match(text)
        if not m:
            sequence += _symbols_to_sequence(_clean_text(text, cleaner_names), mode, separator)
            break
        sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names), mode, separator)
        sequence += _arpabet_to_sequence(m.group(2), mode)
        text = m.group(3)

    # Append EOS token
    if mode == 'text':
        sequence.append(_symbol_to_id_text['[SEP]'])
    else:
        sequence.append(_symbol_to_id_pinyin['~'])
    return sequence


def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = ''
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol_pinyin:
            s = _id_to_symbol_pinyin[symbol_id]
            # Enclose ARPAbet back in curly braces:
            if len(s) > 1 and s[0] == '@':
                s = '{%s}' % s[1:]
            result += s
    return result.replace('}{', ' ')


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbols, mode='', separator=''):
    return _get_symbols(symbols, mode, separator)


def _arpabet_to_sequence(text, mode=''):
    return _symbols_to_sequence(['@' + s for s in text.split()], mode)



def _get_symbols(symbols, mode, separator=''):
    symbols = list(symbols) if separator == '' else symbols.split(separator)

    symbol_to_id = _symbol_to_id_text if mode == 'text' else _symbol_to_id_pinyin
    res_list = list()
    for s in symbols:
        s = '[PAD]' if mode == 'text' and s == ' ' else s
        if s == '_' or s == '~':
            continue
        if s not in symbol_to_id:
            print('{}模式下的{}字符不存在'.format(mode, s))
            s = '[UNK]'
        res_list.append(symbol_to_id[s])
    return res_list
