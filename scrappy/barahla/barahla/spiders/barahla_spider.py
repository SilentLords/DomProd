# -*- coding: utf-8 -*-
import csv

import scrapy

import os
import sys
import django
DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'

django.setup()
from apps.base.models import HouseModel, HouseInfo, Image


class BarahlaSpider(scrapy.Spider):
    link_pool = []
    name = 'barahla_spider'
    allowed_domains = ['barahla.net']
    start_urls = ['https://tyumen.barahla.net/realty/217/']

    def parse(self, response):
        cards = response.css('.ads')
        city = 0
        for card in cards:
            title = card.css('p.title > a::text').get().replace('  ', '')
            title_link = card.css('p.title > a::attr(href)').get().replace('  ', '')
            house_id = card.css('p.title > a::attr(href)').get().replace('  ', '').split("/")[-1].split('_')[0].replace(
                    '.html', '')
            price = int(card.css('span.price > strong::text').get().replace('  ', ''))
            title_image = card.css('.advert_image_block > a > img::attr(src)').get()
            time_to_create = card.css('.right-side > p::text').get()
            print('------------------------------------------\n')
            for url in self.start_urls:
                if url == response.url:
                    print('This is city')
                    self.start_urls.index(url)
            print(city)
            if self.check_db(house_id):
                self.link_pool.append(title_link)
                yield ({'title': title,
                        "link": title_link,
                        "house_id": house_id,
                        "price": price,
                        "img": title_image,
                        'address': '',
                        'data': '',
                        'time_created': time_to_create,
                        'host': self.allowed_domains[0],
                        'city': city,
                        'type': 'Вторичка'
                        })
            else:
                print('This row is already exist')
        self.save()

    def check_db(self, house_id_val):
        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            return False
        else:
            return True

    def save(self):
        # print('save', self.link_pool)
        with open('../../info/info/spiders/links.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for link in self.link_pool:
                writer.writerow([link])
