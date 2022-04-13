# -*- coding: utf-8 -*-
"""
実行モジュール: Web UIから音声評価結果を確認する。

実行例:

python server.py --host XXX.XXX.XXX.XXX --port 5000 --datadir data --model models/hogehoge.h5 --debug True

実行後、ブラウザで http://XXX.XXX.XXX.XXX:5000/ を開く
"""
import os
import sys
import argparse
from keras.models import load_model
import scipy.io.wavfile as wav
from python_speech_features import logfbank
from sklearn.metrics import mean_squared_error
from flask import Flask, jsonify, render_template, session

from utils import DATA_PATH, get_latest_path, get_all_path

# 引数の定義及び読み込み
parser = argparse.ArgumentParser(description='sound anormaly detection web ui server')
parser.add_argument('--datadir', type=str, default=DATA_PATH, help='data directory path')
parser.add_argument('--model', type=str, default='model\model.h5', help='trained model filename')
parser.add_argument('--input_size', type=int, default=20, help='input data size')
parser.add_argument('--port', type=int, default=5000, help='listen port')
parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
parser.add_argument('--host', type=str, default='127.0.0.1', help='web server host address')
args = parser.parse_args()


"""
デバッグオプション
"""
debug = args.debug

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

"""
入力データのカラム数
"""
input_size = args.input_size

"""
ホスト
"""
host = args.host

"""
ポート
"""
port = args.port

"""
音声異常検知辞書の更新
"""
labels = []
values = []
result = {
    'labels': labels,
    'values': values,
}
def _get_score(file:str) -> float:
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

# 初期読み込み
files = get_all_path(path=datadir)
for file in files:
    # 異常判定スコア計算
    detect_score = _get_score(file)
    if debug:
        print(f'predicted target: {file}, score: {str(detect_score)}')
    labels.append(file)
    values.append(detect_score)

# アプリケーションオブジェクト生成
app = Flask(__name__)
# session 用シークレットキー
app.secret_key='sound_anormaly_web_ui'

@app.route('/update', methods=['POST'])
def update():
    """
    音声異常検知辞書の更新。

    Parameters
    --------
    None

    Returns
    --------
    result: dict
        音声異常検知辞書
    """
    global result, labels, values
    file = get_latest_path(path=datadir)
    if file is not None:
        if os.path.isfile(file):
            # 異常判定スコア計算
            detect_score = _get_score(file)
            if file not in labels:
                labels.append(file)
                values.append(detect_score)
                if debug:
                    print(f'[update] append label: {file}, value: {str(detect_score)}')
                    print(f'[update] update dict {str(result)}')
        elif debug:
            print(f'[update] latest file {file} not exists.')
    elif debug:
        print('[update] latest file is None.')
    return jsonify(result)

@app.route('/clear', methods=['GET'])
def clear_result():
    """
    結果を初期化。
    Parameters
    --------
    None

    Returns
    --------
    result: dict
        音声異常検知辞書
    """
    global result, labels, values
    result = {}
    labels = []
    values = []
    if debug:
        print('[clear] clear dict')
    return jsonify(result)

@app.route('/', methods=['GET'])
def show_index():
    """
    index.html を表示する。

    Parameters
    --------
    None

    Returns
    --------
    None
    """
    # セッション上に初期化した観測データを格納
    if 'result' not in session:
        # 観測初期化
        session['result'] = result
        #session['labels'] = labels
        #session['values'] = values
    # /template/index.html を表示
    return render_template('index.html')

if __name__ == '__main__':
    """
    起動時のオプション処理を行い、Webアプリケーションを開始する。
    """
    app.run(debug=debug,host=host, port=port)
