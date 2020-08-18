#!/bin/bash

unset http_proxy
unset https_proxy
. /var/www/dom/env/bin/activate

cd /var/www/dom/src/scrappy/mail/mail/spiders/
scrapy crawl mail_spider -L WARNING
cd /var/www/dom/src/scrappy/mail/info/info/spiders/
scrapy crawl info_v1 -L WARNING
