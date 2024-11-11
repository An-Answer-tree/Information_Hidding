import numpy as np
from scipy.io import wavfile
import pywt
import matplotlib.pyplot as plt

# 读取wav音频文件
file_path = 'music.wav'  # 请替换为实际文件路径
sample_rate, audio_channel = wavfile.read(file_path)

# 选择一个声道（例如第一个声道）进行分析
if audio_channel.ndim > 1:
    audio_channel = audio_channel[:, 0]

# 执行一维DWT变换（使用Daubechies小波 'db1' 作为示例）
coeffs = pywt.wavedec(audio_channel, wavelet='db1', level=4)

# 分离低频和高频系数
cA4, cD4, cD3, cD2, cD1 = coeffs  # cA是低频部分，cD是各级高频部分

# 逆DWT重建信号
audio_reconstructed = pywt.waverec(coeffs, wavelet='db1')

# 可视化原始音频信号、DWT分解结果和逆DWT重建信号
plt.figure(figsize=(12, 10))

# 原始音频信号
plt.subplot(5, 1, 1)
plt.plot(audio_channel, color='blue')
plt.title("Original Audio Signal")

# DWT分解的各级细节系数
plt.subplot(5, 1, 2)
plt.plot(cD1, color='red')
plt.title("DWT Detail Coefficients - Level 1")

plt.subplot(5, 1, 3)
plt.plot(cD2, color='orange')
plt.title("DWT Detail Coefficients - Level 2")

plt.subplot(5, 1, 4)
plt.plot(cA4, color='green')
plt.title("DWT Approximation Coefficients (Low Frequency)")

plt.subplot(5, 1, 5)
plt.plot(audio_reconstructed, color='purple')
plt.title("Inverse DWT Reconstructed Audio Signal")

plt.tight_layout()
plt.show()