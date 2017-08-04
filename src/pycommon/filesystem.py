import os
import hashlib


##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对文件操作的简单封装，方便文件操作时调用</p>
# <p>主要包括文件写入，文件读取，文件追加和获取文件md5</p>
#
# <br/><br/>
# <p>该文件引用了os,hashlib基础库，不需要额外引用第三方库</p>
#
##

def write_all_text(path, content, encoding='utf-8'):
    """
    把内容写入到文件
    :param path: 路径
    :param content: 文件名
    :param encoding: 编码
    :return:
    """
    dir_name = os.path.dirname(path)
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    file = open(path, 'w', encoding=encoding, errors='ignore')
    file.write(content)
    file.close()


def read_all_text(path, encoding='utf-8'):
    """
        读取文件内容
    :param path:文件路径
    :param encoding:编码
    :return:
    """
    if os.path.exists(path) is False:
        return ''
    file = open(path, encoding=encoding, errors='ignore')
    text = file.read()
    file.close()
    return text


def append_text_to_file(path, text, encoding='utf-8'):
    """
    追加文件
    :param path: 
    :param text: 
    :param encoding: 
    :return:
    """
    if os.path.exists(path):
        file = open(path, 'a', encoding=encoding, errors='ignore')
        file.write(text)
        file.close()
    else:
        write_all_text(path, text, encoding)


def get_file_md5(filen_name):
    """
        获取文件的md5
    :param filen_name :文件名称
    :return:
    """
    if not os.path.isfile(filen_name):
        return
    my_hash = hashlib.md5()
    f = open(filen_name, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        my_hash.update(b)
    f.close()
    return my_hash.hexdigest()


if __name__ == "__main__":
    append_text_to_file('e:/ab.txt', 'aewew')
