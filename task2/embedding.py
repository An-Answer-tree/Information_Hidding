import numpy as np
from scipy.io import wavfile

def embed_text_in_audio(audio_file_in, text, audio_file_out, m0, m1, N, attenuation):
    # 读取音频文件
    sample_rate, audio_data = wavfile.read(audio_file_in)
    
    # 只使用一个声道
    if audio_data.ndim > 1:
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
    stegano_audio = []
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
        
        stegano_audio.append(echo_subframe)
        
    # 将所有子帧连接起来
    stegano_audio = np.concatenate(stegano_audio)
    
    # 填充剩余的音频数据
    remaining_audio = audio_data[num_bits*N:]
    stegano_audio = np.concatenate((stegano_audio, remaining_audio))
    
    # 将浮点型转换回整数型并写入文件
    stegano_audio_int = np.int16(stegano_audio / np.max(np.abs(stegano_audio)) * 32767)
    wavfile.write(audio_file_out, sample_rate, stegano_audio_int)
    
    
def extract_text_from_audio(audio_file_in, m0, m1, N):
    # 读取音频文件
    sample_rate, stegano_audio_data = wavfile.read(audio_file_in)
    
    # 如果是立体声，转换为单声道
    if stegano_audio_data.ndim == 2:
        stegano_audio_data = stegano_audio_data[:, 0]
    
    # 将音频数据转换为浮点型并归一化
    stegano_audio_data = stegano_audio_data.astype(np.float32)
    stegano_audio_data /= np.max(np.abs(stegano_audio_data))
    
    num_subframes = len(stegano_audio_data) // N
    
    bits = ''
    for i in range(num_subframes):
        # 获取子帧
        subframe = stegano_audio_data[i*N : (i+1)*N]
        
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
    audio_file_in = 'Before_I_Rise.wav'  # 输入的音频文件
    # 要隐藏的文本
    # "谁问你了"英文圣经节选🤣
    text = 'NiceOpinionButThere\'sJustOneSmallProblemWithIt:WhoAsked?LikeGenuinelyWhoAsked?WhoGaveYouTheTalkingStick?I\'llTellYouNobodyDidNobodyAskedDudeThereAreZeroPeopleWhoAskedAmongUsLookIInvitedEveryoneWhoAskedToThisPartyAYOThisIsPhotoOfEveryoneWhoAskedYooCheckItOutIt\'sABusFullOfEveryoneWhoAskedYouKnowWhatManI\'llDoYouAFavorClearlyWeCan\'tSeeWhoAskedSoI\'mJustGonnaDoItMyselfI\'mGonnaFindOutWhoAsked'
    audio_file_out = 'output_'+ audio_file_in # 输出的音频文件
    rate, data = wavfile.read(audio_file_in)    # 获取采样率
    del data

    帧长 = 100   # 子帧的长度(ms)
    m0 = 120   # 当比特为 '0' 时的回声时延
    m1 = 180   # 当比特为 '1' 时的回声时延
    N = int(rate*帧长/1000)   # 子帧的样本数
    attenuation = 0.5  # 回声的衰减因子
    
    # 调用嵌入函数
    embed_text_in_audio(audio_file_in, text, audio_file_out, m0, m1, N, attenuation)
    print("文本已成功嵌入到音频文件中。")
    
    # 调用提取函数
    extracted_text = extract_text_from_audio(audio_file_out, m0, m1, N)
    print('写入的文本为:', text)
    print('提取的文本为:', extracted_text)
    
if __name__ == '__main__':
    main()