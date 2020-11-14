import base64
import json
import requests


def base64_api(uname, pwd, img):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


if __name__ == "__main__":
    img_path = "./image/5.png"  # 识别的图片
    result = base64_api(uname='账号', pwd='密码', img=img_path)  # 改成自己的账号和密码
    print(result)
