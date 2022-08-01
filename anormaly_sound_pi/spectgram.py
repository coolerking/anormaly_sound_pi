# -*- coding: utf-8 -*-
"""
wavファイルからスペクトラムを生成するモジュール。

参考：
https://www.itd-blog.jp/entry/voice-recognition-10
"""
import os
import wave
import argparse
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from utils import show_spectgram, save_spectgram

# コマンドライン引数
parser = argparse.ArgumentParser(description='output spectgram from a wave file')
parser.add_argument('--wave', type=str, help='target wave filename(wav format)')
parser.add_argument('--out', type=str, help='output graph image filename(png format)')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

#waveファイルから必要な情報を読み込む
if not os.path.isfile(args.wave):
    raise RuntimeError(f'target filename:{args.wave} is not a file')

# waveファイルオープン
wavefile = wave.open(args.wave, 'r')
if args.debug:
    print(f'target filename:{args.wave}')

# waveファイルメタ情報入手
nframes = wavefile.getnframes() # フレーム総数を調べる
framerate = wavefile.getframerate() # フレームレート(サンプリング周波数)を調べる
if args.debug:
    print(f' total {nframes} frames')
    print(f' framerate:{framerate}')

# waveファイルから音声データを取得
y = wavefile.readframes(nframes) # フレームの読み込み
y = np.frombuffer(y, dtype='int16') # 波形を変換出来る様に変形する
t = np.arange(0, len(y))/float(framerate) # 音声データの長さ(x軸)
if args.debug:
    print(f' t-length:{len(t)} [{t[0]}, {t[-1]}]')

# waveファイルのクローズ
wavefile.close()

if not args.out:
    # GUI表示
    if args.debug:
        print('drawing graph image')
    show_spectgram(y, framerate)
else:
    # イメージをファイル出力
    save_spectgram(y, framerate, args.out)
    if args.debug:
        print(f'output graph image:{args.out}')