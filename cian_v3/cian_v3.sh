export http_proxy="http://v1xut92y:gstagemp@foxy.ltespace.com:10872"
export https_proxy="https://v1xut92y:gstagemp@foxy.ltespace.com:10872"
. /var/www/dom/env/bin/activate
cd /var/www/dom/src/cian_v3/cian_v3/spiders/
scrapy crawl cian -L WARNING
