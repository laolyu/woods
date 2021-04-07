# -*- coding:utf-8 -*-
from aip import AipOcr


def get_file_content(file):
    # image_path = r'C:\Users\Administrator\Pictures' # 读取图片
    # filePath = "forOCR.png"
    with open(file, 'rb') as fp:
        return fp.read()


def write_to_file(content):
    with open(r'C:\Users\Administrator\Desktop\text.txt', 'a', encoding='utf-8') as f:
        f.write(content)


def domain(file):
    config = {
        'appId': '20014895',
        'apiKey': 'EosZ9o20EkuIN1kfe3YiwjHA',
        'secretKey': 'Xz81lU90C00dqRbElLTcUgOu2aZ78Y8c'
    }
    client = AipOcr(**config)
    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    try:
        image_string = client.basicAccurate(get_file_content(file), options)  # 调用百度的OCR API
        image_string = image_string['words_result']  # 解析结果
        # print(image_string)
        words_result = ''
        for string in image_string:
            # words_result += string['words']  # 不换行
            words_result += string['words'] + '\n'  # 换行

        print(words_result)
    except Exception as e:
        words_result = e

    write_to_file(words_result)


if __name__ == '__main__':
    file = r'F:\screenshot\screenshot.png'
    domain(file)
