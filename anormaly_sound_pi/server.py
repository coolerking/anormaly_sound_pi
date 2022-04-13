# -*- coding: utf-8 -*-
"""
実行モジュール: Web UIから音声評価結果を確認する。
"""
import os
import sys
import argparse
from keras.models import load_model
import scipy.io.wavfile as wav
from python_speech_features import logfbank
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
model = load_model(args.model)

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
result = {}
files = get_all_path(path=datadir)
for file in files:
    # 評価対象音声ファイル読み込み
    (rate,sig) = wav.read(file)
    # 誤差計算
    detect_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)
    # 評価対象音声ファイルデータを使って異常かどうか予測
    detect_pred = model.predict(detect_data)
    result[file] = detect_pred

# アプリケーションオブジェクト生成
app = Flask(__name__)
# session 用シークレットキー
app.secret_key='sound_anormaly_web_ui'

@app.route('/update', methods=['GET'])
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
    global result
    file = get_latest_path(path=datadir)
    if file is not None:
        if os.path.isfile(file):
            # 評価対象音声ファイル読み込み
            (rate,sig) = wav.read(file)
            # 誤差計算
            detect_data = logfbank(sig,rate,winlen=0.01,nfilt=input_size)
            # 評価対象音声ファイルデータを使って異常かどうか予測
            detect_pred = model.predict(detect_data)
            result[file] = detect_pred
            if debug:
                print(f'update dict {str(result)}')
        elif debug:
            print(f'latest file {file} not exists.')
    else:
        print('latest file is None.')
    print(result)
    print(type(result))
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
    global result
    result = {}
    if debug:
        print('clear dict')
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
    # /template/index.html を表示
    return render_template('index.html')

if __name__ == '__main__':
    """
    起動時のオプション処理を行い、Webアプリケーションを開始する。
    """
    app.run(debug=debug,host=host, port=port)
