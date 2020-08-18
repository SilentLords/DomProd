# -*- coding: utf-8 -*-

# Scrapy settings for yandex_v2 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'yandex_v2'

SPIDER_MODULES = ['yandex_v2.spiders']
NEWSPIDER_MODULE = 'yandex_v2.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yandex_v2 (+http://www.yourdomain.com)'

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
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control": "max-age=0",
"Connection": "keep-alive",
"cookie": "rgid=566725; smart_banner_closed=1; splash_banner_closed=1; yuidss=3622032021587647719; ymex=1903007720.yrts.1587647720#1903007720.yrtsi.1587647720; mda=0; my=YwA=; gdpr=0; _ym_uid=1587799811189713622; _ym_d=1588095961; yandexuid=3622032021587647719; amplitude_id_fbaa2666dc22e95808260dfd4e9bb80dyandex.ru=eyJkZXZpY2VJZCI6IjE4ZjhkZWJmLTM1YjEtNDM3YS04NmY1LTQ1OWVjMzgxNjhhMlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU5MjY0OTUyOTg5NywibGFzdEV2ZW50VGltZSI6MTU5MjY1MDg3ODA4NCwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; _delighted_web={%22rDgJXH2PxcDyVP0X%22:{%22_delighted_fst%22:{%22t%22:%221592582436120%22}%2C%22_delighted_lst%22:{%22t%22:%221593536886839%22%2C%22m%22:{%22token%22:%22S4aBZJMeZz8Eg2LBQMKWM53M%22}}}}; TS015979f0=01f3111baf44b630f0c41d11e85704b9a0a9c429b634160f700c3dc0f0c7f5f186de25e22bc23f9ed5f6dd8004ac3793553af0af773f22d36208b20d8cd6806d88a6032936c14590ca260f01352a4fdd188c6c560b; yandex_gid=20669; skid=3277195321594745476; device_id='aa8cd199d5a57e1292e924bf5c9157425fe5f3a6f'; active-browser-timestamp=1596021836208; _ym_isad=2; Session_id=3:1596485161.5.1.1588095815065:qIYrBQ:26.1|352473087.-1.2.1:63618759|1130000045665485.8389346.2.2:8389346|220903.792737.U5_3eD_t5LCk7BuNUqHUZQMn2hg; sessionid2=3:1596485161.5.1.1588095815065:qIYrBQ:26.1|352473087.-1.2.1:63618759|1130000045665485.8389346.2.2:8389346|220903.287447.6Fx_1hF4BxYVAyu8KHJAuJoj9n0; L=eCxgcUhrS158cnZSY3h8TgR4UQ0BRWB+BwUABV4BHD4lNBM/PRoHVDgS.1596485161.14316.337512.ae36530ac757736ca4f0376641015f09; yandex_login=admin@domafound.ru; i=mnhccwRUk2LVIntRXkt61p/aWY/4Lq397PY/D0f0ugM34W710p4wX8pdW6kUb92vX8R66OTWZc1pTjo8cz0X0Of58No=; _csrf_token=7ab3ad4f68383073d8b586a4e4ea6324d669e6256244d2b8; suid=0b0e71c5b8501f6735a67c297facd4bb.06ddb30668e69bbddc3ba961c60233a9; font_loaded=YSv1; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; rgid=566725; yp=1626281242.ygu.1#1911845161.udn.cDphZG1pbkBkb21hZm91bmQucnU%3D#1596631373.szm.2:1680x1050:1639x981#1911845161.multib.1; X-Vertis-DC=myt; from=direct; BgeeyNoBJuyII=1; splash_banner_closed=1; BgeeyNoBJuyII=1; _ym_visorc_21930706=w; yabs-frequency=/5/6G0n0FGZAL_nrG5V/q_ToS9G0001mF240/; spravka=dD0xNTk2NTMzMDAxO2k9MTc4LjQ2LjEwMy4xNzg7dT0xNTk2NTMzMDAxNzE2MTYxMjYzO2g9ZmEyOWY5ZTI0NGI4ZDljYWE3OGVmZmIxMTQ5ZjZlOWY=; ys=udn.cDphZG1pbkBkb21hZm91bmQucnU%3D#ymrefl.560B802789A10EBA#wprid.1596532817388684-427564253068484022730491-prestable-app-host-sas-web-yp-39#c_chck.1359661563; smart_banner_closed=1; prev_uaas_data=3622032021587647719%23256346%23249664%23227540%23220600%23254621%23250897%23245498%23233395%23244763%23239041%23241487%23241661%23229282%23213159%23262005%23255349%23215859; prev_uaas_expcrypted=ivoLly1n67Ojp2dgvoyX0ietrgkF6izY-spB69GWukqS4y49ZKc-dCMtUUc2Y2WgM0e_G5VEuknBfi9Z-R7prj_cHjfSAjI-DNAEQ9iikQnRLElSj0FOD9QVzeojFJE83LN8Q7aJeQRrgGWxQp2N-JRuEvG7FLi49NBWeKDVx8l6HjFiHBaluA0QxdlTq4fMrNGKzordSgcutgsLvq9tcG_vVSFJAkgSV3odX0fTR61QkT_xHMu-sMCQaRC_T-vhY4TH7-WflOfxHYN1I1EALQ%2C%2C; from_lifetime=1596533533052",
"Host": "realty.yandex.ru",
"User-Agent": "'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'yandex_v2.middlewares.YandexV2SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'yandex_v2.middlewares.YandexV2DownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'yandex_v2.pipelines.YandexV2Pipeline': 300,
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
