# -*- coding: utf-8 -*-
"""
音声ファイル特徴量可視化Web UI

1. 以下のコマンドで実行
```bash
$ streamlit run view.py
```
2. ブラウザで http://localhost:8501 を開く
3. Browse files を押下し、wavファイルを選択
"""
import io
import sklearn
import librosa
import librosa.display
import librosa.feature
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def _normalize(x:any, axis=0):
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

def _show_feature(uploaded_file:any)-> None:
    """
    対象のwavファイルを読み込み、メタ情報や各種特徴量グラフを
    表示する。

    Parameters
    -----
    uploaded_file   アップロードファイルオブジェクト(streamlit)

    Returns
    -----
    None
    """
    # ヘッダ（ファイル名）
    st.header(f'{uploaded_file.name}')

    # 音声再生ガジェット
    bytes_data = uploaded_file.getvalue()
    st.audio(bytes_data)

    # メタ情報
    data, sr =sf.read(io.BytesIO(bytes_data))
    y = librosa.core.resample(data, orig_sr=sr, target_sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    zero_crossings = librosa.zero_crossings(y=y, pad=False)
    st.write(f'- Filename: {uploaded_file.name}')
    st.write(f'- Size: {str(len(bytes_data))} bytes')
    st.write(f'- Sampling rate: {str(sr)} Hz')
    st.write('- Audio length: %.2f sec' % (len(y) / sr))
    st.write('- Tempo %.5f bpm' % tempo)
    st.write(f'- Zero Crossing Rate(sum): {str(sum(zero_crossings))}')

    # 振幅グラフ Sound Frequency Graph
    #  X座標: 時間
    #  Y座標: 周波数(Hz:1秒間に何回の生起が発生するか)
    fig1 = plt.figure(figsize=(16,6))
    plt.title(f'Sound Frequency / {uploaded_file.name}')
    librosa.display.waveshow(y=y, sr=sr)
    st.write('### Sound Frequency')
    st.pyplot(fig1)
        
    # 音圧グラフ Sound Pressure Graph
    #  X座標: 周波数(Hz:1秒間に何回の生起が発生するか)
    #  Y座標: 周波数の振幅(ログスケール)
    D = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    fig2 = plt.figure(figsize=(16, 6))
    plt.title(f'Sound Pressure / {uploaded_file.name}')
    plt.plot(D)
    plt.grid()
    st.write('### Sound Pressure')
    st.pyplot(fig2)

    # 振幅スペクトログラム Amplitude Spectrogram (声の場合、声紋ともいう)
    #  X座標: 時間 (Sec)
    #  Y座標: 周波数の振幅(ログスケール/フルスケール,dBFS)
    #  値: 座標点該当周波数での強度(振幅の大きさ)
    DB = librosa.amplitude_to_db(D, ref=np.max)
    fig3 = plt.figure(figsize=(16, 6))
    librosa.display.specshow(DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
    plt.title(f'Amplitude Spectrogram / {uploaded_file.name}')
    plt.colorbar()
    st.write('### Amplitude Spectrogram')
    st.pyplot(fig3)

    # Melスペクトログラム Mel-Spectrogram
    #  X座標: 時間 (Sec)
    #  Y座標: 周波数の振幅(ログスケール/フルスケール,dBFS)
    #  値: 座標点該当周波数での強度(周波数の振幅,dB)
    S = librosa.feature.melspectrogram(y, sr=sr)
    S_DB = librosa.amplitude_to_db(S, ref=np.max)
    fig4= plt.figure(figsize=(16, 6))
    img = librosa.display.specshow(S_DB, sr=sr, hop_length=512, x_axis='time', y_axis='log')
    plt.title(f'Mel Spectrogram / {uploaded_file.name}')
    plt.colorbar(img, format='%+2.0f dB')
    st.write('### Mel Spectrogram')
    st.pyplot(fig4)

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

    fig5 = plt.figure(figsize=(16, 6))
    # 振幅グラフ(青線)の描画
    librosa.display.waveshow(y, sr=sr, alpha=0.5, color='b')
    # スペクトル重心(赤線)の描画
    plt.plot(t, _normalize(spectral_centroids), color='r')
    plt.title(f'Spectral Centroid / {uploaded_file.name}')
    st.write('### Spectral Centroid')
    st.pyplot(fig5)

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

    fig6 = plt.figure(figsize=(16, 6))
    # 振幅グラフ(青線)の描画
    librosa.display.waveshow(y, sr=sr, alpha=0.5, color='b')
    # 周波数ロールオフ(赤線)の描画
    plt.plot(t, _normalize(spectral_rolloff), color='r')
    plt.title(f'Spectral Rolloff / {uploaded_file.name}')
    st.write('### Spectral Rolloff')
    st.pyplot(fig6)

    # メル周波数ケプストラム係数
    # Mel-Frequency Cepstral Coefficients (MFCCs)
    mfccs = librosa.feature.mfcc(y, sr=sr)
    mfccs = _normalize(mfccs, axis=1)
    fig7 = plt.figure(figsize=(16, 6))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    plt.title(f'MFCCs / {uploaded_file.name}')
    plt.colorbar(format='%+2.0f')
    st.write('### MFCCs')
    st.pyplot(fig7)

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
    fig8 = plt.figure(figsize=(16, 6))
    librosa.display.specshow(log_mel, sr=sr, x_axis='time', y_axis='linear')
    plt.title(f'log-Mel Spectrogram / {uploaded_file.name}')
    st.write('### log-MFCCs')
    st.pyplot(fig7)


def main()->None:
    """
    Streamlit を使ってWeb UIを表示する。

    Parameters
    -----
    None

    Returns
    -----
    None
    """
    # ページ設定
    st.set_page_config(layout='wide')

    # タイトル
    st.title('Sound Feartures')
    st.write('You can evaluate sound features of selected wav files.')

    # ファイル選択(サイドバー)
    st.sidebar.header('Choose wav files')
    st.sidebar.write('You can select multi files.')
    uploaded_files = st.sidebar.file_uploader('Choose wav files', accept_multiple_files=True)
    if uploaded_files is not None and len(uploaded_files) >0:
        index = 0
        for col in st.columns(len(uploaded_files)):
            with col:
                _show_feature(uploaded_files[index])
                index = index + 1

if __name__ == '__main__':
    main()