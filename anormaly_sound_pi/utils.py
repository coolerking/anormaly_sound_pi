#-*-coding:utf-8-*-
"""
ユーティリティ関数モジュール
"""
import os
import glob
import datetime
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

"""
定数: デフォルトデータディレクトリ名
"""
DATA_PATH = 'data'

"""
定数: デフォルトデータファイル先頭文字列
"""
DATA_PREFIX = 'mic_'

"""
定数: デフォルトデータファイル拡張子文字列
"""
DATA_SUFFIX = 'wav'

"""
定数: データファイル残存履歴数デフォルト値
"""
DATA_AGE = 2

def _get_date_format_path(path:str=DATA_PATH, prefix:str=DATA_PREFIX, suffix:str=DATA_SUFFIX) -> str:
    """
    YYYYmmdd_HHMMSS 形式のファイルパス文字列を生成する。

    Parameters
    --------
    path: str, default DATA_PATH
        ファイルが配置されるディレクトリ
    prefix: str, default DATA_PREFIX
        ファイル名の先頭文字列
    suffix: str, default DATA_SUFFIX
        ファイル名の拡張子指定文字列
    
    Returns
    --------
    path: str
        YYYYmmdd_HHMMSS 形式のファイルパス文字列
    """
    if path is None or len(path) == 0:
        path = ''
    elif path.rfind(os.sep) == -1:
        path += os.sep
    if prefix is None or len(prefix) == 0:
        prefix = ''
    if suffix is None or len(suffix) == 0:
        suffix = '.log'
    elif suffix.find('.') == -1:
        suffix = '.' + suffix
    path += prefix + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + suffix
    return path

def _get_files(path:str=DATA_PATH, prefix:str=DATA_PREFIX, suffix:str=DATA_SUFFIX) -> list:
    """
    条件に合致するファイルパス文字列を昇順にして返却する。

    Parameters
    --------
    path: str, default None
        検索対象とするディレクトリ（存在しない場合、作成する）
    prefix: str, default None
        検索対象とするファイル名先頭文字列
    suffix: str, default None
        検索対象の拡張子文字列
    
    Returns
    --------
    matched_list: list
        条件に合致するファイルパス文字列リスト（昇順）
    """
    matched_files = []
    if path is None or len(path) == 0:
        path = '*'
    elif path.rfind(os.sep) == -1:
        path += os.sep
        os.makedirs(path, exist_ok=True)
        path += '*'
    files = glob.glob(path)
    if len(files) == 0 or ((prefix is None or prefix == '') and (suffix is None or suffix == '')):
        for file in files:
            matched_files.append(_get_path(path, file))
        return sorted(matched_files)
    for file in files:
        prefix_matched = False
        if prefix is not None and len(prefix) > 0 and file.find(prefix) >= 0:
            prefix_matched = True
        elif prefix is None or len(prefix) == 0:
            prefix_matched = True
        if prefix_matched == False:
            continue
        suffix_matched = False
        if suffix is not None and len(suffix) != 0 and file.rfind(suffix) == len(file) - len(suffix):
            suffix_matched = True
        elif suffix is None or len(suffix) == 0:
            suffix_matched = True
        if prefix_matched and suffix_matched:
            matched_files.append(file)
    return sorted(matched_files)

def _get_path(path=DATA_PATH, filename=''):
    """
    ファイルパス文字列を作成する。

    Parameters
    --------
    path: str, default DATA_PATH
        ファイルが存在するパス名
    filename: str, default ''
        ファイル名
    
    Returns
    --------
    path: str
        ファイルパス文字列
    """
    if path is None or len(path) == 0:
        path = ''
    elif path.rfind(os.sep) == -1:
        path += os.sep
    return path + filename

def data_rotate(path:str=DATA_PATH, prefix:str=DATA_PREFIX, suffix:str=DATA_SUFFIX, age:int=DATA_AGE) -> str:
    """
    引数に指定されたディレクトリ、先頭文字列・拡張子文字列ファイルを指定の履歴数で管理する。
    戻り値は次に作成すべきファイルパス文字列。

    Parameters
    --------
    path: str, default DATA_PATH
        ディレクトリ（存在しない場合、作成する）
    prefix: str, default DATA_PREFIX
        ファイル名先頭文字列
    suffix: str, default DATA_SUFFIX
        ファイル拡張子文字列
    age: int, default DATA_AGE
        残すファイル履歴
    
    Returns
    --------
    path: str
        次に作成すべきファイルパス
    """
    remove_files = _get_files(path=path, prefix=prefix, suffix=suffix)[:(-1 * (age-1))]
    for remove_file in remove_files:
        os.remove(remove_file)
    return _get_date_format_path(path=path, prefix=prefix, suffix=suffix)

