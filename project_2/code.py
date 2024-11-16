import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def lsb_hide(cover_image_path, secret_message, output_image_path):
    # 加载载体图像
    img = Image.open(cover_image_path)
    img_array = np.array(img)

    # 将秘密信息转换为二进制
    secret_bits = ''.join([format(ord(i), '08b') for i in secret_message])
    n_bits = len(secret_bits)

    # 获取图像的尺寸
    rows, cols, channels = img_array.shape

    # 计算可用的最低有效位数量
    total_pixels = rows * cols * channels
    if n_bits > total_pixels:
        raise ValueError("秘密信息过大，无法嵌入！")

    # 展平图像数组
    flat_img = img_array.flatten()

    # 嵌入秘密信息
    for i in range(n_bits):
        bit = int(secret_bits[i])
        flat_img[i] = (flat_img[i] & ~1) | bit  # 将最低有效位替换为秘密比特

    # 生成含密图像
    stego_img_array = flat_img.reshape(img_array.shape)
    stego_img = Image.fromarray(stego_img_array.astype('uint8'))
    stego_img.save(output_image_path)
    print(f"秘密信息已成功嵌入，生成的图像保存为 {output_image_path}")
    
    
def lsb_extract(stego_image_path, message_length):
    # 加载含密图像
    img = Image.open(stego_image_path)
    img_array = np.array(img)

    # 展平图像数组
    flat_img = img_array.flatten()

    # 提取秘密信息
    secret_bits = ''
    for i in range(message_length * 8):
        bit = flat_img[i] & 1  # 获取最低有效位
        secret_bits += str(bit)

    # 将二进制转换为字符串
    secret_message = ''
    for i in range(0, len(secret_bits), 8):
        byte = secret_bits[i:i+8]
        secret_message += chr(int(byte, 2))

    print(f"提取的秘密信息为：{secret_message}")
    return secret_message


def calculate_psnr(original_image_path, stego_image_path):
    # 加载图像
    original_img = Image.open(original_image_path)
    stego_img = Image.open(stego_image_path)

    # 转换为numpy数组
    original_array = np.array(original_img).astype(float)
    stego_array = np.array(stego_img).astype(float)

    # 计算MSE
    mse = np.mean((original_array - stego_array) ** 2)

    # 如果MSE为零，图像完全相同
    if mse == 0:
        return float('inf')

    # 计算PSNR
    PIXEL_MAX = 255.0
    psnr = 10 * np.log10((PIXEL_MAX ** 2) / mse)
    print(f"PSNR值为：{psnr} dB")
    return psnr


def main():
    # 定义文件路径和秘密信息
    cover_image_path = 'cover_image.png'  # 载体图像路径
    stego_image_path = 'stego_image.png'  # 含密图像保存路径
    secret_message = 'Hello, World!'      # 秘密信息

    # 调用隐藏算法
    lsb_hide(cover_image_path, secret_message, stego_image_path)

    # 计算PSNR
    calculate_psnr(cover_image_path, stego_image_path)

    # 调用提取算法
    extracted_message = lsb_extract(stego_image_path, len(secret_message))

    # 验证提取的消息是否正确
    if secret_message == extracted_message:
        print("信息提取成功，秘密信息完整无误。")
    else:
        print("信息提取失败，秘密信息有误。")

if __name__ == '__main__':
    main()