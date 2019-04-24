#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 时间格式和日期格式处理
import re


def date_time_deal(text):
    # year mon day deal example 2018-02-05
    mat_date_formal1 = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", text)
    for data in mat_date_formal1:
        formal_data = data.split("-")
        formal_data = "($" + str(formal_data[0]) + ")年" + str(int(formal_data[1])) + "月" + str(
            int(formal_data[2])) + "日"
        text = text.replace(data, formal_data)
    # year mon day deal example 2018/02/05
    mat_date_formal2 = re.findall(r"(\d{4}\/\d{1,2}\/\d{1,2})", text)
    for data in mat_date_formal2:
        formal_data = data.split("/")
        formal_data = "($" + str(formal_data[0]) + ")年" + str(int(formal_data[1])) + "月" + str(
            int(formal_data[2])) + "日"
        text = text.replace(data, formal_data)
    mat_date_formal3 = re.findall(r"(\d{4}\.\d{1,2}\.\d{1,2})", text)
    for data in mat_date_formal3:
        formal_data = data.split(".")
        # print(formal_data)
        formal_data = "($" + str(formal_data[0]) + ")年" + str(int(formal_data[1])) + "月" + str(
            int(formal_data[2])) + "日"
        text = text.replace(data, formal_data)
    # month days data deal
    mat_mon_formal1 = re.findall(r"(\d{1,2}-\d{1,2})", text)
    for data in mat_mon_formal1:
        formal_data = data.split("-")
        formal_data = str(int(formal_data[0])) + "月" + str(int(formal_data[1])) + "日"
        text = text.replace(data, formal_data)
    # year mon day deal example 2018/02/05
    mat_mon_formal2 = re.findall(r"(\d{1,2}/\d{1,2})", text)
    for data in mat_mon_formal2:
        formal_data = data.split("/")
        print(formal_data)
        formal_data = str(int(formal_data[0])) + "月" + str(int(formal_data[1])) + "日"
        text = text.replace(data, formal_data)
    # time formal deal formal 12:15
    mat_time_formal1 = re.findall(r"(\d{1,2}:\d{1,2})", text)
    for ti in mat_time_formal1:
        formal_ti = ti.split(":")
        formal_ti = str(int(formal_ti[0])) + "点" + str(int(formal_ti[1])) + "分"
        text = text.replace(ti, formal_ti)
    return text


if __name__ == "__main__":
    text = date_time_deal(text='他的生日是2016-12-12 14:34,是个可爱的小宝贝.二宝的生日是2016/12/21 11:34,好可爱的.2016.12.21, 12/21')
    print(text)
    # format = "([Jan|Feb|Mar]\s\d{1,2})"
    # re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", "birthday is Jan .")
    # p = re.compile(r'((Jan|Feb|Mar).\s\d{1,2})')
    # print(p.findall("birthday is Jan. 1"))
