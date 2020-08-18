#!/bin/bash

unset http_proxy
unset https_proxy
. /var/www/dom/env/bin/activate

cd /var/www/dom/src/scrappy/barahla/barahla/spiders/
scrapy crawl barahla_spider -L WARNING
cd /var/www/dom/src/scrappy/barahla/info/info/spiders/
scrapy crawl info_v1 -L WARNING
