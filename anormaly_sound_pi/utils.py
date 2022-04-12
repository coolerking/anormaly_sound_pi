#-*-coding:utf-8-*-
"""
ユーティリティ関数モジュール
"""
import os
import glob
import datetime

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
    #print(path)
    files = glob.glob(path)
    #print(files)
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
        print(file)
        print(suffix)
        print(file.rfind(suffix))
        print(len(file) - len(suffix))
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
    print(path)
    print(prefix)
    print(suffix)
    print(_get_files(path=path, prefix=prefix, suffix=suffix))
    print(remove_files)
    print(age)
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
        return files[-1:0][0]
    else:
        return None


if __name__ == '__main__':
    #print(_get_date_format_path())
    #print(_get_date_format_path(path='hehehe', prefix='fufufu_', suffix='www'))
    #print(_get_files(path='anormaly_sound_pi', prefix='', suffix=''))
    #print(_get_files(path='anormaly_sound_pi', prefix='', suffix='wav'))
    print(_get_files(path=DATA_PATH, prefix=DATA_PREFIX, suffix=DATA_SUFFIX))
