from PIL import Image
import pytesseract

img = Image.open('./image/phone1.png')
result = pytesseract.image_to_string(img)
print(result)

# linux 环境下的安装
# sudo apt-get install tesseract-ocr  # 图片识别引擎
# pip install pillow  # 打开图片文件
# pip install pytesseract  # 解析图片中数据
