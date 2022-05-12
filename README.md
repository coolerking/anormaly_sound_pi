# Sound Anormaly Detection with Raspberry Pi

Raspberry Pi にUSBマイクを接続して、電動バギーが接近していることを検知する。

[![Sound Anormaly Detection](http://img.youtube.com/vi/C-q4WTERQNY/0.jpg)](https://www.youtube.com/watch?v=C-q4WTERQNY)

## 前提

### 音声検知側

- Raspberry Pi4 8GBmem / ACアダプタ
- Raspberry Pi OS bullseye 2022/04/04版
- swap設定 2GB
- SunFounder 超小型 USBミニマイク (もしくは、Sound Blaster V3 & ピンマイク)

### 音声発生源側

- タミヤ楽しい工作シリーズ No.112 電動バギー (ローギア)

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
pip install python_speech_features
pip install six wheel mock -U
pip install sklearn

pip install flask
mkdir ~/projects
cd ~/projects
wget "https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/main/tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh"
chmod +x tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh
./tensorflow-2.8.0-cp39-none-linux_aarch64_numpy1221_download.sh
pip install tensorflow-2.8.0-cp39-none-linux_aarch64.whl
git clone https://github.com/coolerking/anormaly_sound_pi.git
cd anormaly_sound_pi
git checkout main
```

## マイクUSBデバイス番号確認

マイクデバイスをRaspberry Pi USBコネクタに接続し、以下のコマンドを実行する。

```bash
cd ~/projects/anormaly_sound_pi/anormaly_sound_pi
python detect.py
```

Raspberry Pi(USB) にSoundBlasterを接続、マイクコネクタにピンマイクを差した状態での実行結果の一部は以下の通り。

```json
{'index': 0, 'structVersion': 2, 'name': 'bcm2835 Headphones: - (hw:0,0)', 'hostApi': 0, 'maxInputChannels': 0, 'maxOutputChannels': 8, 'defaultLowInputLatency': -1.0, 'defaultLowOutputLatency': 0.0016099773242630386, 'defaultHighInputLatency': -1.0, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
{'index': 1, 'structVersion': 2, 'name': 'Sound Blaster Play! 3: USB Audio (hw:1,0)', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 2, 'defaultLowInputLatency': 0.008684807256235827, 'defaultLowOutputLatency': 0.008684807256235827, 'defaultHighInputLatency': 0.034829931972789115, 'defaultHighOutputLatency': 0.034829931972789115, 'defaultSampleRate': 44100.0}
:
```

上記の例の場合、Sound Blasterのデバイスインデックスは `1` であることがわかる。

## 学習データ(wavファイル)の収集

**正常** な音声を録音して、学習データとして使用する。
Raspberry Pi に接続したマイクを対象に向ける。
デバイスインデックスが`1`の場合、以下のように実行する。

```bash
cd ~/projects/anormaly_sound_pi/anormaly_sound_pi
mkdir data
python record.py --sec 10 --datadir data --dev_index 1 --debug True --age 5
```

上記の例では、10秒間収集した音声データファイル(wav形式)をdataディレクトリに保存する。
data ディレクトリには最新5世代の音声ファイルを残し、他のデータは削除する。

## トレーニング処理実行

学習データを `data/mic_yyyymmdd_hhmmss.wav` とした場合、以下のように実行する。

```bash
mkdir models
python train.py --train data/mic_yyyymmdd_hhmmss.wav --model models/anormaly.h5
```

上記の場合、学習済みモデルファイル `models/anormaly.h5` が作成される。

## 音声ファイルの評価

学習済みモデルファイル `models/anormaly.h5` 、評価対象の音声ファイルが `data/mic_yyyymmdd_hhmmss.wav` である場合、次のように実行する。

```bash
python eval.py --eval data/mic_yyyymmdd_hhmmss.wav --model models/anormaly.h5 --debug True
```

以下、実行例。

```bash
Namespace(eval='eval.wav', model='anomaly.h5', input_size=20)
/home/pi/projects/anormaly_sound_pi/anormaly_sound_pi/eval.py:43: WavFileWarning: Chunk (non-data) not understood, skipping it.
  (rate,sig) = wav.read(Datafile)
Score:  1.2546335234695254
```

正常な音声と異常時の音声を複数何度か繰り返し、正常と異常を切り分けるスコア値をみつける。

また、以下のように `--eval` のかわりに `--datadir` を指定した場合、指定ディレクトリ内の最新ファイルを対象とする。

```bash
python eval.py --datadir data --model models/anormaly.h5 --debug True
```

## 異常検知スコアグラフ表示

以下を実行する。

```bash
cd ${HOME}/projects/anormaly_sound_pi/anormaly_sound_pi
chmod +x record.sh
crontab -e
```

crontabを以下のように編集する。

```shell
0-59 * * * * /home/pi/projects/anormaly_sound_pi/anormaly_sound_pi/record.sh
```

> もっとはやく検知情報をグラフへ反映させたい場合は、
>
> ```shell
> watch -n 2 /home/pi/projects/anormaly_sound_pi/anormaly_sound_pi/record.sh 1> /dev/null 2>&1
> ```
>
> などで実行させる（上記記述ではバックグラウンド実行とはならない）。

data ディレクトリに履歴が溜まってきたら、以下のコマンドを実行する。

```bash
python server.py --host XXX.XXX.XXX.XXX --port 5000 --model models/anormaly.h5 --datadir data --debug True
```

実行後、`http://XXX.XXX.XXX.XXX:5000/` をブラウザで開くとグラフで確認できる。

## ライセンス

[MITライセンス](./LICENSE) 準拠とする。
