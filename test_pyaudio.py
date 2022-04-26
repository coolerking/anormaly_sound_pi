#-*-coding:utf-8-*-

import argparse
import pyaudio
import wave

parser = argparse.ArgumentParser(description='record to wav format file')
parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
parser.add_argument('--chunk', type=int, default=4096, help='data size')
parser.add_argument('--bit_depth', type=int, default=pyaudio.paInt16, help='data size')
parser.add_argument('--channels', type=int, default=1, help='channel mono:1 stereo:2')
parser.add_argument('--sampling_rate', type=int, default=44100, help='sampling rate(kHz)')
#parser.add_argument('--datadir', type=str, default=DATA_PATH, help='data directory path')
#parser.add_argument('--age', type=int, default=DATA_AGE, help='remained latest data file count')
parser.add_argument('--dev_index', type=int, default=1, help='USB mic index no')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

def  test_mic():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=args.bit_depth,
        rate = args.sampling_rate,
        channels = args.channels,
        input_device_index = args.dev_index,
        input = True,
        output = False,
        frames_per_buffer=args.chunk)

    wavefile = wave.open('wave_test.wav','wb')
    wavefile.setnchannels(args.channels)
    wavefile.setsampwidth(audio.get_sample_size(args.bit_depth))
    wavefile.setframerate(args.sampling_rate)

    stream.start_stream()
    for i in range(0, int((args.sampling_rate / args.chunk) * args.sec)):
        frames = []
        frames.append(stream.read(args.chunk))
        f = b''.join(frames)
        #print(f)
        print(i)
        wavefile.writeframes(f)
        #print(len(f))
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile.close()

if __name__ == '__main__':
    test_mic()
