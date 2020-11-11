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