# -*- coding: utf-8 -*-
# 実行方法　python3 this.py datafile

import os
import sys
import numpy as np
import pandas as pd
import keras.models
import scipy.io.wavfile as wav
from python_speech_features import logfbank
from sklearn.metrics import mean_squared_error
import argparse

'''
引数管理
'''
parser = argparse.ArgumentParser(description='train AutoEncoder with wav format file')
#parser.add_argument('--sec', type=int, default=3, help='recording time(sec)')
parser.add_argument('--eval', type=str, default='eval.wav', help='eval data filename(wav format)')
parser.add_argument('--model', type=str, default='./ae_audio_model.h5', help='trained model filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
#parser.add_argument('--dev_index', type=int, default=1, help='USB mic index no')
args = parser.parse_args()
print(args)

# 入力データのカラム数
INPUT_SIZE = args.input_size

ModelFile = args.model

if not os.path.exists(ModelFile):
    print("Modelfile not exist.")
    exit()

Datafile = args.eval
if not os.path.exists(Datafile):
    print("Datafile not exist.")
    exit()

model = keras.models.load_model(ModelFile)

# 検出用データを読み込んで誤差を計算
(rate,sig) = wav.read(Datafile)
detect_data = logfbank(sig,rate,winlen=0.01,nfilt=INPUT_SIZE)

detect_pred = model.predict(detect_data)
detect_score = mean_squared_error(detect_data, detect_pred)
print('Score: ', detect_score)
