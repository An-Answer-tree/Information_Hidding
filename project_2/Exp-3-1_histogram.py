import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def plot_histograms(original_image_path, stego_image_path):
    # 加载原始图像并转换为灰度
    original_image = Image.open(original_image_path).convert('L')
    original_array = np.array(original_image)

    # 加载含密图像并转换为灰度
    stego_image = Image.open(stego_image_path).convert('L')
    stego_array = np.array(stego_image)

    # 计算两个图像的直方图
    original_histogram, bin_edges = np.histogram(original_array, bins=256, range=(0, 255))
    stego_histogram, _ = np.histogram(stego_array, bins=256, range=(0, 255))

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.title("Histogram Comparison")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.plot(bin_edges[0:-1], original_histogram, color='blue', label='Original Image')
    plt.plot(bin_edges[0:-1], stego_histogram, color='red', linestyle='dashed', label='Stego Image')
    plt.legend()
    plt.grid(True)
    plt.show()

# 显示原始图像和含密图像的直方图
plot_histograms('./resource/2/DSC04813.png', './resource/2/output1.png')