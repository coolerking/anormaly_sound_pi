#-*-coding:utf-8-*-
"""
USBマイクを接続した状態で本コードを実行し index 番号を
確認する。
"""
try:
    import pyaudio
except:
    print('please install pyaudio package')

def main():
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        print(audio.get_device_info_by_index(i))

if __name__ == '__main__':
    main()
