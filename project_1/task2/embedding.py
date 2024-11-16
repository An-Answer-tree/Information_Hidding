import numpy as np
from scipy.io import wavfile

def embed_text_in_audio(audio_file_in, text, audio_file_out, m0, m1, N, attenuation):
    # 读取音频文件
    sample_rate, audio_data = wavfile.read(audio_file_in)
    
    # 如果是立体声，转换为单声道
    if audio_data.ndim == 2:
        audio_data = audio_data[:, 0]
    
    # 将音频数据转换为浮点型并归一化
    audio_data = audio_data.astype(np.float32)
    audio_data /= np.max(np.abs(audio_data))
    
    # 将文本转换为二进制位
    bits = ''.join([format(ord(char), '08b') for char in text])
    
    num_bits = len(bits)
    total_samples_needed = num_bits * N
    if total_samples_needed > len(audio_data):
        raise ValueError("音频文件过短，无法嵌入所有文本信息。")
    
    # 初始化嵌入后的音频数据
    stego_audio = []
    for i, bit in enumerate(bits):
        # 获取子帧
        subframe = audio_data[i*N : (i+1)*N]
        
        # 选择对应的回声时延
        m = m0 if bit == '0' else m1
        
        # 生成回声信号
        delayed = np.zeros_like(subframe)
        if m < len(subframe):
            delayed[m:] = subframe[:-m]
        echo_subframe = subframe + attenuation * delayed
        
        stego_audio.append(echo_subframe)
        
    # 将所有子帧连接起来
    stego_audio = np.concatenate(stego_audio)
    
    # 填充剩余的音频数据
    remaining_audio = audio_data[num_bits*N:]
    stego_audio = np.concatenate((stego_audio, remaining_audio))
    
    # 将浮点型转换回整数型并写入文件
    stego_audio_int = np.int16(stego_audio / np.max(np.abs(stego_audio)) * 32767)
    wavfile.write(audio_file_out, sample_rate, stego_audio_int)
    
    
def extract_text_from_audio(audio_file_in, m0, m1, N):
    # 读取音频文件
    sample_rate, stego_audio_data = wavfile.read(audio_file_in)
    
    # 如果是立体声，转换为单声道
    if stego_audio_data.ndim == 2:
        stego_audio_data = stego_audio_data[:, 0]
    
    # 将音频数据转换为浮点型并归一化
    stego_audio_data = stego_audio_data.astype(np.float32)
    stego_audio_data /= np.max(np.abs(stego_audio_data))
    
    num_subframes = len(stego_audio_data) // N
    
    bits = ''
    for i in range(num_subframes):
        # 获取子帧
        subframe = stego_audio_data[i*N : (i+1)*N]
        
        # 计算倒谱
        spectrum = np.fft.fft(subframe)
        log_spectrum = np.log(np.abs(spectrum) + 1e-10)
        cepstrum = np.fft.ifft(log_spectrum).real
        
        # 比较倒谱在 m0 和 m1 位置的幅值
        F0 = np.abs(cepstrum[m0]) if m0 < len(cepstrum) else 0
        F1 = np.abs(cepstrum[m1]) if m1 < len(cepstrum) else 0
        
        # 决定嵌入的比特值
        bit = '0' if F0 > F1 else '1'
        bits += bit
        
    # 将二进制位转换回文本
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    text = ''.join(chars)
    return text

def main():
    audio_file_in = 'music2.wav'  # 输入的音频文件
    text = '921127970138'         # 要隐藏的文本
    audio_file_out = 'output.wav' # 输出的音频文件
    
    m0 = 180   # 当比特为 '0' 时的回声时延
    m1 = 200   # 当比特为 '1' 时的回声时延
    N = 4410   # 子帧的样本数（100ms，对于44100Hz的采样率）
    attenuation = 0.5  # 回声的衰减因子
    
    # 调用嵌入函数
    embed_text_in_audio(audio_file_in, text, audio_file_out, m0, m1, N, attenuation)
    print("文本已成功嵌入到音频文件中。")
    
    # 调用提取函数
    extracted_text = extract_text_from_audio(audio_file_out, m0, m1, N)
    print('提取的文本为:', extracted_text)
    
if __name__ == '__main__':
    main()