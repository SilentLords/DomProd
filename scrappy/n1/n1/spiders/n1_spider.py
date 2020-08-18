# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys

import scrapy
DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from apps.base.models import HouseModel, HouseInfo, Image

class N1SpiderSpider(scrapy.Spider):
    name = 'n1_spider'
    allowed_domains = ['n1.ru']
    start_urls = ['https://tumen.n1.ru/kupit/kvartiry/?sort=-date&limit=50']
    link_pool = []


    def parse(self, response):
        cards = response.css('.living-list-card')
        city = 0
        for card in cards:
            if self.check_db(card.css('a.link::attr(href)').get().split('w/')[1].replace('/', '')):
                self.link_pool.append(response.urljoin(card.css('a.link::attr(href)').get()))
            if card.css('a.link::attr(href)').get().split('w/')[1].replace('/', '').__len__()>10:
                h = int(card.css('a.link::attr(href)').get().split('w/')[1].replace('/', '')) // 10000000
            else:
                h = int(card.css('a.link::attr(href)').get().split('w/')[1].replace('/', ''))
            if card.css('.living-list-card-newbuilding'):
                type_ = 'Новостройки'
            else:
                type_ = 'Вторичка'
            for url in self.start_urls:
                if url == response.url:
                    city = self.start_urls.index(url)
            yield ({
                'type': type_,
                'house_id': h,
                "link": response.urljoin(card.css('a.link::attr(href)').get()),
                "title": card.css('a.link > span::text').get(),
                "price": card.css('.living-list-card-price__item::text').get().replace(' ', ''),
                'address': card.css('a.link > span::text').get().split(',')[1] + ' ' +
                           card.css('a.link > span::text').get().split(',')[2] + ' ' + card.css(
                    '.living-list-card__inner-block::text').get() + ' ' + card.css(
                    'span.living-list-card-city-with-estate__item::text').get(),
                "img": card.css('.offer-list-preview__item > img::attr(src)').get(),
                'time_created': '',
                'data': '',
                'host': 'tumen.n1.ru',
                'city': city
            })
            # print(card.css('.offer-list-preview__item > img::attr(src)').get())
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
