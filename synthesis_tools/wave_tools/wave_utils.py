import os
from synthesis_tools.wave_tools.tools import vol_gain, trim_noise
import traceback
from synthesis_tools.wave_tools.tools import write_wave_vad, io_to_wav
from synthesis_tools.wave_tools.vad_detect import vad_check_wav


# from audio import load_wav
# import io
def vad_check(out, tmp_fn):
    result = b''
    idx = 0
    for wav in out:
        # wav = io.BytesIO(load_wav(wav))
        write_segment_wav = False
        if write_segment_wav:
            tmp_fn_seg = tmp_fn.replace('.wav', '_%d_vad.wav' % idx)
            io_to_wav(wav, tmp_fn_seg)
            wav.seek(0)
        wav = vad_check_wav(wav_path_or_stream=wav)
        result += wav

        idx += 1
    write_wave_vad(wav_path=tmp_fn, audio=result, sample_rate=16000)


def handle_wav(wav_file_path, app_logger=None, use_trim_noise=False, vol=False, speed_wav=True):
    ret = ''
    try:
        app_logger.info('in handle_wav vol:' + str(vol))
        app_logger.info('in handle_wav use_trim_noise:' + str(use_trim_noise))
        if use_trim_noise:
            wav_file_path = trim_noise(wav_file_path, app_logger)
            app_logger.info('in handle_wav wav_file_path after trim_noise:' + str(wav_file_path))

        path8k = wav_file_path.replace(".wav", "_8k.wav")

        cmd = 'sox %s -r 16000 %s' % (wav_file_path, path8k)
        app_logger.info('in handle_wav running %s' % cmd)
        os.system(cmd)
        app_logger.info('in handle_wav path8k:' + str(path8k))

        ret = path8k
        if speed_wav:
            path_spd = path8k.replace(".wav", "_spd.wav")
            if os.path.isfile(path_spd):
                os.remove(path_spd)

            bin_path = 'soundstretch'
            cmd_speed = '%s %s %s -tempo=-4 > /dev/null 2>&1' % (bin_path, path8k, path_spd)
            os.system(cmd_speed)
            app_logger.info('in handle_wav path_spd:' + str(path_spd))

            if os.path.isfile(path_spd):
                ret = path_spd
            else:
                app_logger.info(str(path_spd) + ' not exists')
                ret = path8k
        else:
            ret = path8k

        if vol:
            new_ret = vol_gain(ret)
            app_logger.info('in handle_wav new_ret:' + str(new_ret))
            if new_ret is not None:
                ret = new_ret
    except Exception as e:
        app_logger.info('handle_wav fail, the error is %s' % e)
        traceback.print_exc()

    app_logger.info('in handle_wav last ret:' + str(ret))
    if os.path.isfile(ret):
        return ret
    else:
        return None


def concate_wav_by_fn(outwav_fn_list, outwav_fn, app_logger):
    from pydub import AudioSegment

    if len(outwav_fn_list) > 0:
        rst_wav = AudioSegment.from_wav(outwav_fn_list[0])
        for index in range(1, len(outwav_fn_list)):
            cur_wav = AudioSegment.from_wav(outwav_fn_list[index])
            rst_wav += cur_wav
        rst_wav.export(outwav_fn, format='wav')
    else:
        app_logger.info('concate_wav_by_fn have no input ')
    print("concate_wav_by_fn done")
