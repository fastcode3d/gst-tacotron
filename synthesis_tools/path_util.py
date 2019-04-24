# path_util.py
import os


def remove_ext(fn):
    mfn, _ = os.path.splitext(fn)
    return mfn


def main_filename(fn):
    return remove_ext(os.path.basename(fn))


def get_path(fn):
    p, fn = os.path.split(fn)
    return p
