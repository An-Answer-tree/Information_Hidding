import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, ifft
import matplotlib.pyplot as plt

# 步骤1: 读取音频文件
file_path = "music.wav"  # 替换成你的音频文件名
sample_rate, audio_channel = wavfile.read(file_path)

# 只选择一个声道进行分析
if audio_channel.ndim > 1:
    audio_channel = audio_channel[:, 0]
# 步骤2: 一维离散傅里叶变换
data_fft = fft(audio_channel)

# 步骤3: 一维离散傅里叶逆变换
data_ifft = ifft(data_fft)

# 步骤4: 观察结果
# 原始音频波形
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.title("Original Audio Waveform")
plt.plot(audio_channel)

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
