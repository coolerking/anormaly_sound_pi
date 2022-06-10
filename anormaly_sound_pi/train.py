# -*- coding: utf-8 -*-
"""
実行モジュール: 音声異常検知モデルを学習する。
実行例: python train.py --train data\train.wav --model model\model.h5 --input_size 20
"""
import os
import sys
import time
from keras.layers import Dense, BatchNormalization, Activation
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, TensorBoard
import scipy.io.wavfile as wav
from python_speech_features import logfbank
import argparse
from utils import get_log_path

# 引数管理
parser = argparse.ArgumentParser(description='train AutoEncoder with wav format file')
parser.add_argument('--train', type=str, default='train.wav', help='train data filename(wav format)')
parser.add_argument('--base', type=str, help='base trained model filename(option)')
parser.add_argument('--model', type=str, default='./ae_audio_model.h5', help='trained model filename')
parser.add_argument('--ignore_rows', type=int, default=10, help='ignore data rows')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
parser.add_argument('--epochs', type=int, default=2000, help='epochs')
parser.add_argument('--early_stopping', type=bool, default=False, help='use early stopping')
parser.add_argument('--tensor_board', type=bool, default=False, help='use TensorBoard')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

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

"""
先頭削除対象行数
"""
ignore_rows = args.ignore_rows

"""
デバッグフラグ
"""
debug = args.debug

"""
epochs
"""
epochs = args.epochs

"""
early stopping
"""
early_stopping = args.early_stopping

"""
Tensor Board
"""
tensor_board = args.tensor_board

if debug:
    print(args)

# トレーニングデータ読み込み
if not os.path.exists(data_path):
    if debug:
        print(f'Datafile {data_path} not exist.')
    exit()
(rate,sig) = wav.read(data_path)

# 10secデータを1000レコードと16カラムに分割
train_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)
if debug:
    print(f'train data original shape: {train_data.shape}')
# 先頭行削除
train_data = train_data[ignore_rows:]
if debug:
    print(f'train data reshaped: {train_data.shape}')

#
if args.base:
    if not os.path.isfile(args.base):
        if debug:
            print(f'base model {args.base} not exist, stop.')
        sys.exit(-1)
    if debug:
        print(f'loading base model: {args.base}')
    model = load_model(args.base)
else:
    # AutoEncoderモデルの組み立て
    if debug:
        print(f'create new model')
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


# コールバック関数
callbacks = []
if early_stopping:
    callbacks.append(
        EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=0, mode='auto')
    )
if tensor_board:
    callbacks.append(
        TensorBoard(log_dir=get_log_path(), histogram_freq=0, batch_size=32, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
    )

# 学習：入力データと結果データを同一にする
elapsed = time.perf_counter()
history = model.fit(
    x=train_data, # 学習データ(入力) 
    y=train_data, # 学習データ(出力)、入力と同じ
    epochs=epochs, 
    batch_size=4, 
    validation_split=0.1,
    callbacks = callbacks)
elapsed = time.perf_counter() - elapsed
if debug:
    print(f'training elapse time {elapsed}')

# 学習済みモデルを保存
model.save(model_path)
if debug:
    print(f'Saved model file {model_path}')
