from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os

import pkuseg

from util import audio
from chinese2pinyin import ch2p, ch2ch, ch2word


def build_from_path(in_dir, out_dir, num_workers=1, mode='pinyin', tqdm=lambda x: x):
    '''Preprocesses the LJ Speech dataset from a given input path into a given output directory.

      Args:
        in_dir: The directory where you have downloaded the LJ Speech dataset
        out_dir: The directory to write the output into
        num_workers: Optional number of worker processes to parallelize across
        tqdm: You can optionally pass tqdm to get a nice progress bar

      Returns:
        A list of tuples describing the training examples. This should be written to train.txt
    '''

    # We use ProcessPoolExecutor to parallize across processes. This is just an optimization and you
    # can omit it and just call _process_utterance on each input if you want.
    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []
    index = 1
    seg = pkuseg.pkuseg(user_dict='user_dict/user_dict')
    with open(os.path.join(in_dir, 'wavs.txt'), encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            feat_path = os.path.join(in_dir, 'lpcf', '%s.f32' % parts[0])
            text = parts[1]
            # pinyin = ch2p("&".join(seg.cut(text)))
            if mode == 'text':
                text, pinyin = ch2ch("&".join(seg.cut(text)))
                # text, pinyin = ch2ch("".join(seg.cut(text)))
                print(text, "=>", pinyin)
                futures.append(executor.submit(partial(_process_utterance, out_dir, index, feat_path, pinyin, text)))
            elif mode == 'text_word':
                # text, pinyin = ch2ch("&".join(seg.cut(text)))
                text, pinyin = ch2word(text)
                print(text, "=>", pinyin)
                futures.append(executor.submit(partial(_process_utterance, out_dir, index, feat_path, pinyin, text)))
            else:
                pinyin = parts[2]
                print(text, "=>", pinyin)
                futures.append(executor.submit(partial(_process_utterance, out_dir, index, feat_path, pinyin, None)))
            index += 1
    return [future.result() for future in tqdm(futures)]


def reduce_dim(features):
    """ reduce dimension from 55d to 20d keep features[0:18] and features[36:38] only
    :param features: 55d
    return: 20d
    """
    N, D = features.shape
    assert D == 55, "Dimension error. %sx%s" % (N, D)
    features = np.concatenate((features[:, 0:18], features[:, 36:38]), axis=1)
    assert features.shape[1] == 20, "Dimension error. %s" % str(features.shape)
    return features.T


def _process_utterance(out_dir, index, feat_path, pinyin, text):
    '''Preprocesses a single utterance audio/text pair.

    This writes the mel and linear scale spectrograms to disk and returns a tuple to write
    to the train.txt file.

    Args:
      out_dir: The directory to write the spectrograms into
      index: The numeric index to use in the spectrogram filenames.
      feat_path: Path to the audio file containing the speech input
      text: The text spoken in the input audio file

    Returns:
      A (spectrogram_filename, mel_filename, n_frames, text) tuple to write to train.txt
    '''
    # Load features from file
    feat = np.fromfile(feat_path, dtype="float32")

    # Reduce dimension
    feat = np.resize(feat, (-1, 55))
    features = reduce_dim(feat)

    lpc_frames = features.shape[1]

    # Write features to disk
    lpc_feature_filename = 'lpc_feature-{}.npy'.format(index)
    np.save(os.path.join(out_dir, lpc_feature_filename), features.T, allow_pickle=False)

    return (text, lpc_feature_filename, None, lpc_frames, pinyin)
