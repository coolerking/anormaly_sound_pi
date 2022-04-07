#-*-coding:utf-8-*-
import argparse
import pyaudio
import wave

'''
引数管理
'''
parser = argparse.ArgumentParser(description='record to wav format file')
parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
parser.add_argument('--filename', type=str, default='test.wav', help='record filename')
parser.add_argument('--dev_index', type=int, default=17, help='USB mic index no')
args = parser.parse_args()
print(args)

'''
初期値
'''
form_1 = pyaudio.paInt16 #ビット解像度(bit)
chans = 1 # チャネル
samp_rate = 44100 # サンプリング周波数(kHz)
chunk = 4096 # 一度に取得するデータ数
record_secs = args.sec # 録音する秒数(sec)
dev_index = args.dev_index # デバイス番号
wav_output_filename = args.filename # 出力するファイル


audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(
    format=form_1,
    rate = samp_rate,
    channels = chans,
    input_device_index = dev_index,
    input = True,
    frames_per_buffer=chunk)
print("recording")
frames = []

# loop through stream and append audio chunks to frame array
for i in range(0,int((samp_rate/chunk)*record_secs)):
    data = stream.read(chunk)
    frames.append(data)

print("finished recording")

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

# save the audio frames as .wav file
wavefile = wave.open(wav_output_filename,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()