from selenium import webdriver
import time
import csv


class TaobaoSpider():
    def __init__(self):
        # 设置selenium属性
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
        self.driver = webdriver.Chrome('./chromedriver', options=option)
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        self.driver.maximize_window()  # 最大化窗口

    def get_url(self, url):
        self.driver.get(url=url)

    def login(self, username, password):
        # 登录
        self.driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath('//div[@class="fm-btn"]').click()
        time.sleep(4)

    def search_parse_save(self, username, password, keyword='华为手机'):
        """搜索"""
        self.driver.find_element_by_css_selector('#q').send_keys(keyword)
        self.driver.find_element_by_class_name('search-button').click()
        time.sleep(3)
        print(self.driver.current_url)
        # 如果出现登录页面，则登录
        if "login" in str(self.driver.current_url):
            self.login(username, password)
        time.sleep(3)
        # 提取数据
        lis = self.driver.find_elements_by_css_selector('#mainsrp-itemlist > div > div > div:nth-child(1) > div.item')
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        self.driver.implicitly_wait(1)

        item = {}
        for li in lis:
            item['price'] = li.find_element_by_css_selector('.ctx-box > div.row > div.price > strong').text
            item['deal'] = li.find_element_by_css_selector('.ctx-box .deal-cnt').text
            item['title'] = li.find_element_by_css_selector('.ctx-box .row-2 a').text

            try:
                if li.find_element_by_css_selector('.shop > a > span:nth-child(2)').text:
                    item['shop'] = li.find_element_by_css_selector('.shop > a > span:nth-child(2)').text
                elif li.find_element_by_css_selector('.shop > a').text:
                    item['shop'] = li.find_element_by_css_selector('.shop > a').text
                else:
                    continue
            except Exception as e:
                item['shop'] = "shop error"
            item['city'] = li.find_element_by_css_selector('.ctx-box > div.row > div.location').text
            print(item)
            time.sleep(2)
            # 保存数据到csv文件中
            try:
                with open('tb.csv', 'a', encoding='utf_8_sig', newline='') as f:
                    w = csv.DictWriter(f, dict(item).keys())
                    w.writerow(item)
            except Exception as e:
                print('write error')
        self.driver.quit()


if __name__ == '__main__':
    tb = TaobaoSpider()

    base_url = 'https://www.taobao.com/'
    username = 'tb账号'  # tb账号
    password = '密码'  # 密码
    keyword = '女包 小清新'  # 搜索关键词
    tb.get_url(base_url)
    tb.search_parse_save(username, password, keyword)
