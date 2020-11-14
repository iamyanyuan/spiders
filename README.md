# author yanyuan

# 目标网站：https://news.cnblogs.com/

# 随机ua
# 安装第三方库 pip install fake_useragent


```class UserAgenMiddleware(object):
    def process_request(self, request, spider):
        try:            
            ua = UserAgent()
            request.headers['User-Agent'] = ua.random
        except FakeUserAgentError:
            pass```
            
            
# 免费代理ip使用说明： 先抓取代理ip、port --> 入库 --> 检验ip是否可用，删除不可用ip
# 最后有效的ip可能只有几十个，可以多找一些免费代理网站提取ip，或者直接花钱买更高效
# scrapy中设置随机ip方法跟设置ua方法类似 

注意：免费代理大部分是不能使用，建议使用付费代理ip测试，或者两个结合

scrapy的暂停和重启：
1、先创建一个目录用于存放任务
启动命令
```scrapy crawl blogs -s JOBDIR=jobs/blog001```

main.py文件中设置
execute(['scrapy', 'crawl', 'blogs', '-s', 'JOBDIR=jobs/blog001'])


验证码识别说明：
1、Tesseract OCR 图片识别引擎只能识别比较简单的验证码
2、另外三个是付费打码，可根据自己需求选择，有好的打码平台页可以分享。
           