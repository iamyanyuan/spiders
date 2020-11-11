import requests
import time
import pymysql
from fake_useragent import UserAgent
from lxml import etree

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='mysql',
                       database='spider', charset='utf8')
cursor = conn.cursor()


class Get_ips(object):
    """获取免费代理ip"""

    def get_kdl_ips(self):
        """快代理ip"""
        for page in range(1, 2):
            time.sleep(1)
            headers = {'User-Agent': UserAgent().random}
            text = requests.get(url='https://www.kuaidaili.com/free/inha/{}'.format(page),
                                headers=headers)
            html = etree.HTML(text.content)
            trs = html.xpath('//*[@id="list"]/table/tbody/tr')
            data = []

            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = str(tr.xpath('./td[2]/text()')[0])
                proxy_type = tr.xpath('./td[4]/text()')[0]
                res_tiem = float(tr.xpath('./td[6]/text()')[0].split('秒')[0])
                end_tiem = tr.xpath('./td[7]/text()')[0].split(' ')[0]
                data.append((ip, port, proxy_type, res_tiem, end_tiem))
            yield data

    def get_yundaili(self):
        for p in range(1, 7):
            time.sleep(1)
            headers = {'User-Agent': UserAgent().random}
            text = requests.get(url='http://www.ip3366.net/free/?stype=1&page=%d' % p, headers=headers)

            html = etree.HTML(text.content.decode('gbk'))
            trs = html.xpath('//*[@id="list"]/table/tbody/tr')
            data = []

            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = str(tr.xpath('./td[2]/text()')[0])
                proxy_type = tr.xpath('./td[4]/text()')[0]
                res_tiem = tr.xpath('./td[6]/text()')[0].split('秒')[0]
                end_tiem = tr.xpath('./td[7]/text()')[0].split(' ')[0].replace('/', '-')
                data.append((ip, port, proxy_type, res_tiem, end_tiem))
            print(data)
            yield data

    def put_in_sql(self):
        """数据入库"""
        # ips = self.get_kdl_ips()
        ips = self.get_yundaili()

        for data in ips:
            for i in data:
                my_sql = "insert  proxy(ip, port, proxy_type, res_tiem, end_tiem) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(my_sql, i)
                conn.commit()


class Proxies(object):
    """获取代理ip"""

    def delete_ip(self, ip):
        del_sql = "delete from proxy where ip='{0}'".format(ip)
        cursor.execute(del_sql)
        conn.commit()

    def get_useful_ip(self, ip, port, proxy_type):
        url = 'http://www.baidu.com'
        if proxy_type == 'HTTP':
            proxy_url = 'http://{}:{}'.format(ip, port)
            proxies = {'http': proxy_url}
        else:
            proxy_url = 'https://{}:{}'.format(ip, port)
            proxies = {'https': proxy_url}
        try:
            response = requests.get(url, proxies=proxies)
        except Exception as e:
            print('Ip invalid')
            self.delete_ip(ip)
        else:
            code = response.status_code
            if code < 200 and code > 300:
                print('Ip invalid')
                self.delete_ip(ip)

            else:
                # code >= 200 and code < 300:
                print('Ip useful:', ip)

    def get_random_ip(self):
        rand_sql = "select ip, port, proxy_type from proxy order by rand() limit 1"
        cursor.execute(rand_sql)
        for i in cursor.fetchall():
            print(i)
            ip = i[0]
            port = i[1]
            proxy_type = i[2]
            useful_ip = self.get_useful_ip(ip, port, proxy_type)

            if useful_ip:
                if proxy_type == 'HTTP':
                    print("http://{}:{}".format(ip, port))
                    return "http://{}:{}".format(ip, port)
                else:
                    print("https://{}:{}".format(ip, port))
                    return "https://{}:{}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    get_ip = Proxies()
    get_ip.get_random_ip()  # 获取随机IP

    getip = Get_ips()  # 爬取免费代理
    # getip.get_yundaili()  # 运行爬虫提取ip
    # getip.put_in_sql()  # ip入库