def get_latest_path(path:str=DATA_PATH, prefix:str=DATA_PREFIX, suffix:str=DATA_SUFFIX) -> str:
    """
    引数に指定されたディレクトリ、先頭文字列・拡張子文字列を満たすファイルのうち最後に作成されたファイルのパスを返却する。

    Parameters
    --------
    path: str, default DATA_PATH
        ディレクトリ（存在しない場合、作成する）
    prefix: str, default DATA_PREFIX
        ファイル名先頭文字列
    suffix: str, default DATA_SUFFIX
        ファイル拡張子文字列
    
    Returns
    --------
    path: str
        次に作成すべきファイルパス、存在しない場合はNoneを返却
    """
    files = _get_files(path=path, prefix=prefix, suffix=suffix)
    if len(files) > 0:
        return files[-1]
    else:
        return None

def get_all_path(path:str=DATA_PATH, prefix:str=DATA_PREFIX, suffix:str=DATA_SUFFIX) -> str:
    """
    引数に指定されたディレクトリ、先頭文字列・拡張子文字列を満たすファイルのすべてのパス（昇順）を返却する。

    Parameters
    --------
    path: str, default DATA_PATH
        ディレクトリ（存在しない場合、作成する）
    prefix: str, default DATA_PREFIX
        ファイル名先頭文字列
    suffix: str, default DATA_SUFFIX
        ファイル拡張子文字列
    
    Returns
    --------
    paths: array(syr)
        ファイルパスリスト、存在しない場合は[]を返却
    """
    return _get_files(path=path, prefix=prefix, suffix=suffix)

def get_log_path() -> str:
    """
    ログディレクトリ先文字列を作成する。

    Returns
    --------
    logdir: str
        ログディレクトリ先文字列
    """
    return './logs_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def save_spectgram(y:any, framerate:int=44100, path:str=None) ->None:
    """
    周波数スペクトラム(縦軸:kHz、横軸:sec)イメージ(PNG形式)ファイルを生成する。

    y:any           測定値の時系列データ
    framerate:int   フレームレート
    path:str        PNG形式イメージファイルパス
    """

    # セグメント長
    N = 1024
    # scikit-learnのスペクトラム関数を使用
    freqs, times, Sx = signal.spectrogram(
        y,                  # 測定値の時系列データ
        fs=framerate,       # サンプリング頻度←waveフレームレート
        window='hamming',   # 窓関数:ハミング窓を使用
        nperseg=N,          # セグメント長
        noverlap=N-100,     # セグメント間でオーバラップするサイズ
        detrend=False,      # トレンド除去しない
        scaling='spectrum') # スペクトログラム変数：V**2パワースペクトルを計算

    # グラフ描画
    f, ax = plt.subplots()
    # X軸:times(秒) Y軸:freqs/1000(kHz) C軸(色): Sxの対数×10 
    ax.pcolormesh(times, freqs/1000, 10* np.log10(Sx), cmap='viridis')
    ax.set_ylabel('Frequency[kHz]')
    ax.set_xlabel('Time[s]')
    if path is None:
        path = 'spectgram_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    plt.savefig(path)

def show_spectgram(y:any, framerate:int=44100) ->None:
    """
    周波数スペクトラム(縦軸:kHz、横軸:sec)イメージ(PNG形式)ファイルを表示する。

    Parameters
    -----
    y:any           測定値の時系列データ
    framerate:int   フレームレート
    """

    # セグメント長
    N = 1024
    # scikit-learnのスペクトラム関数を使用
    freqs, times, Sx = signal.spectrogram(
        y,                  # 測定値の時系列データ
        fs=framerate,       # サンプリング頻度←waveフレームレート
        window='hamming',   # 窓関数:ハミング窓を使用
        nperseg=N,          # セグメント長
        noverlap=N-100,     # セグメント間でオーバラップするサイズ
        detrend=False,      # トレンド除去しない
        scaling='spectrum') # スペクトログラム変数：V**2パワースペクトルを計算

    # グラフ描画
    f, ax = plt.subplots()
    # X軸:times(秒) Y軸:freqs/1000(kHz) C軸(色): Sxの対数×10 
    ax.pcolormesh(times, freqs/1000, 10* np.log10(Sx), cmap='viridis')
    ax.set_ylabel('Frequency[kHz]')
    ax.set_xlabel('Time[s]')
    if path is None:
        path = 'spectgram_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
    plt.show()

#if __name__ == '__main__':
    #print(_get_date_format_path())
    #print(_get_date_format_path(path='hehehe', prefix='fufufu_', suffix='www'))
    #print(_get_files(path='anormaly_sound_pi', prefix='', suffix=''))
    #print(_get_files(path='anormaly_sound_pi', prefix='', suffix='wav'))
    #print(_get_files(path=DATA_PATH, prefix=DATA_PREFIX, suffix=DATA_SUFFIX))
