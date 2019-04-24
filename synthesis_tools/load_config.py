#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os

WORK_DIR = os.getcwd()
# print(WORK_DIR)
# if not WORK_DIR.endswith("/tacotron"):
#     WORK_DIR = "/root/GJTTS"


def load_json(config_path=os.path.join(WORK_DIR, "config/config.json")):
    with open(config_path, encoding="utf-8") as f:
        config_file = json.load(f)
    return config_file


config_file = load_json()
# print(config_file.get("gpu_frac"))
