import uuid
import os


def gen_tmp_fn(app_logger, workdir):
    uuid_str = str(uuid.uuid1()).replace('-', '')
    tmp_fn = os.path.join(workdir, 'tmp/%s.wav' % uuid_str)
    tmp_path = os.path.dirname(tmp_fn)
    app_logger.info('tmp_path: ' + str(tmp_path))
    app_logger.info('tmp_fn: ' + str(tmp_fn))
    return tmp_fn, uuid_str
