from synthesis_tools.wave_tools.tools import AudioSegment_join
from synthesis_tools.wave_tools.wave_utils import handle_wav
from synthesis_tools.util import gen_tmp_fn
from synthesis_tools.wave_tools.wave_utils import vad_check


def wave_main(out, total_len, app_logger, workdir, use_vad_noise_trim, vol, use_trim_noise, speed_wav):
    tmp_fn, uuid_str = gen_tmp_fn(app_logger=app_logger, workdir=workdir)
    if use_vad_noise_trim:
        try:
            vad_check(out, tmp_fn)
        except Exception as e:
            print("error:", e)
            AudioSegment_join(out, tmp_fn)
    else:
        AudioSegment_join(out, tmp_fn)
    app_logger.info('self.vol: ' + str(vol))
    app_logger.info('total_len: ' + str(total_len))
    new_fn = handle_wav(tmp_fn, app_logger=app_logger, use_trim_noise=use_trim_noise,
                        vol=vol, speed_wav=speed_wav)
    app_logger.info('new_fn after handle_wav: ' + str(new_fn))
    return new_fn, uuid_str
