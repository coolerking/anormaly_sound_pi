# -*- coding: utf-8 -*-

# 例）毎時00分にデータを検出にかける
# crontab -e
# 0 * * * * python3 /folder/this.py data.wav

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
parser.add_argument('--threshold', type=float, default=1.0, help='score threshold float value')
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

args = args.eval
Datafile = args[1]
if not os.path.exists(Datafile):
    print("Datafile not exist.")
    exit()

model = keras.models.load_model(ModelFile)

# 検出用データを読み込んで誤差を計算
(rate,sig) = wav.read(Datafile)
detect_data = logfbank(sig,rate,winlen=0.01,nfilt=INPUT_SIZE)

detect_pred = model.predict(detect_data)
detect_score = mean_squared_error(detect_data, detect_pred)


##############################
# 検出結果が異常であればアクション
#import smtplib
#from email.mime.text import MIMEText

# 異常と判別するしきい値
BORDER = args.threshold

if detect_pred > BORDER:
    # MIMETextを作成
    message = "異常を検出しました。"
    print(message)
    #msg = MIMEText(message)
    #msg["Subject"] = "AI検出アラート"
    #msg["To"] = "送信先@aaa.com"
    #msg["From"] = "送信元@bbb.com"

    # サーバを指定する
    #server = smtplib.SMTP("smtp.bbb.com(社内SMTPサーバ)", 25(ポート番号))
    # メールを送信する
    #server.send_message(msg)
    # 閉じる
    #server.quit()
