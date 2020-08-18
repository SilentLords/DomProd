# -*- coding: utf-8 -*-
import csv
import re

import scrapy

import os
import sys
import django
from .services import get_cord

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'

django.setup()
from apps.base.models import HouseModel


class CianSpiderSpider(scrapy.Spider):
    name = 'cian_spider'
    link_pool = []
    allowed_domains = ['cian.ru']
    start_urls = [
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=5024&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1']

    def parse(self, response):
        cards = response.css('._93444fe79c--card--_yguQ')
        print(cards)
        city = 0
        print('Processing...')
        for card in cards:
            title = card.css('a.c6e8ba5398--header--1fV2A > ::text').get()
            if title:
                pass
            else:
                title = card.css('.c6e8ba5398--subtitle--UTwbQ::text').get()
            link = card.css('a.c6e8ba5398--header--1fV2A::attr(href)').get()
            house_id = card.css('a.c6e8ba5398--header--1fV2A::attr(href)').get().split('/')[-2]
            address = card.css('.c6e8ba5398--address-links--1tfGW > span::attr(content)').get()
            price = re.sub(r'[ ₽]', '', card.css('.c6e8ba5398--header--1dF9r::text').get())
            time_created = card.css('.c6e8ba5398--absolute--9uFLj::text').get()
            title_image = card.css('img.c6e8ba5398--image--3ua1b::attr(src)').get()
            print('Parse info finish')
            if self.check_db(house_id):
                print('Database check completed')
                for url in self.start_urls:
                    if url == response.url:
                        city = self.start_urls.index(url)
                print(f'City index is: {city}')
                y_cord, x_cord = get_cord(address)
                print(f"House cords is: {x_cord}, {y_cord}")
                self.link_pool.append(link)
                yield ({'title': title,
                        "link": link,
                        "house_id": house_id,
                        "price": price,
                        "img": title_image,
                        'address': address,
                        'data': '',
                        'time_created': time_created,
                        'host': self.allowed_domains[0],
                        'city': city,
                        'type': '',
                        'cords': [x_cord, y_cord]
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
