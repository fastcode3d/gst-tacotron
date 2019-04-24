# wav_util.py

import os
import subprocess
import contextlib
import wave
from synthesis_tools.path_util import main_filename, get_path
from synthesis_tools.cmd_util import call_cmd
from pydub import AudioSegment


# noinspection PyPep8,PyBroadException
def get_stat(fn):
    try:
        cmd = 'sox %s -n stat -v' % fn
        s = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
        s = s.decode('utf-8')
        s = s.strip()
        v = float(s)
    except:
        print(fn, ' v=err')
        v = 'err'
    return v


def vol_gain(fn):
    mfn = main_filename(fn)
    v = get_stat(fn)
    if v != 'err':
        dst_fn = os.path.join(get_path(fn), mfn + '_vol.wav')
        call_cmd('sox -v %s %s %s' % (v, fn, dst_fn))
        return dst_fn
    else:
        return None


def trim_noise(fn, logger):
    try:
        logger.info('fn:' + fn)
        mfn = main_filename(fn)
        new_fn = os.path.join(get_path(fn), mfn + '_trim_noise.wav')
        cmd = 'sox -V3 %s %s silence 1 1 0.1%% 1 1 0.1%% : newfile : restart' % (fn, new_fn)
        logger.info('in trim_noise:' + cmd)
        call_cmd(cmd)
        logger.info('new_fn:' + new_fn)

        mfn = main_filename(new_fn)
        new_fn = os.path.join(get_path(fn), mfn + '001.wav')
        logger.info('new_fn 1:' + new_fn)
        return new_fn
    except Exception as e:
        raise e


def io_to_wav(wav_io, fn):
    with open(fn, 'wb') as fw:
        wav_bytes = wav_io.read()
        fw.write(wav_bytes)


def write_wave_vad(wav_path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(wav_path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


def AudioSegment_join(out, tmp_fn):
    result = AudioSegment.silent(duration=100)
    slience = AudioSegment.silent(duration=200)
    for wav in out:
        result += AudioSegment.from_file(wav, format='wav')
    result += slience
    result.export(tmp_fn, format='wav')


def trim_len(fn, length=None, char_len=None, logger=None):
    try:
        if char_len is not None:
            length = 0.3 * char_len

        logger.info('trim len fn:' + fn + ' len: ' + str(length))
        mfn = main_filename(fn)
        new_fn = os.path.join(get_path(fn), mfn + '_trim_len.wav')
        cmd = 'sox %s %s trim 0 %d' % (fn, new_fn, length)
        logger.info('in trim_len:' + cmd)
        call_cmd(cmd)
        logger.info('new_fn:' + new_fn)
        return new_fn
    except Exception as e:
        raise e
