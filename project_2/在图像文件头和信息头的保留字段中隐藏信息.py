import struct

def embed_data_in_bmp(bmp_file, data, output_file):
    with open(bmp_file, 'rb') as file:
        bmp_header = file.read(14)  # 读取文件头部
        rest_of_file = file.read()  # 读取剩余文件内容

    # 将数据打包为无符号四字节整数
    packed_data = struct.pack('<I', data)

    # 生成新的文件头，替换保留字段
    new_header = bmp_header[:6] + packed_data + bmp_header[10:]

    # 写入新的 BMP 文件
    with open(output_file, 'wb') as file:
        file.write(new_header)
        file.write(rest_of_file)

    print(f"Data embedded into {output_file}")

# 调用函数，示例中隐藏数字 12345
embed_data_in_bmp('baboon.bmp', 12345, 'baboon_with_hidden_data.bmp')

def extract_data_from_bmp(bmp_file):
    with open(bmp_file, 'rb') as file:
        file.read(6)  # 跳过文件头的开始部分
        hidden_data = file.read(4)  # 读取隐藏的数据

    # 解包数据
    data = struct.unpack('<I', hidden_data)[0]
    print(f"Data extracted: {data}")
    return data

# 调用函数，从修改过的文件中提取数据
extract_data_from_bmp('baboon_with_hidden_data.bmp')