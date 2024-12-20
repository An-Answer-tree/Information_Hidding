import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def chi_square_test(image_path):
    # 加载图像并转换为灰度
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)

    # 统计像素值频率
    observed_freq = np.bincount(image_array.flatten(), minlength=256)

    # 计算期望频率
    expected_freq = np.zeros(256)
    for i in range(256):
        expected_freq[i] = (observed_freq[i // 2 * 2] + observed_freq[i // 2 * 2 + 1]) / 2

    # 计算卡方值
    chi_square_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)

    print(f"Chi-square statistic for {image_path}: {chi_square_stat}")

# 应用卡方测试
chi_square_test('cover_image.png')
chi_square_test('stego_image.png')