import numpy as np
from scipy.io import wavfile
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt

# 读取PCM音频文件
file_path = 'audio_work/sardine_fish.wav'  
sample_rate, audio_channel = wavfile.read(file_path)

# 只选择一个声道进行分析
if audio_channel.ndim > 1:
    audio_channel = audio_channel[:, 0]

# 执行一维DCT变换
dct_transformed = dct(audio_channel, type=2, norm='ortho')

# 执行逆DCT变换
idct_reconstructed = idct(dct_transformed, type=2, norm='ortho')

# 可视化原始音频信号、DCT变换结果、逆变换后的重建信号
plt.figure(figsize=(12, 8))

# 原始音频信号
plt.subplot(2, 2, 1)
plt.plot(audio_channel)
plt.title("Original Audio Waveform")

# DCT变换后的频域表示
plt.subplot(2, 2, 2)
plt.plot(dct_transformed)
plt.title("After DCT")

# 逆DCT变换重建的音频信号
plt.subplot(2, 2, 3)
plt.plot(idct_reconstructed)
plt.title("Recovered Audio Waveform")

plt.tight_layout()
plt.show()