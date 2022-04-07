# -*- coding: utf-8 -*-
# 実行方法　python3 this.py datafile

import os
import sys
import numpy as np
import pandas as pd
import keras.models
from keras.layers import Dense, BatchNormalization, Activation
from keras.models import Sequential
import scipy.io.wavfile as wav
from python_speech_features import logfbank
import argparse

'''
引数管理
'''
parser = argparse.ArgumentParser(description='train AutoEncoder with wav format file')
#parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
parser.add_argument('--train', type=str, default='test.wav', help='train data filename(wav format)')
parser.add_argument('--model', type=str, default='./ae_audio_model.h5', help='trained model filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
#parser.add_argument('--dev_index', type=int, default=1, help='USB mic index no')
args = parser.parse_args()
print(args)


# 入力データの項目数
INPUT_SIZE = args.input_size
ModelFile = args.model

# 学習用データの読み込み
Datafile = args.train

if not os.path.exists(Datafile):
    print("Datafile not exist.")
    exit()
(rate,sig) = wav.read(Datafile)

# 10secデータを1000レコードと16カラムに分割
train_data = logfbank(sig,rate,winlen=0.01,nfilt=INPUT_SIZE)

# AutoEncoderモデルの組み立て
model = Sequential()
model.add(Dense(INPUT_SIZE,input_shape=(INPUT_SIZE,)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(int(INPUT_SIZE/2)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(INPUT_SIZE))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(INPUT_SIZE))
model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# 学習：入力データと結果データを同一にする
history = model.fit(
    x=train_data, 
    y=train_data, 
    epochs=100, 
    batch_size=4, 
    validation_split=0.1)

# 学習済みモデルを保存
model.save(ModelFile)
print('Model saved.')
