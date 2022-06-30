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

# セグメント長
N=1024

# scikit-learnのスペクトラム関数を使用
freqs, times, Sx = signal.spectrogram(
    y,                  # 測定値の時系列データ
    fs=framerate,       # サンプリング頻度←waveフレームレート
    window='hamming',   # 窓関数:ハミング窓を使用
    nperseg=N,          # セグメント長
    noverlap=N-100,     # セグメント間でオーバラップするサイズ
    detrend=False,      # トレンド除去しない
    scaling='spectrum') # スペクトログラム変数：V**2パワースペクトルを計算

# グラフ描画
f, ax = plt.subplots()
ax.pcolormesh(times, freqs/1000, 10* np.log10(Sx), cmap='viridis')
ax.set_ylabel('Frequency[kHz]')
ax.set_xlabel('Time[s]')

if not args.out:
    # GUI表示
    if args.debug:
        print('drawing graph image')
    plt.show()
else:
    # イメージをファイル出力
    plt.savefig(args.out)
    if args.debug:
        print(f'output graph image:{args.out}')