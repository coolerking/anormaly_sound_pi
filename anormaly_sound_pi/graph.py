# -*- coding: utf-8 -*-
"""
実行モジュール: 音声データをグラフ化する。
pip install librosa
python graph.py --path hogehoge.wav --debug True

FYI:
https://qiita.com/kotai2003/items/69638e18b6d542fb275e
"""

import os
import sys
import datetime
import sklearn
import librosa
import librosa.display
import librosa.feature
import argparse
import numpy as np
import matplotlib.pyplot as plt
'''
引数管理
'''
parser = argparse.ArgumentParser(description='output some graphs for sound wav file')
parser.add_argument('--path', type=str, default='test.wav', help='target wav file path')
parser.add_argument('--sr', type=int, default=44100, help='sampling rate')
parser.add_argument('--show', type=bool, default=False, help='show graph if true')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

"""
デバッグオプション
"""
debug = args.debug

"""
グラフ表示オプション
"""
show = args.show

"""
サンプリングレート
"""
sr = args.sr

"""
ターゲットファイルパス
"""
path = args.path
if path is None or not os.path.isfile(path):
    if debug:
        print(f'target wav path {str(path)} not exist, stop.')
    sys.exit(-1)

'''
wavファイルのロード
y: 音声信号の値 (audio time series) 振幅
sr: サンプリング周波数
''' 
y, sr = librosa.load(path)#, sr=sr)

if debug:
    print('Sampling rate (Hz): %d' % sr)
    print('Audio length (seconds): %.2f' % (len(y) / sr))
    tempo, _ = librosa.beat.beat_track(y, sr=sr)
    print('Tempo %.5f bpm' % tempo)
    '''
    Zero Crossing Rateは、音声の波形を描いたとき、
    波が中央より上(正)から中央より下(負)に、
    またはその逆に変化する頻度を数えて、
    その頻度により音声の特徴を表すというもの。
    ZCRが大きいほどより noisy な音声と捉えられるらしい。
    '''
    zero_crossings = librosa.zero_crossings(y, pad=False)
    print('Zero Crossing Rate(sum): %d' % sum(zero_crossings))
    if not show:
        outpath = path + '_meta.txt'
        with open(outpath, 'w') as f:
            f.write(f'target wav file path: {path}\n')
            f.write(f'date: {str(datetime.datetime.now())}\n')
            f.write('Sampling rate (Hz): %d\n' % sr)
            f.write('Audio length (seconds): %.2f\n' % (len(y) / sr))
            f.write('Tempo %.5f bpm\n' % tempo)
            f.write('Zero Crossing Rate(sum): %d\n' % sum(zero_crossings))

'''
X軸値となる時間配列を取得
'''
time = np.arange(0,len(y)) / sr

'''
print(time.shape)
plt.plot(time, y)
plt.xlabel('Time(s)')
plt.ylabel('Sound Amplitude')
'''

'''
振幅グラフ
'''
plt.figure(figsize=(16,6))
#librosa.display.waveshow(y, sr=sampling_rate)
librosa.display.waveshow(y=y, sr=sr)

if show:
    plt.show()
else:
    outpath = path + '_sound_amplitude.png'
    plt.savefig(outpath)
    if debug:
        print(f'save sound amplitude graph: {outpath}')

D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
print(D.shape)

plt.figure(figsize=(16, 6))
plt.plot(D)
plt.grid()

if show:
    plt.show()
else:
    outpath = path + '_sound_amplitude_logscaple.png'
    plt.savefig(outpath)
    if debug:
        print(f'save sound amplitude log scale graph: {outpath}')


DB = librosa.amplitude_to_db(D, ref=np.max)

plt.figure(figsize=(16, 6))
librosa.display.specshow(DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.colorbar()
#plt.show()

if show:
    plt.show()
else:
    outpath = path + '_spectgram.png'
    plt.savefig(outpath)
    if debug:
        print(f'save spectgram graph: {outpath}')

S = librosa.feature.melspectrogram(y, sr=sr)
S_DB = librosa.amplitude_to_db(S, ref=np.max)
plt.figure(figsize=(16, 6))
librosa.display.specshow(S_DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
plt.colorbar()
#plt.show()
if show:
    plt.show()
else:
    outpath = path + '_mel_spectgram.png'
    plt.savefig(outpath)
    if debug:
        print(f'save mel-spectgram graph: {outpath}')


spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]

# Computing the time variable for visualization
frames = range(len(spectral_centroids))

# Converts frame counts to time (seconds)
t = librosa.frames_to_time(frames)


def normalize(x, axis=0):
  return sklearn.preprocessing.minmax_scale(x, axis=axis)

plt.figure(figsize=(16, 6))
librosa.display.waveshow(y, sr=sr, alpha=0.5, color='b')
plt.plot(t, normalize(spectral_centroids), color='r')
if show:
    plt.show()
else:
    outpath = path + '_spectral_centroid.png'
    plt.savefig(outpath)
    if debug:
        print(f'save spectral centroid graph: {outpath}')

#Mel-Frequency Cepstral Coefficients (MFCCs)
mfccs = librosa.feature.mfcc(y, sr=sr)
mfccs = normalize(mfccs, axis=1)

print('mean: %.2f' % mfccs.mean())
print('var: %.2f' % mfccs.var())

plt.figure(figsize=(16, 6))
librosa.display.specshow(mfccs, sr=sr, x_axis='time')
if show:
    plt.show()
else:
    outpath = path + '_MFCCs.png'
    plt.savefig(outpath)
    if debug:
        print(f'save mel-frequency cepstral coefficients(MFCCs) graph: {outpath}')

sys.exit(0)