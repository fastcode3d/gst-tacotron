# -*- coding: utf-8 -*-
# common.py
from collections import OrderedDict as Odic
import datetime
import logging
import os
import platform
import re
import socket
import shutil
import subprocess
import traceback

cfgs_root = 'cfgs/'


# copy form pydub
def exec_exists(program):
    """
    Mimics behavior of UNIX which command.
    """
    # Add .exe program extension for windows support
    if os.name == "nt" and not program.endswith(".exe"):
        program += ".exe"

    envdir_list = [os.curdir] + os.environ["PATH"].split(os.pathsep)

    for envdir in envdir_list:
        program_path = os.path.join(envdir, program)
        if os.path.isfile(program_path) and os.access(program_path, os.X_OK):
            return program_path
    return None


def remove_path(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            return False
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            return False
    else:
        print("file {} is not a file or dir.".format(path))
    return True


def get_cfg_list_txt(this_sellbot_dir='.'):
    txt = this_sellbot_dir + '/cfgs/to_pub.txt'
    print('get_cfg_list_txt:', txt)
    with open(txt) as f:
        cfg_list = [l.strip() for l in f]
    return cfg_list


def get_cfg_list(this_sellbot_dir='.'):
    cfg_list = get_cfg_list_txt(this_sellbot_dir)

    # cfg_list = os.listdir(cfgs_root)
    # print('cfg_list0:', cfg_list)
    this_cfgs_root = this_sellbot_dir + '/' + cfgs_root
    cfg_list = [j for j in cfg_list if not j.endswith('_en') and j != 'templates' and os.path.isdir(this_cfgs_root + j)]
    # print('cfg_list:', cfg_list)
    return cfg_list


def export_sentences(sentence_outputs, id_lst, txt, id_txt=None):
    def isnum(_s):
        mo = re.match(r'^[-_\d]+$', _s)
        return mo is not None

    if txt is not None and id_txt is not None:
        id_lst_1 = []
        id_lst_2 = []
        for j in id_lst:
            if isnum(j):
                tt = (int(j.split('_')[0]), int(j.split('_')[1])) if '_' in j else (int(j), 0)  # '_' in j
                id_lst_1.append(tt)
            else:
                tt = (j, 0)
                id_lst_2.append(tt)
        # L1 = [(int(j.split('_')[0]), int(j.split('_')[1])) if '_' in j else (int(j), 0) for j in L]
        id_lst_1 = sorted(id_lst_1)
        id_lst_2 = sorted(id_lst_2)
        id_lst = id_lst_1
        id_lst.extend(id_lst_2)
        id_lst = [('%d_%d' % (j[0], j[1]) if j[1] != 0 else '%s' % str(j[0])) for j in id_lst]
    else:
        print('export_sentences, txt & id_txt both none!')

    if txt is not None:
        # print('txt:', txt)
        p = get_path(txt)
        mkdir_p(p)
        print('writing', txt)
        with open(txt, 'w') as f:
            for key in id_lst:
                f.write(str(key) + '<------------------->' + sentence_outputs[key] + '\n')
                # f.write(sentence_outputs[key] + '\n')

    if id_txt is not None:
        print('writing', id_txt)
        with open(id_txt, 'w') as f:
            for key in id_lst:
                f.write(str(key) + '\n')


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def remove_ext(fn):
    mfn, _ = os.path.splitext(fn)
    return mfn


def basename(fn):
    return os.path.basename(fn)


def get_ext(f):
    filename, file_extension = os.path.splitext(f)
    return file_extension


def main_filename(fn):
    return remove_ext(os.path.basename(fn))


def get_path(fn):
    p, fn = os.path.split(fn)
    return p


def grep(info, fn):
    r = []
    with open(fn) as f:
        for l in f:
            val = l.strip()
            if info in val:
                r.append(val)
    return r


def distrib_name():
    try:
        return platform.linux_distribution()[0].lower()
    except Exception as e:
        print(e)
        return "N/A"


def os_name():
    dn = distrib_name()
    if dn.startswith('centos'):
        return 'centos'
    elif 'ubuntu' in dn.lower():
        return 'ubuntu'
    else:
        return dn


def is_centos():
    return distrib_name().startswith('centos')


def call_cmd(s, verbose=False):
    if verbose:
        print('running:', s)
    r = os.system(s)
    # print('return val:', r, type(r), r == 0)
    return r == 0


def call_cmd_and_get_output(cmd):
    print('cmd str:', cmd)
    try:
        s = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT).decode('utf-8').strip()
    except Exception:
        print('run cmd error:', cmd)
        s = None
    return s


