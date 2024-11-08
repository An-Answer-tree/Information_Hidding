import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt

# 步骤1: 读取音频文件
rate, data = wavfile.read('music.wav')  # 替换成你的音频文件名

# 步骤2: 一维离散傅里叶变换
data_fft = fft(data)

# 步骤3: 一维离散傅里叶逆变换
data_ifft = ifft(data_fft)

# 步骤4: 观察结果
# 原始音频波形
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.title("Original Audio Waveform")
plt.plot(data)

# 频谱图
plt.subplot(2, 2, 2)
plt.title("Frequency Spectrum")
plt.plot(np.abs(data_fft))

# 恢复的音频波形
plt.subplot(2, 2, 3)
plt.title("Recovered Audio Waveform")
plt.plot(np.real(data_ifft))

plt.tight_layout()
plt.show()