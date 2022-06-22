#-*-coding:utf-8-*-
"""
音声データから音圧を算出する。
"""
import os
import wave
import datetime
import argparse
import numpy as np
#import matplotlib.pyplot as plt

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

parser = argparse.ArgumentParser(description='calculate sound pressure for a given wav file and write to csv file')
parser.add_argument('--input', type=str, help='target wav file path')
parser.add_argument('--output', type=str, default='sp_' + now.strftime("%Y%m%d%H%M%S") + '.csv', help='output csv filename')
parser.add_argument('--sampling_rate', type=int, default=44100, help='sampling rate(kHz)')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()


if not os.path.isfile(args.input):
    raise RuntimeError(f'input file:{args.input} not found')

if args.debug:
    print(f'read file:{args.input}')
wave_file = wave.open(args.input,'rb')
x = wave_file.readframes(wave_file.getnframes())
x = np.frombuffer(x, dtype='int16')

def to_db(x, N):
    """
    フレームデータから音圧を算出する。

    Parameters
    -----
    x:np.array  フレームデータ
    N:int       windowサイズ

    Returns
    -----
    dbs:np.array    音圧(dB単位)リスト
    """
    pad = np.zeros(N//2)
    pad_data = np.concatenate([pad, x, pad])
    rms = np.array([np.sqrt((1/N) * (np.sum(pad_data[i:i+N]))**2) for i in range(len(x))])
    return 20 * np.log10(rms)

# ウィンドウサイズ
N = 1024
db = to_db(x, N)
# サンプリングレート
sr = args.sampling_rate #44100
t = np.arange(0, db.shape[0]/sr, 1/sr)

if args.debug:
    print('show sound pressure graph(real data)')
    import matplotlib.pyplot as plt
    plt.plot(t, db, label='signal')
    plt.show()

def smoothing(input, window):
    """
    データをスムージングする。

    Parameters
    -----
    input       入力データ
    windows     ウィンドウサイズ

    Returns
    -----
    np.array    スムージング後のデータ
    """
    output = []
    for i in range(input.shape[0]):
        if i < window:
            output.append(np.mean(input[:i+window+1]))
        elif i > input.shape[0] - 1 - window:
            output.append(np.mean(input[i:]))
        else:
            output.append(np.mean(input[i-window:i+window+1]))
    return np.array(output)

smoothed_db = smoothing(db, 100)

if args.debug:
    print('show sound pressure graph(smoothed data)')
    import matplotlib.pyplot as plt
    plt.plot(t, smoothed_db, label='signal')
    plt.show()

v = np.vstack((t, smoothed_db)).transpose()
if args.debug:
    print(v)
np.savetxt(args.output, v, delimiter=',')
if args.debug:
    print(f'file:{args.output} saved')
