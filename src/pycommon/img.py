from PIL import Image

##
# <p>Copyright (c) 2016-2017 cat80 </p>
# <p>该文件是对excel操作的简单封装，方便操作excel时调用</p>
# <br/><br/>
# <p>该文件引用了xlrd,xlwt库作来操作excel</p>
# <p>主要包含了读取excel(read_xls)和写入excel(write_xls)，具体使用方法看参数说明</p>
#
##

def rgb_to_black_white(src_path, target_path, clear_level=122):
    """
    清理图片为黑白图片并且去噪点
    :param filename:
    :return:
    """
    init_img = Image.open(src_path)
    im = Image.new("RGB", init_img.size)
    im.paste(init_img)
    im.convert('L')  # 去灰度
    (w, h) = im.size
    R = 0
    G = 0
    B = 0
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            rgb = im.getpixel(pos)
            (r, g, b) = rgb
            R = R + r
            G = G + g
            B = B + b
    rate1 = R * 1000 / (R + G + B)
    rate2 = G * 1000 / (R + G + B)
    rate3 = B * 1000 / (R + G + B)
    for x in range(w):
        for y in range(h):
            pos = (x, y)
            rgb = im.getpixel(pos)
            (r, g, b) = rgb
            n = r * rate1 / 1000 + g * rate2 / 1000 + b * rate3 / 1000
            if n >= clear_level:
                im.putpixel(pos, (255, 255, 255))
            else:
                im.putpixel(pos, (0, 0, 0))

    im.save(target_path)
