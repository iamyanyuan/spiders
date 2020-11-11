# __author__ = 'yanyuan'

# 简单版selenium模拟登录淘宝和搜索商品并输出商品信息，
# 像ua、代理、反识别、翻页等 可自行设置和对相关功能板块的进一部封装
# chrome浏览器的版本要和webdriver浏览器驱动版本要一致
# 下载链接: http://npm.taobao.org/mirrors/chromedriver/
from selenium import webdriver
import time

driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.taobao.com')

# 搜索
driver.find_element_by_css_selector('#q').send_keys('华为手机')
driver.find_element_by_class_name('search-button').click()
time.sleep(2)

# 登录
driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys('淘宝账号')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys('密码')
time.sleep(2)
driver.find_element_by_xpath('//div[@class="fm-btn"]').click()
time.sleep(3)

# 提取数据
lis = driver.find_elements_by_css_selector('#mainsrp-itemlist > div > div > div:nth-child(1) > div.item')
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
driver.implicitly_wait(1)
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
    time.sleep(30)

driver.quit()  # 关闭driver
