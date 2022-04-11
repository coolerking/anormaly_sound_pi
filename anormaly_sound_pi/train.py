# -*- coding: utf-8 -*-
"""
実行モジュール: 音声異常検知モデルを学習する。
実行例: python train.py --train data\train.wav --model model\model.h5 --input_size 20
"""
import os
from keras.layers import Dense, BatchNormalization, Activation
from keras.models import Sequential
import scipy.io.wavfile as wav
from python_speech_features import logfbank
import argparse

# 引数管理
parser = argparse.ArgumentParser(description='train AutoEncoder with wav format file')
parser.add_argument('--train', type=str, default='train.wav', help='train data filename(wav format)')
parser.add_argument('--model', type=str, default='./ae_audio_model.h5', help='trained model filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
args = parser.parse_args()
print(args)


"""
入力データの項目数
"""
input_size = args.input_size

"""
モデルファイルパス
"""
model_path = args.model

"""
トレーニングデータファイルパス(wavファイル)
"""
data_path = args.train

# トレーニングデータ読み込み
if not os.path.exists(data_path):
    print(f'Datafile {data_path} not exist.')
    exit()
(rate,sig) = wav.read(data_path)

# 10secデータを1000レコードと16カラムに分割
train_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)

# AutoEncoderモデルの組み立て
model = Sequential()
model.add(Dense(input_size,input_shape=(input_size,)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(int(input_size/2)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(input_size))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(input_size))
model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# 学習：入力データと結果データを同一にする
history = model.fit(
    x=train_data, # 学習データ(入力) 
    y=train_data, # 学習データ(出力)、入力と同じ
    epochs=100, 
    batch_size=4, 
    validation_split=0.1)

# 学習済みモデルを保存
model.save(model_path)
print(f'Saved model file {model_path}')
