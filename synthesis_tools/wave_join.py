#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from pydub import AudioSegment

# https://github.com/jiaaro/pydub/


"""
pip install pydub
安装 libav or ffmpeg 依赖:

Mac (using homebrew):

# libav
brew install libav --with-libvorbis --with-sdl --with-theora

####    OR    #####

# ffmpeg
brew install ffmpeg --with-libvorbis --with-ffplay --with-theora
Linux (using aptitude):

# libav
apt-get install libav-tools libavcodec-extra-53

####    OR    #####

# ffmpeg
apt-get install ffmpeg libavcodec-extra-53

Windows:

Download and extract libav from Windows binaries provided here.
Add the libav /bin folder to your PATH envvar
pip install pydub
"""


class AudioJoiner:
    def __init__(self):
        self.fileList = list()

    # 将文件加到表里
    def join_singlefile(self, audioFile):
        self.fileList.append(audioFile)

    # 将文件表加到表里
    def join_list(self, filelist):
        self.fileList.extend(filelist)

    # 加载声音文件
    def load_songfile(self, songPath, frame_rate=16000, channels=1):
        # song = None
        if os.path.exists(songPath):
            song = AudioSegment.from_file(songPath)
            if not song:
                print("audio format is no support.")
            else:
                song.set_channels(channels)
                song.set_frame_rate(frame_rate)
        else:
            return None
        return song

    # 合并两个音频文件,adjectDb是否平衡音量
    def combine_two_song_file(self, songPath1, songPath2, frame_rate=16000, channels=1, adjectDb=False):
        song1 = self.load_songfile(songPath1, frame_rate, channels)
        song2 = self.load_songfile(songPath2, frame_rate, channels)
        if not song1 or not song2:
            return None
        if adjectDb:
            # 取得两个MP3文件的声音分贝
            db1 = song1.dBFS
            db2 = song2.dBFS
            # 调整两个MP3的声音大小，防止出现一个声音大一个声音小的情况
            dbplus = db1 - db2
            if dbplus < 0:  # song1的声音更小
                song1 += abs(dbplus)
            elif dbplus > 0:  # song2的声音更小
                song2 += abs(dbplus)
                # 拼接两个音频文件
        song = song1 + song2
        return song

    # 合并两个音频流, adjectDb是否平衡音量
    def combine_two_song(self, song1, song2, adjectDb=False):
        if not song1 or not song2:
            return None
        if adjectDb:
            # 取得两个MP3文件的声音分贝
            db1 = song1.dBFS
            db2 = song2.dBFS
            # 调整两个MP3的声音大小，防止出现一个声音大一个声音小的情况
            dbplus = db1 - db2
            if dbplus < 0:  # song1的声音更小
                song1 += abs(dbplus)
            elif dbplus > 0:  # song2的声音更小
                song2 += abs(dbplus)
        # 拼接两个音频文件
        song = song1 + song2
        return song

    # 导出合并后的音频文件
    def export_audio_file(self, targetPath="output.wav", audio_format="wav",
                          bitrate="256k", frame_rate=16000, channels=1):

        filenum = len(self.fileList)
        if filenum <= 0:
            return False

        if filenum == 1:
            outputsong = self.load_songfile(self.fileList[0], frame_rate, channels)
        else:
            outputsong = self.load_songfile(self.fileList[0], frame_rate, channels)
            for i in range(filenum - 1):
                tempsong = self.load_songfile(self.fileList[i + 1], frame_rate, channels)
                outputsong = self.combine_two_song(outputsong, tempsong)

        # 导出音频文件
        if outputsong:
            outputsong.export(targetPath, format=audio_format, bitrate=bitrate)
            if os.path.exists(targetPath):
                return True
            else:
                return False
        return False

    # 清除文件列表
    def clear_list(self):
        self.fileList.clear()


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
        if os.path.exists(program_path) and os.access(program_path, os.X_OK):
            return program_path
    return None


def wave_join(wave_folds, outfile="/media/btows/SDB/working/project/join_tts/62.wav"):
    """
    :param tts_fold: 表示合成的TTS所在的文件夹
    :param sent_id: 所有TTS 合成变量的变量名
    :param replace_sent: 进行拼接的句子
    :param json_path: replace json 所在的路径和音频所在的路径，注意 将replace.json 放在这个文件夹里面
    :param outfile: 音频保存路径
    :return:
    """
    if not exec_exists("ffmpeg"):
        print("Could not find ffmpeg.")
        return
    audio_joiner = AudioJoiner()
    audio_joiner.clear_list()
    filelist = list()
    for wav in wave_folds:
        if os.path.exists(wav):
            filelist.append(wav)
        else:
            print("%s not exist" % wav)

    audio_joiner.join_list(filelist)
    # print("pass")
    if audio_joiner.export_audio_file(outfile, "wav"):
        print("合并成功")
        # os.system("ffplay %s"%outfile)


if __name__ == "__main__":
    wave_join()
