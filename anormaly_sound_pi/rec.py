#-*-coding:utf-8-*-

import argparse
import pyaudio
import wave
import time
from utils import DATA_PATH, DATA_AGE, data_rotate


# 引数定義およびパース
parser = argparse.ArgumentParser(description='record to wav format file')
parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
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
channels = 1

"""
初期値: サンプリング周波数(kHz)
"""
sampling_rate = 44100
"""
初期値: 一度に取得するデータ数
"""
chunk = 4096

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

# 配列frames データをwavファイルにして保存
wavefile = wave.open(wav_filename,'wb')
wavefile.setnchannels(channels)
wavefile.setsampwidth(audio.get_sample_size(format))
wavefile.setframerate(sampling_rate)

def callback(in_data, frame_count, time_info, status):
    # wavfile へ書き込み
    if debug:
        print(type(in_data))
    wavefile.writeframes(in_data)

    return (in_data, pyaudio.paContinue)

# 引数情報に従って、PyAudio ストリーム生成
stream = audio.open(
    format=format,
    rate = sampling_rate,
    channels = channels,
    input_device_index = dev_index,
    input = True,
    frames_per_buffer=chunk,
    stream_callback=callback)
if debug:
    print("recording")

stream.start_stream()

time.sleep(record_secs)
wavefile.close()
if debug:
    print(f'wait {record_secs} secs.')

print('stop_stream()')
stream.stop_stream()
print('close()')
stream.close()
print('terminate()')
audio.terminate()
if debug:
    print("stopped recording")
time.sleep(5)
wavefile.close()

if debug:
    print('wrote to {}'.format(wav_filename))