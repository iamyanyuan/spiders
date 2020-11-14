from MyQR import myqr  # pip3 install MyQR
import os


def make_dynamic_qr(words, picture=None, save_name=None, **kwargs):
    """生成动态（底图）二维码"""
    myqr.run(words=words,  # 输入链接或str作为参数
             version=1,  # 边长，范围1~40
             level='H',  # 纠错等级，从低到高： L M Q H
             picture=picture,  # 底图文件
             colorized=True,  # True 底图为彩色， False底图为黑白
             contrast=1.0,  # 对比度，默认1.0
             brightness=1.0,  # 底图的亮度，默认1.0
             save_name=save_name,  # 输出文件名
             save_dir=os.getcwd()  # 存储的目录，默认当前目录
             )


if __name__ == '__main__':
    words = "https://github.com/iamyanyuan/spiders"
    picture = 't.gif'
    save_name = "qr.gif"
    make_dynamic_qr(words, picture, save_name)
