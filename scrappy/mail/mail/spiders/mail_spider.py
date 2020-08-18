# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys
from .services import get_cord
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

from apps.base.models import HouseModel, CITY_CHOICES


class MailSpider(scrapy.Spider):
    name = 'mail_spider'
    allowed_domains = ['tumn.realty.mail.ru']
    start_urls = ['https://tumn.realty.mail.ru/sale/living/?sort=date&sort_direct=desc']
    link_pool = []

    def parse(self, response):
        cards = response.css('.p-instance')
        city = 0
        for card in cards:
            if self.check_db(
                    card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', '').replace('?osale2',
                                                                                                              '').replace(
                        '?osale1', '')):
                self.link_pool.append(card.css('a.p-instance__title::attr(href)').get())
            if card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', '').replace('?osale2',
                                                                                                         '').replace(
                '?osale1', '').__len__() > 10:
                h = int(
                    card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', '').replace('?osale2',
                                                                                                              '').replace(
                        '?osale1', '')) % 10000000
            else:
                h = int(
                    card.css('a.p-instance__title::attr(href)').get().split('-')[-1].replace('/', '').replace('?osale2',
                                                                                                              '').replace(
                        '?osale1', ''))
            for url in self.start_urls:
                if url == response.url:
                    city = CITY_CHOICES[self.start_urls.index(url)][0]
            address = ''.join(card.css('a.p-instance__title::text').get().split(',')[1:])
            if response.css('.p-instance__param_color_green'):
                _type = 'Новостройки'
            else:
                _type = 'Вторичка'
            if address.find(CITY_CHOICES[city][1]) == -1:
                address = 'г.' + CITY_CHOICES[city][1] + address
            print(address)
            y_cord, x_cord = get_cord(address)
            yield ({
                'house_id': int(h),
                "link": card.css('a.p-instance__title::attr(href)').get(),
                "title": card.css('a.p-instance__title::text').get(),
                "price": int("".join([x for x in card.css('span.p-instance__title::text').get() if ord(x) < 128])),
                'address': address,
                "img": card.css('img.photo__pic::attr(src)').get(),
                'time_created': card.css('.p-instance__param.js-ago::attr(datetime)').get(),
                'data': '',
                'host': self.allowed_domains[0],
                'city': city,
                'cords': [x_cord, y_cord],
                'type': _type
            })
            print('-----------------------------------------------\n')
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
