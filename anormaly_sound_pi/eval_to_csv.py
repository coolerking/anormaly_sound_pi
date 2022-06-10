# -*- coding: utf-8 -*-
"""
評価結果をCSVファイルとして出力するモジュール。
"""
import os
import sys
import csv
import time
import datetime
import argparse

from keras.models import load_model
import scipy.io.wavfile as wav
from python_speech_features import logfbank
from sklearn.metrics import mean_squared_error

from utils import DATA_PATH, get_all_path

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))


parser = argparse.ArgumentParser(description='sound anormaly detection web ui server')
parser.add_argument('--datadir', type=str, default=DATA_PATH, help='data directory path')
parser.add_argument('--model', type=str, default=os.path.join('model','model.h5'), help='trained model filename')
parser.add_argument('--output', type=str, default='eval_' + now.strftime("%Y%m%d%H%M%S") + '.csv', help='output csv filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
args = parser.parse_args()

"""
デバッグオプション
"""
debug = args.debug
if debug:
    print(f'arguments: {args}')

"""
音声データの入力データサイズ
"""
input_size = args.input_size

"""
データディレクトリ
"""
if not os.path.isdir(args.datadir):
    if debug:
        print(f'data dir {args.datadir} not exist, stop.')
    sys.exit(-1)
datadir = args.datadir

"""
モデル
"""
if not os.path.isfile(args.model):
    if debug:
        print(f'model {args.model} not exist, stop.')
    sys.exit(-1)
if debug:
    print(f'loading model: {args.model}')
model = load_model(args.model)
if debug:
    print('finish loading')

def get_score(file:str) -> float:
    """
    音声異常データファイルパス先のファイルを読み込み、異常判定スコアを算出する。

    Parameters:
    --------
    file: str
        対象とする音声データファイル(wav形式)
    
    Returns
    --------
    detect_score: float
        異常判定スコア
    """
    # 評価対象音声ファイル読み込み
    (rate,sig) = wav.read(file)
    # 誤差計算
    detect_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)
    # 評価対象音声ファイルデータを使って異常かどうか予測
    detect_pred = model.predict(detect_data)
    # 異常判定スコア計算
    return mean_squared_error(detect_data, detect_pred)

def get_scores(dirpath:str) -> list:
    """
    すべての音声データを評価して、結果リストを返却する。

    Parameters:
    ----------
    datapath: str   音声データが格納されているディレクトリパス

    Returns
    -----------
    list            要素[<ファイル名>, <スコア>] のリスト
    """
    scores = []
    files = get_all_path(path=dirpath)
    for file in files:
        score = []
        # 異常判定スコア計算
        detect_score = get_score(file)
        if debug:
            print(f'predicted target: {file}, score: {str(detect_score)}')
        score.append(file)
        score.append(detect_score)
        scores.append(score)
    return scores

if __name__ == '__main__':
    elapsed = time.perf_counter()
    # 全スコア結果を取得
    scores = get_scores(args.datadir)
    print(f'evaluated {len(scores)} wav files')

    # CSVファイルへ格納する
    with open(args.output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for score in scores:
            writer.writerow(score)
    elapsed = time.perf_counter() - elapsed
    print(f'output csv file: {args.output} / {elapsed} sec')
