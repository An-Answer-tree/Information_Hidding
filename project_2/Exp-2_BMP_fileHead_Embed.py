import struct

def hide_message_in_bmp(bmp_file, txt_file, output_file):
    # 读取 BMP 文件
    with open(bmp_file, 'rb') as f:
        header = f.read(54)  # 读取 BMP 头部
        image_data = f.read()  # 读取图像数据
    
    # 读取文本文件
    with open(txt_file, 'r') as f:
        hidden_message = f.read()
    hidden_message_bytes = hidden_message.encode('utf-8')
    # 按4字节对齐
    hidden_message_bytes += b'\x00' * (4 - len(hidden_message_bytes) % 4)
    
    # 计算新的偏移量
    offset = 54 + len(hidden_message_bytes)
    
    # 修改 BMP 头部数据偏移量
    modified_header = header[:10] + struct.pack('<I', offset) + header[14:]
    
    # 创建新的 BMP 文件
    with open(output_file, 'wb') as f:
        f.write(modified_header)  # 写入修改后的头部
        f.write(hidden_message_bytes)  # 写入隐藏信息
        f.write(image_data)  # 写入原图像数据

# 调用函数
hide_message_in_bmp('./resource/2/baboon.bmp', './resource/2/hidden.txt', './resource/2/baboon2.bmp')