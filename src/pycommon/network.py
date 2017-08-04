import requests
import bs4
import urlpath
import os
import re
from  datetime import datetime
from common.filesystem import *


##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对网络下载的相关的一些封装，如获取内容，保存网页地址等</p>
# </br></br>
# <p>该文件引用了request进行网络请求方法 </p>
##


def download_str(url, encoding=None):
    response = requests.get(url)
    if encoding is not None:
        response.encoding = encoding
    return response.text


def download_file(url, local_file):
    try:
        start_time = datetime.now()
        dir_name = os.path.dirname(local_file)
        url_path = urlpath.URL(url)
        if (os.path.isdir(dir_name) is 0):
            os.makedirs(dir_name)
        headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
        )

        r = requests.get(url, headers=headers, timeout=3)

        file_pure_path = urlpath.URL(local_file)
        local_file = file_pure_path.drive + file_pure_path.path
        with open(local_file, "wb") as code:
            code.write(r.content)
        end_time = datetime.now()
        print('下载完成:{0} ==> {1},耗时:{2}s'.format(url, local_file, (end_time - start_time).seconds))
    except Exception as e:
        print('下载出错...' + str(e))


def combine_url(refurl, path):
    path_low = path.lower()
    if (path_low.startswith('http://') or path_low.startswith('https://')):
        return path;
    url = urlpath.URL(refurl)
    if (path_low.startswith('/')):
        return "{0}{1}".format(url.drive, path)
    else:
        return "{0}/{1}".format(url.parent, path)


def download_or_read_file(url, localfile):
    if os.path.exists(localfile) == False:
        download_file(url, localfile)
    return read_all_text(localfile)
