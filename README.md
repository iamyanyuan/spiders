# author yanyuan

# 目标网站：https://news.cnblogs.com/

# 随机ua
# 安装第三方库 pip install fake_useragent


`class UserAgenMiddleware(object):
    def process_request(self, request, spider):
        try:            
            ua = UserAgent()
            request.headers['User-Agent'] = ua.random
        except FakeUserAgentError:
            pass`
            
            
            