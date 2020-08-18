# -*- coding: utf-8 -*-

# Scrapy settings for domclick_v1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'domclick_v1'

SPIDER_MODULES = ['domclick_v1.spiders']
NEWSPIDER_MODULE = 'domclick_v1.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'domclick_v1 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"cookies": "PAINT_ACTIVE_MAP__COOKIE_VITRINA=%7B%22value%22%3A2%7D; ftgl_cookie_id=758f2bd9b209fa84b09551be3653525a; qrator_ssid=1596657654.551.7k0gOZiOKTmCKiek-s4p6t60cvbp2fmr044r7h4dpnrkt547k; RETENTION_COOKIES_NAME=29b11b75cea24d9684c8529313af4e73:6_cOlskH-rmZ-jHToNDIH4nXy2Y; sessionId=98df7d68d10a4c61a73bcfd3c792a482:XOFCB3iVQJ3LQjyQOS4WYcj-amU; UNIQ_SESSION_ID=28d5026d91de482f902879e69453c9a2:P3JmjQd6bv9UWnVaBOz7bEswgDo; auto-definition-region=false; _sa=SA1.804e8be3-3667-46f6-9142-ad1e3d221a8d.1596657654; SESSION=ba75fa55-4d77-44e5-87c4-128615acab4f; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%220c5b2444-70a0-4932-980c-b4dc0d3f02b5%22}%2C%22isAutoResolved%22:true}; currentLocalityGuid=9460fbc2-5e19-4fd2-bc0b-70a61bc1199c; currentSubDomain=tyumen; regionName=9460fbc2-5e19-4fd2-bc0b-70a61bc1199c:%D0%A2%D1%8E%D0%BC%D0%B5%D0%BD%D1%8C; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; mobile-region-shown=1; qrator_jsid=1596657653.781.oqUsW7jmnBPMeRgR-j3tfo55v8mj5936i0fuiks4j34138o0u; currentRegionGuid=dd883c15-4164-45c7-91fc-2a9381b5563b",
"Host": "tyumen.domclick.ru",
"If-None-Match": "W/27884-ViWJcxcnePeISH+oa//Lk59K5ng",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'domclick_v1.middlewares.DomclickV1SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'domclick_v1.middlewares.DomclickV1DownloaderMiddleware': 543,
#}
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
#" Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'domclick_v1.pipelines.DomclickV1Pipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
