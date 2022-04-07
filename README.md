# anormaly_sound_pi

Raspberry Pi にUSBマイクを接続して、音声異常検知をおこなう。

## セットアップ

```shell
sudo apt-get install build-essential python3 python3-dev python3-pip python3-virtualenv python3-numpy python3-pandas python3-pillow
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
pip install pyaudio
cd ~/
python3 -m virtualenv -p python3 env --system-site-packages
echo "source ~/env/bin/activate" >> ~/.bashrc
source ~/.bashrc
mkdir ~/projects
cd ~/projects/
git clone https://github.com/coolerking/anormaly_sound_pi.git
cd anormaly_sound_pi
python detect_sound_index.py
```

