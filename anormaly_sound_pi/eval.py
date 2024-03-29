# -*- coding: utf-8 -*-
"""
実行モジュール: 音声ファイルを評価し、スコアを返却する。

python eval.py ... 
echo $?

エラーコードにScore値が返却される。
エラーコード-1の場合、何も処理していない。
"""

import os
import sys
import datetime
from keras.models import load_model
import scipy.io.wavfile as wav
from python_speech_features import logfbank
from sklearn.metrics import mean_squared_error
import argparse
from utils import DATA_PATH, get_latest_path

'''
引数管理
'''
parser = argparse.ArgumentParser(description='evaluate a wav format file with the trained model')
parser.add_argument('--datadir', type=str, default=DATA_PATH, help='data directory path')
parser.add_argument('--eval_path', type=str, default=None, help='eval target wav filename')
parser.add_argument('--model', type=str, default='model\model.h5', help='trained model filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
parser.add_argument('--ignore_rows', type=int, default=10, help='ignore data rows')
parser.add_argument('--visible', type=bool, default=False, help='output spectgram images')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
#parser.add_argument('--dev_index', type=int, default=1, help='USB mic index no')
args = parser.parse_args()

"""
デバッグオプション
"""
debug = args.debug

"""
入力データのカラム数
"""
input_size = args.input_size

"""
学習済みモデルファイルパス
"""
model_path = args.model

"""
評価対象音声ファイルパス
"""
eval_path = args.eval_path

"""
先頭削除行数
"""
ignore_rows = args.ignore_rows

# 引数表示
if debug:
    print(args)
    print(eval_path)
    print(args.datadir)
    print(get_latest_path(path=args.datadir))
# 評価対象音声ファイルの存在確認
if eval_path is not None:
    if not os.path.isfile(eval_path):
        if debug:
            print(f'eval path {str(eval_path)} not exist.')
        eval_path = get_latest_path(path=args.datadir)
else:
    eval_path = get_latest_path(path=args.datadir)
if debug:
    print(eval_path)
    print(args.datadir)
    print(get_latest_path(path=args.datadir))
if eval_path is None or not os.path.isfile(eval_path):
    if debug:
        print(f'eval path {str(eval_path)} not exist, stop.')
    sys.exit(-1)

# 学習済みモデルファイルのロード
if not os.path.exists(model_path):
    if debug:
        print(f'model path {model_path} not exist, stop')
    sys.exit(-1)
model = load_model(model_path)

# 評価対象音声ファイル読み込み
(rate,sig) = wav.read(eval_path)

# 誤差計算
detect_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)
if debug:
    print(f'target data original shape: {detect_data.shape}')

# 先頭10削除
detect_data = detect_data[ignore_rows:]
if debug:
    print(f'target data reshaped: {detect_data.shape}')

# 評価対象音声ファイルデータを使って異常かどうか予測
detect_pred = model.predict(detect_data)

# 異常判定スコア計算
detect_score = mean_squared_error(detect_data, detect_pred)
if debug:
    print(f'Score: {str(detect_score)}')

# 可視化が真の場合、スペクトラム出力
if args.visible:
    import datetime
    from utils import save_spectgram
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    save_spectgram(sig.flatten(), 44100, timestamp + '_wave.png')
    save_spectgram(detect_data.flatten(), 44100, timestamp + '_input.png')
    save_spectgram(detect_pred.flatten(), 44100, f'{timestamp}_output_{format(detect_score,".4f")}.png')
# 終了
sys.exit(detect_score)
