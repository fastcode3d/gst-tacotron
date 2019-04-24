# cmd_util.py

import os


def call_cmd(s, verbose=False):
    if verbose:
        print('running:', s)
    r = os.system(s)
    # print('return val:', r, type(r), r == 0)
    return r == 0
