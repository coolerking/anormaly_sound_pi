# -*- coding: utf-8 -*-
"""
実行モジュール: 音声データを可視化(グラフ化)する。
pip install librosa
python graph.py --path hogehoge.wav --debug True

注意：
T470 では、260秒wavファイルを4本を連続で実行できませんでした(メモリ不足)。

FYI:
https://qiita.com/kotai2003/items/69638e18b6d542fb275e
"""
import os
import sys
import time
import glob
import datetime
import sklearn
import librosa
import librosa.display
import librosa.feature
import argparse
import numpy as np
import matplotlib.pyplot as plt

def normalize(x, axis=0):
    """
    行もしくは列ごとに正規化処理

    Parameters
    ------
    x       値群
    axis    正規化範囲(対象の次元数)

    Returns
    -----
    正規化済み値群
    """
    return sklearn.preprocessing.minmax_scale(x, axis=axis)

def make_graphs(path:str, sr:int=None, show:bool=False, debug:bool=False) -> None:
    """
    音声データ分析のための各種情報・グラフを表示/保存する。

    Parameters
    ----
    path:str        wavファイルパス、wavファイル群(拡張子wav)が格納されているディレクトリ
    sr:int          サンプリング周波数
    show:bool
    """

    # wavファイルのロード
    # y: 音声信号の値 (audio time series) 振幅
    #sr: サンプリング周波数
    if sr is None:
        y, sr = librosa.load(path)
    else:
        y, sr = librosa.load(path=path, sr=sr)

    # テンポ
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Zero Crossings
    # Zero Crossing Rate(ZCR)は、音声の波形を描いたとき、
    # 波が中央より上(正)から中央より下(負)に、
    # またはその逆に変化する頻度を数えて、
    # その頻度により音声の特徴を表すというもの。
    # ZCRが大きいほどより noisy な音声と捉えられるらしい。
    zero_crossings = librosa.zero_crossings(y=y, pad=False)

    if debug:
        print('** Target wav file meta data **')
        print(f' Target wav sound file path: {path}')
        print(' Sampling rate (Hz): %d' % sr)
        print(' Audio length (seconds): %.2f' % (len(y) / sr))
        print(' Tempo %.5f bpm' % tempo)
        print(' Zero Crossing Rate(sum): %d' % sum(zero_crossings))

    if not show:
        outpath = path + '_meta.csv'
        with open(outpath, 'w') as f:
            f.write('\"path\", \"sampling rate(Hz)\", \"length(secs)\", \"tempo (bpm)\", \"ZCR\", \"date\"\n')
            f.write(f'\"{path}\", {str(sr)}, {str(len(y) / sr)}, {str(tempo)}, {str(sum(zero_crossings))}, {str(datetime.datetime.now())}\n')
        if debug:
            print(f'saved file: {outpath}')

    # 振幅グラフ Sound Frequency Graph
    #  X座標: 時間
    #  Y座標: 周波数(Hz:1秒間に何回の生起が発生するか)
    plt.figure(figsize=(16,6))
    plt.title(f'Sound Frequency / {path}')
    librosa.display.waveshow(y=y, sr=sr)

    if show:
        plt.show()
    else:
        outpath = path + '_sound_frequency.png'
        plt.savefig(outpath)
        if debug:
            print('** Sound Frequency Graph **')
            print('  X: time (Sec)')
            print('  Y: frequency (Hz)')
            print(f'saved graph: {outpath}')


    # 音圧グラフ Sound Pressure Graph
    #  X座標: 周波数(Hz:1秒間に何回の生起が発生するか)
    #  Y座標: 周波数の振幅(ログスケール)
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    plt.figure(figsize=(16, 6))
    plt.title(f'Sound Pressure / {path}')
    plt.plot(D)
    plt.grid()

    if show:
        plt.show()
    else:
        outpath = path + '_sound_pressure.png'
        plt.savefig(outpath)
        if debug:
            print('** Sound Pressure Graph **')
            print('  X: frequency (Hz)')
            print('  Y: amplitude of frequency (dB)')
            print(f'saved graph: {outpath}')


    # 振幅スペクトログラム Amplitude Spectrogram (声の場合、声紋ともいう)
    #  X座標: 時間 (Sec)
    #  Y座標: 周波数の振幅(ログスケール/フルスケール,dBFS)
    #  値: 座標点該当周波数での強度(振幅の大きさ)
    DB = librosa.amplitude_to_db(D, ref=np.max)
    plt.figure(figsize=(16, 6))
    librosa.display.specshow(DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
    plt.title(f'Amplitude Spectrogram / {path}')
    plt.colorbar()

    if show:
        plt.show()
    else:
        outpath = path + '_amplitude_spectrogram.png'
        plt.savefig(outpath)
        if debug:
            print('** Amplitude Spectrogram Graph **')
            print('  X: time (Sec)')
            print('  Y: amplitude of frequency (dBFS)')
            print('  value: power')
            print(f'saved graph: {outpath}')


    # Melスペクトログラム Mel-Spectrogram
    #  X座標: 時間 (Sec)
    #  Y座標: 周波数の振幅(ログスケール/フルスケール,dBFS)
    #  値: 座標点該当周波数での強度(周波数の振幅,dB)
    S = librosa.feature.melspectrogram(y, sr=sr)
    S_DB = librosa.amplitude_to_db(S, ref=np.max)
    plt.figure(figsize=(16, 6))
    img = librosa.display.specshow(S_DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
    plt.title(f'Mel Spectrogram / {path}')
    plt.colorbar(img, format='%+2.0f dB')

    if show:
        plt.show()
    else:
        outpath = path + '_mel_spectgram.png'
        plt.savefig(outpath)
        if debug:
            print('** Mel Spectrogram Graph **')
            print('  X: time (Sec)')
            print('  Y: Frequency (Hz)')
            print('  value: power log scale (dB)')
            print(f'save graph: {outpath}')

    # スペクトラルセントロイド(スペクトル重心) Spectral Centroid
    #  X座標: 時間 (Sec)
    #  Y座標(青): 周波数(Hz:1秒間に何回の生起が発生するか)
    #  Y座標(赤): スペクトル重心(周波数の加重平均値、音響特徴量の一種)

    # スペクトル重心の算出
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]
    # 可視化のためのフレームカウント(時間変数)を計算
    frames = range(len(spectral_centroids))
    # フレームカウントを時間（秒）に変換
    t = librosa.frames_to_time(frames)

    plt.figure(figsize=(16, 6))
    # 振幅グラフ(青線)の描画
    librosa.display.waveshow(y, sr=sr, alpha=0.5, color='b')
    # スペクトル重心(赤線)の描画
    plt.plot(t, normalize(spectral_centroids), color='r')
    plt.title(f'Spectral Centroid / {path}')
    if show:
        plt.show()
    else:
        outpath = path + '_spectral_centroid.png'
        plt.savefig(outpath)
        if debug:
            print('** Spectral Centroid Graph **')
            print('  X: time (Sec)')
            print('  Y (blue): frequency')
            print('  Y (red):  spectral centroid')
            print(f'saved graph: {outpath}')


    # 周波数ロールオフ Spectral Rolloff
    #  X座標: 時間 (Sec)
    #  Y座標(青): 周波数(Hz:1秒間に何回の生起が発生するか)
    #  Y座標(赤): Spectral Rolloff(周波数の加重平均値、音響特徴量の一種)

    # ロールオフ（roll-off）とは、フィルタの「切れ」を表す特性。
    # フィルタの帯域の端における通過特性の変化の急峻さで表され、
    # 大きい値ほど切れがよいフィルタとなる。
    # 単位はdB/octave（周波数が2倍変化した時の通過特性の変化）
    # またはdB/decade（周波数が10倍変化した時の通過特性の変化）。

    # 周波数ロールオフの計算
    spectral_rolloff = librosa.feature.spectral_rolloff(y, sr=sr)[0]

    plt.figure(figsize=(16, 6))
    # 振幅グラフ(青線)の描画
    librosa.display.waveshow(y, sr=sr, alpha=0.5, color='b')
    # 周波数ロールオフ(赤線)の描画
    plt.plot(t, normalize(spectral_rolloff), color='r')
    plt.title(f'Spectral Rolloff / {path}')
    if show:
        plt.show()
    else:
        outpath = path + '_spectral_rolloff.png'
        plt.savefig(outpath)
        if debug:
            print('** Spectral Rolloff Graph **')
            print('  X: time (Sec)')
            print('  Y (blue): frequency')
            print('  Y (red):  spectral rolloff')
            print(f'saved graph: {outpath}')

    # メル周波数ケプストラム係数
    # Mel-Frequency Cepstral Coefficients (MFCCs)

    mfccs = librosa.feature.mfcc(y, sr=sr)
    mfccs = normalize(mfccs, axis=1)
    #if debug:
        

    plt.figure(figsize=(16, 6))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.title(f'MFCCs / {path}')
    plt.colorbar(format='%+2.0f')

    if show:
        plt.show()
    else:
        outpath = path + '_MFCCs.png'
        plt.savefig(outpath)
        if debug:
            print('** Mel-Frequency Cepstral Coefficients(MFCCs) Graph **')
            print('  X: time (Sec)')
            print('  Y: Frequency (Hz)')
            print('  value: mel-spectrogram')
            print('    mean: %.2f' % mfccs.mean())
            print('    var:  %.2f' % mfccs.var())
            print(f'saved graph: {outpath}')

    # ログメル周波数ケプストラム係数 log-melspectrogram

    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    # 事前に計算されたパワースペクトルを使っても同じ結果になる
    #D = np.abs(librosa.stft(y))
    #S = librosa.feature.melspectrogram(S=D, sr=sr)
    # melフィルターバンク構築のためのカスタム引数による、
    # mel-frequencyスペクトログラム係数の表示(デフォルトfmax=sr/2)
    #S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    # 対数変換
    log_mel = np.log(mel)
    plt.figure(figsize=(16, 6))
    librosa.display.specshow(log_mel, sr=sr, x_axis='time', y_axis='linear')
    plt.title(f'log-Mel Spectrogram / {path}')
    if show:
        plt.show()
    else:
        outpath = path + '_log_mel_spectrogram.png'
        plt.savefig(outpath)
        if debug:
            print('** log-mel spectrogram **')
            print('  X: time (Sec)')
            print('  Y: Frequency (Hz)')
            print('  value: mel-spectrogram log-scale')
            print(f'saved graph: {outpath}')


if __name__ == '__main__':
    """
    引数を処理し、音声データを1件づつ分析グラフ群を作成する。
    """

    # 引数管理
    parser = argparse.ArgumentParser(description='output some graphs for sound wav file')
    parser.add_argument('--path', type=str, default='test.wav', help='target wav file path or directory path')
    parser.add_argument('--sr', type=int, default=44100, help='sampling rate')
    parser.add_argument('--show', type=bool, default=False, help='show graph if true')
    parser.add_argument('--debug', type=bool, default=False, help='print debug lines')
    args = parser.parse_args()

    # ターゲットファイルパス
    if args.path is None:
        print(f'target wav path is {str(args.path)}, stop.')
        sys.exit(-1)

    if os.path.isfile(args.path):
        paths = []
        paths.append(args.path)
    elif os.path.isdir(args.path):
        paths = glob.glob(os.path.join(args.path, '*.wav'))

    if args. debug:
        print(f'Target paths: {str(paths)}')
    
    total_elapsed = 0.0
    for path in paths:
        start = time.perf_counter()
        if args.debug:
            print(f'* START: {path}')
        make_graphs(path=path, sr=args.sr, show=args.show, debug=args.debug)
        elapsed = time.perf_counter() - start
        if args.debug:
            print(f'* END: {path} elapsed time {elapsed} sec')
        total_elapsed = total_elapsed + elapsed

    if args.debug:
        print(f'* END total elapsed time {total_elapsed} sec')        

    sys.exit(0)
