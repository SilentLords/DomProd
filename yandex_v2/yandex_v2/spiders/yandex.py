# -*- coding: utf-8 -*-
import csv
import os
import re
import sys
import scrapy

DEBUG = True
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from services import get_cord

from apps.base.models import HouseModel, CITY_CHOICES


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


def correct_house_id(url):
    house_id = re.sub(r'[^1-9]', '', re.sub(r'/|\?osale2|\?osale1| ', '', url))
    if len(house_id) > 10:
        return int(house_id) % 10000000
    else:
        return int(house_id)


class YandexSpider(scrapy.Spider):
    name = 'yandex'
    allowed_domains = ['realty.yandex.ru']
    start_urls = ['https://realty.yandex.ru/tyumen/kupit/kvartira/bez-posrednikov/?sort=DATE_DESC']
    urls_pool = ['https://realty.yandex.ru/tyumen/kupit/kvartira/bez-posrednikov/?sort=DATE_DESC']

    def parse(self, response):
        cards = response.css('.OffersSerpItem')
        page_index = self.urls_pool.index(response.url)
        for card in cards:
            if cards.index(card) < 10:
                self.parse_card(card, response,page_index)

    def parse_card(self, card, response, page_index):
        city = 0
        link = response.urljoin(card.css('.SerpItemLink::attr(href)').get())
        house_id = correct_house_id(link)
        if check_db(house_id):
            print('NEW HOUSE!')
            if 0<= page_index <3:
                city = 0
            address = card.css('.OffersSerpItem__address::text').get()
            if not address.find(CITY_CHOICES[city][1]) > -1:
                address = CITY_CHOICES[city][1] + ' ' + address
            x_cord, y_cord, address = get_cord(address)
            price = re.sub('[^0-9]', '', card.css('.Price > span::text').get())
            title = card.css('h3.OffersSerpItem__title::text').get()
            print(x_cord,y_cord,address)
            yield ({
                'mode': 0,
                # 'type': type_,
                'house_id': house_id,
                "link": link,
                "title": title,
                "price": price,
                'address': address,
                "img": card.css('.offer-list-preview__item > img::attr(src)').get(),
                'time_created': '',
                'data': '',
                'host': self.allowed_domains[0],
                'city': city,
                'cords': [x_cord, y_cord]
            })
        else:
            print('This house is already exist')

