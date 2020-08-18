#!/bin/bash
export http_proxy="http://Selmrniki002:T2d2DiW@50.114.84.109:45785"
export https_proxy="https://Selmrniki002:T2d2DiW@50.114.84.109:45785"
. /var/www/dom/env/bin/activate
cd /var/www/dom/src/scrappy/avito_parser/avito/avito/spiders/
scrapy crawl avito -L WARNING
cd /var/www/dom/src/scrappy/avito_parser/info/info/spiders/
scrapy crawl info_v1 -L WARNING
