#!/bin/bash

export http_proxy="http://Selmrniki002:T2d2DiW@50.114.84.109:45785"
export https_proxy="https://Selmrniki002:T2d2DiW@50.114.84.109:45785"
. /var/www/dom/env/bin/activate

cd /var/www/dom/src/scrappy/cian/cian/spiders/
scrapy crawl cian_spider -L WARNING
cd /var/www/dom/src/scrappy/cian/info/info/spiders/
scrapy crawl info_v1 -L WARNING
