#!/bin/bash
. /var/www/dom/env/bin/activate
cd /var/www/dom/src/scrappy/n1/n1/spiders/
scrapy crawl n1_spider -L WARNING
cd /var/www/dom/src/scrappy/n1/info/info/spiders/
scrapy crawl info_v1 -L WARNING
