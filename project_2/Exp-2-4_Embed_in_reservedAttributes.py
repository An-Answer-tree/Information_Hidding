import struct

def embed_in_reserved_attributes(bmp_file, data, output_file):
    with open(bmp_file, 'rb') as file:
        bmp_header = file.read(14)  # 读取文件头部
        rest_of_file = file.read()  # 读取剩余文件内容

    # 将数据打包为无符号四字节整数
    packed_data = struct.pack('<I', data)
    if len(packed_data) > 4:
        raise ValueError("Data is too large to embed, max size is 4 bytes")
    # 生成新的文件头，替换保留字段
    new_header = bmp_header[:6] + packed_data + bmp_header[10:]

    # 写入新的 BMP 文件
    with open(output_file, 'wb') as file:
        file.write(new_header)
        file.write(rest_of_file)

    print(f"Data embedded into {output_file}")


def extract_data_from_reserved_attributes(bmp_file):
    with open(bmp_file, 'rb') as file:
        file.read(6)  # 跳过文件头的开始部分
        hidden_data = file.read(4)  # 读取隐藏的数据

    # 解包数据
    data = struct.unpack('<I', hidden_data)[0]
    print(f"Data extracted: {data}")
    return data

embed_in_reserved_attributes('./resource/2/baboon.bmp', 12580, './resource/2/baboon3.bmp')
extract_data_from_reserved_attributes('./resource/2/baboon3.bmp')