from scrapy.cmdline import execute
import time
import sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(['scrapy', 'crawl', 'blogs'])
# scrapy crawl blogs -s JOBDIR=jobs/blog001
execute(['scrapy', 'crawl', 'blogs', '-s', 'JOBDIR=jobs/blog001'])


# execute(['scrapy', 'crawl', 'cnblogs'])

# while True:
#     # 定时抓取
#     os.system('scrapy crawl blogs')
#     time.sleep(10*60)  # 每10分钟
