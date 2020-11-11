import requests

proxies = {
    'https': 'https://121.226.76.213:4264'
}
ret = requests.get(url='https://www.baidu.com', proxies=proxies)

print(ret.text)