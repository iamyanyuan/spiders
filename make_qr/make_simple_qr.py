import qrcode  # pip install qrcode


def make_qr(data=None, save_file=None, **kwargs):
    """生成普通二维码"""
    img = qrcode.make(data)  # data可以是url或者文本内容
    img.save(save_file)  # 保存文件
    img.show()  # 展示文件


if __name__ == '__main__':
    data = 'https://github.com/iamyanyuan/spiders'
    save_file = 'github.png'  # 保存文件名
    make_qr(data, save_file)
