export http_proxy="http://v1xut92y:gstagemp@foxy.ltespace.com:10872"
export https_proxy="https://v1xut92y:gstagemp@foxy.ltespace.com:10872"
. /var/www/dom/env/bin/activate
cd /var/www/dom/src/avito_v2/avito_v2/spiders/
scrapy crawl avito -L WARNING
