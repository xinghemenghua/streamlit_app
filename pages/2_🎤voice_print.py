import streamlit as st
import librosa
import numpy as np
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft
import librosa.display
from pydub import AudioSegment


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="voice_print",
    page_icon="🎤",
)
matplotlib.rc("font", family='SimHei')  # 显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 显示符号

def displayWaveform(wav_file):  # 显示语音时域波形
    plt.figure(dpi=600)  # 将显示的所有图分辨率调高
    matplotlib.rc("font", family='SimHei')  # 显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 显示符号
    samples_1, sr = librosa.load(wav_file, sr=16000)
    # samples = samples[6000:16000]
    samples = samples_1[0::1]
    time = np.arange(0, len(samples)) * (1.0 / sr)

    ft = fft(samples)
    magnitude = np.absolute(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
    frequency = np.linspace(0, sr, len(magnitude))  # (0, 16000, 121632)
    # plot spectrum，限定[:40000]
    # plt.figure(figsize=(18, 8))

    two_subplot_fig = plt.figure(figsize=(10, 10), layout='constrained')

    plt.subplot(211)
    plt.plot(time, samples)
    plt.title("语音信号时域波形")
    plt.xlabel("时长（秒）")
    plt.ylabel("振幅")
    # plt.savefig("your dir\语音信号时域波形图", dpi=600)

    plt.subplot(212)
    plt.plot(frequency[:40000], magnitude[:40000])  # magnitude spectrum
    plt.title("语音信号频域谱线")
    plt.xlabel("频率（赫兹）")

    st.pyplot(two_subplot_fig)


def displaySpectrogram(file_to_Spectrogram_plot):
    x, sr = librosa.load(file_to_Spectrogram_plot, sr=16000)

    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
    spectrogram = librosa.amplitude_to_db(librosa.stft(x))

    # show
    spectrogram_figure = plt.figure(figsize=(10, 6), layout='constrained')
    librosa.display.specshow(spectrogram, y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('语音信号对数谱图')
    plt.xlabel('时长（秒）')
    plt.ylabel('频率（赫兹）')
    st.pyplot(spectrogram_figure)


def download_excel_num(file_to_excel):
    global sound_step
    samples_excel_pd, sr = librosa.load(file_to_excel, sr=16000)  # sr为采样率
    # samples = samples[6000:16000]
    samples_excel = samples_excel_pd[0::sound_step]
    st.metric("数据点数量", len(samples_excel))
    data_df = pd.DataFrame(samples_excel)
    return data_df, len(samples_excel)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    # 关键3，float_format 控制精度，将data_df写到表格的第一页中。若多个文件，可以在page_2中写入
    return df.to_csv()


def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_mp3(filepath)
    return song


def convert_wav(wav_output):
    return wav_output.export(format="wav")



# 展示一级标题
st.header('音频波形数据提取')
st.subheader('生成时域/频域图和语谱图')
up_load_wav_file = st.file_uploader(label="上传wav格式音频文件以绘制时域/频域图", type=['wav'],
                                    accept_multiple_files=False,
                                    key="1",
                                    help=None, on_change=None)

if up_load_wav_file is not None:
    displayWaveform(up_load_wav_file)

file_to_Spectrogram = st.file_uploader(label="上传wav格式音频文件以绘制语谱图", type=['wav'],
                                       accept_multiple_files=False,
                                       key="2",
                                       help=None, on_change=None)

if file_to_Spectrogram is not None:
    displaySpectrogram(file_to_Spectrogram)

st.subheader('生成EXCEL文件')
st.text('EXCEL最大可受数据值（行数）为1048576')
sound_step = st.slider(
    label='选择取值步长',
    min_value=1, max_value=300, step=5)
file_wav_to_excel = st.file_uploader(label="上传wav格式音频文件获取EXCEL文件", type=['wav'],
                                     accept_multiple_files=False,
                                     key="3",
                                     help=None, on_change=None)

if file_wav_to_excel is not None:
    data, samples_excel_number = download_excel_num(file_wav_to_excel)
    if data is not None and samples_excel_number < 1048575:
        csv = convert_df(data)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='large_df.csv',
            mime='text/csv', )
    elif samples_excel_number >= 1048575:
        st.warning('数据点超过EXCEL行数，请重新输入步长', icon="⚠️")

st.write('')
st.write('')
st.write('')
st.write('')

st.markdown('[在线转换音频文件](https://www.aconvert.com/cn/audio/)')
st.markdown('[在线转换PDF文件](https://www.aconvert.com/cn/pdf/)')
st.markdown('[在线转换图像文件](https://www.aconvert.com/cn/image/)')