def call_cmd_and_get_output_not_work_till_now(s):
    print('cmd str:', s)
    # os.system(s)
    ss = s.split()
    cmd = ss[0]
    args = ' '.join(ss[1:])
    ss = [cmd, args]
    # proc = subprocess.Popen(ss, stdout=subprocess.PIPE)
    proc = subprocess.Popen(ss, stdout=subprocess.PIPE, shell=True)
    return proc.stdout.read().decode('utf-8')


def isdir(d):
    return os.path.isdir(d)


def isfile(d):
    return os.path.isfile(d)


def mkdir_p(d):
    if not isdir(d):
        os.makedirs(d)


""" 
日志分级说明：
critical(严重)  
严重错误，表明软件已不能继续运行了。 
error(错误) 
由于更严重的问题，软件已不能执行一些功能了。
warn(警告) 
表明发生了一些意外，或者不久的将来会发生问题（如‘磁盘满了’）。软件还是在正常工作。
info(信息) 
证明事情按预期工作。
debug(调试) 
详细信息，典型地调试问题时会感兴趣。
"""


def create_logger(name, loglevel=logging.INFO, fn=None):
    fmt = '%(asctime)s %(name)s %(levelname)s[%(filename)s:%(lineno)d] %(message)s'
    datefmt = None  # '%y-%m-%d %H:%M:%S'

    # set up logging to file
    '''logging.basicConfig(
        filename=fn,
        level=loglevel,
        format=fmt,
        datefmt=datefmt
    )'''

    logger = logging.getLogger(name)
    logger.handlers = []

    logger.setLevel(loglevel)

    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter(fmt, datefmt=datefmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if fn:
        print('new app_log file:', fn)
        fh = logging.FileHandler(fn, mode='w')
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def now(sep=True):
    fmt = "%Y-%m-%d %H:%M:%S" if sep else "%Y%m%d%H%M%S"
    return datetime.datetime.now().strftime(fmt=fmt)


def s2d(s, fmt="%Y-%m-%d %H:%M:%S"):
    t = datetime.datetime.strptime(s, fmt)
    return t


def parse_cfg_names(c_name, sellbot_dir='.'):
    if c_name is None:
        c_name = 'all'

    c_name = c_name.strip().lower()
    if c_name == '1':
        c_name = 'all'
    elif c_name == '0':
        c_name = 'none'

    if c_name == 'none':
        return []

    if c_name == 'all':
        r = get_cfg_list_txt(sellbot_dir)
    else:
        r = [c_name]
    return r


def d2od(d, to_be_sorted=True):
    if isinstance(d, dict):
        newd = Odic()
        data = sorted(d.items()) if to_be_sorted else d.items()

        for k, v in data:
            newd[k] = d2od(v, to_be_sorted=to_be_sorted)
        return newd
    else:
        return d


def uniq_lst(l):
    pl = []
    for j in l:
        if j not in pl:
            pl.append(j)
    return pl


def load_sim_dict(path, include_self=False):
    try:
        dic = {}
        with open(path, 'r', encoding='utf-8') as f:
            sim_data = f.readlines()
            for line in sim_data:
                line = line.strip()
                line = line.replace("：", ":")
                split_words = line.split(':')
                if len(split_words) == 2:
                    key = split_words[0]
                    if key != "":
                        sim_words = split_words[1].split(' ')
                        for sim_word in sim_words:
                            if sim_word is not '':
                                dic[sim_word] = split_words[0]
                        if include_self:
                            dic[split_words[0]] = split_words[0]
        return dic

    except Exception as e:
        print("load_sim_dict error: " + str(type(e).__name__) + ": " + str(e))
        traceback.print_exc()
        return {}
        # raise


def soft_link(src, dst):
    print('soft linking %s to %s' % (src, dst))
    os.symlink(src, dst)


def get_ip():
    s = None
    ip = 'unknown'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s is not None:
            try:
                s.close()
            except Exception as e:
                print('exception when close socket in get_ip: ' + str(e))
    return ip
