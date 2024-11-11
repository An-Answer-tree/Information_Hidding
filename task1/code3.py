import numpy as np
from scipy.io import wavfile
import pywt
import matplotlib.pyplot as plt

# 读取PCM音频文件
file_path = "audio_work/sardine_fish.wav"
sample_rate, audio_channel = wavfile.read(file_path)

# 只选择一个声道进行分析
if audio_channel.ndim > 1:
    audio_channel = audio_channel[:, 0]

# 执行一维DWT变换 (使用Daubechies小波 'db1' 作为示例) 
coeffs = pywt.wavedec(audio_channel, wavelet="db1")

# 获取DWT分解的各级系数, 该音频下自动计算出的系数有21级
# cAn为整体近似系数, 对应信号的低频部分, cDn为第n级细节系数，对应信号的高频部分
cAn=coeffs[0]
cD1=coeffs[-1]
cD2=coeffs[-2]
cD4=coeffs[-4]
cD8=coeffs[-8]
cD16=coeffs[-16]
# 逆DWT重建信号
audio_reconstructed = pywt.waverec(coeffs, wavelet="db1")

# 可视化原始音频信号、DWT分解结果和逆DWT重建信号
plt.figure(figsize=(12, 10))

# 原始音频信号
plt.subplot(3, 3, 1)
plt.plot(audio_channel, color="blue")
plt.title("Original Audio Signal")
# 整体近似系数
plt.subplot(3, 3, 2)
plt.plot(cAn, color="green")
plt.title("DWT Approximation Coefficients")
# 重建的音频信号
plt.subplot(3, 3, 3)
plt.plot(audio_reconstructed, color="purple")
plt.title("Inverse DWT Reconstructed Audio Signal")

# DWT分解的各级细节系数
plt.subplot(3, 3, 4)
plt.plot(cD1, color="red")
plt.title("DWT Detail Coefficients - Level 1")

plt.subplot(3, 3, 5)
plt.plot(cD2, color="orange")
plt.title("DWT Detail Coefficients - Level 2")

plt.subplot(3, 3, 6)
plt.plot(cD4, color="brown")
plt.title("DWT Detail Coefficients - Level 4")

plt.subplot(3, 3, 7)
plt.plot(cD8, color="black")
plt.title("DWT Detail Coefficients - Level 8")

plt.subplot(3, 3, 8)
plt.plot(cD16, color="pink")
plt.title("DWT Detail Coefficients - Level 16")

plt.tight_layout()
plt.show()
