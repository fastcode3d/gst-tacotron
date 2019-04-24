import re
from synthesis_tools.text_tools.atc import num2chinese


def num_2char(line):
    re_find = re.findall(r"\d+\.?\d*", line)
    print(re_find)
    for num in re_find:
        start = line.index(num)
        end = start + len(num)
        num_after = num2chinese(num=num)
        line = line[:start] + num_after + line[end:]
    return line


if __name__ == "__main__":
    per = num_2char(line="期后您本月在最后还款日10月11日前仅需还款411.7元")
    print(per)
