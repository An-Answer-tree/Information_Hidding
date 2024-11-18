import struct

def check_bmp_for_hidden_data(bmp_file):
    with open(bmp_file, 'rb') as f:
        # 读取文件头字段
        bfType = struct.unpack('H', f.read(2))[0]
        bfSize = struct.unpack('I', f.read(4))[0]
        bfReserved1 = struct.unpack('H', f.read(2))[0]
        bfReserved2 = struct.unpack('H', f.read(2))[0]
        bfOffBits = struct.unpack('I', f.read(4))[0]
        biSize = struct.unpack('I', f.read(4))[0]
        biWidth = struct.unpack('I', f.read(4))[0]
        biHeight = struct.unpack('i', f.read(4))[0]
        biPlanes = struct.unpack('H', f.read(2))[0]
        biBitCount = struct.unpack('H', f.read(2))[0]
        biCompression = struct.unpack('I', f.read(4))[0]
        biSizeImage = struct.unpack('I', f.read(4))[0]
        biXPelsPerMeter = struct.unpack('I', f.read(4))[0]
        biYPelsPerMeter = struct.unpack('I', f.read(4))[0]
        biClrUsed = struct.unpack('I', f.read(4))[0]
        biClrImportant = struct.unpack('I', f.read(4))[0]

        # 计算每像素字节数
        biByteCount = (biBitCount + 7) // 8
        # 计算理论上的图像数据大小
        biSizeImage = biWidth * biByteCount * biHeight
        # 计算理论上的文件总大小
        calculated_bfSize = biSizeImage + bfOffBits
        
        # 输出比较结果
        print(f"实际文件大小: {bfSize}")
        print(f"计算文件大小: {calculated_bfSize}")
        print(f"文件头偏移: {bfOffBits}")
        
        if bfSize != calculated_bfSize:
            print("可能在文件头与数据之间隐藏了信息。")
        else:
            print("未检测到异常，文件头与数据之间没有明显隐藏信息。")

# 使用函数检查文件
check_bmp_for_hidden_data('./resource/2/baboon2.bmp')