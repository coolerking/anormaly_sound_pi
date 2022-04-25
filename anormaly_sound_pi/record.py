#-*-coding:utf-8-*-
"""
実行モジュール: USBマイクから取得した音声をwavファイル化して保存
"""
import argparse
import pyaudio
import wave
from utils import DATA_PATH, DATA_AGE, data_rotate

# 引数定義およびパース
parser = argparse.ArgumentParser(description='record to wav format file')
parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
parser.add_argument('--chunk', type=int, default=4096, help='data size')
parser.add_argument('--channels', type=int, default=1, help='channel')
parser.add_argument('--sampling_rate', type=int, default=44100, help='sampling rate(kHz)')
parser.add_argument('--datadir', type=str, default=DATA_PATH, help='data directory path')
parser.add_argument('--age', type=int, default=DATA_AGE, help='remained latest data file count')
parser.add_argument('--dev_index', type=int, default=1, help='USB mic index no')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

"""
初期値：デバッグオプション
"""
debug = args.debug

"""
初期値：ビット解像度(bit)
"""
format = pyaudio.paInt16

"""
初期値: チャネル
"""
channels = args.channels

"""
初期値: サンプリング周波数(kHz)
"""
sampling_rate = args.sampling_rate
"""
初期値: 一度に取得するデータ数
"""
chunk = args.chunk

"""
初期値: 録音秒数
"""
record_secs = args.sec

"""
初期値: USBデバイス番号
"""
dev_index = args.dev_index

"""
初期値: 出力ファイル名
"""
wav_filename = data_rotate(path=args.datadir, age=args.age)

# 引数表示
if debug:
    print(args)

# PyAudio インスタンス化
audio = pyaudio.PyAudio()

# 引数情報に従って、PyAudio ストリーム生成
stream = audio.open(
    format=format,
    rate = sampling_rate,
    channels = channels,
    input_device_index = dev_index,
    input = True,
    frames_per_buffer=chunk)
if debug:
    print("recording")
#frames = []

# 配列frames データをwavファイルにして保存
wavefile = wave.open(wav_filename,'wb')
wavefile.setnchannels(channels)
wavefile.setsampwidth(audio.get_sample_size(format))
wavefile.setframerate(sampling_rate)

# 指定秒数の音声をchunkサイズごとに取得し、配列framesへ追加
for _ in range(0, int((sampling_rate / chunk) * record_secs)):
    frames = []
    frames.append(stream.read(chunk))
    wavefile.writeframes(b''.join(frames))
if debug:
    print("finished recording")

# ストリームの停止およびクロース
stream.stop_stream()
stream.close()
# PyAudioインスタンスの停止
audio.terminate()

wavefile.close()
if debug:
    print('wrote to {}'.format(wav_filename))
