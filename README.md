# anormaly_sound_pi

Raspberry Pi にUSBマイクを接続して、音声異常検知をおこなう。

## セットアップ

> Windows 環境で試行する場合は https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio よりwhlファイルを取得し、pip installする

```shell
sudo apt-get install build-essential python3 python3-dev python3-pip python3-virtualenv python3-numpy python3-pandas python3-pillow
sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 openmpi-bin libopenmpi-dev
cd ~/
python3 -m virtualenv -p python3 env --system-site-packages
echo "source ~/env/bin/activate" >> ~/.bashrc
source ~/.bashrc
pip install pip --upgrade
pip install pyaudio
pip install keras_applications==1.0.8 --no-deps
pip install keras_preprocessing==1.1.0 --no-deps
pip install numpy==1.22.1 -U
pip install h5py==3.6.0
pip install pybind11
pip install six wheel mock -U
mkdir ~/projects
cd ~/projects
wget "https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/main/tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh"
chmod +x tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh
./tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh
pip install tensorflow-2.8.0-cp39-none-linux_aarch64.whl
git clone https://github.com/coolerking/anormaly_sound_pi.git
cd anormaly_sound_pi
python detect_sound_index.py
```
