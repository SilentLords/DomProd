# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import csv
import re

import scrapy

import os
import sys
import django

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = r'C:/Users/nick/PycharmProjects/Domafound/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'

django.setup()
from apps.base.models import HouseModel, CITY_CHOICES
from services import get_cord


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


def correct_house_id(url):
    url = url.split('/')[-1].split('-')[0]
    house_id = re.sub(r'[^0-9]', '', url)
    if len(house_id) > 10:
        return int(house_id) % 10000000, False
    else:
        return int(house_id), False


class MultilistingSpider(scrapy.Spider):
    name = 'multilisting'
    allowed_domains = ['multilisting.su']
    start_urls = [
        'https://multilisting.su/g-tyumen/sale-flat/from-owner']
    urls_pool = [
        'https://multilisting.su/g-tyumen/sale-flat/from-owner','https://multilisting.su/g-tyumen/sale-house/from-owner','https://multilisting.su/g-tyumen/sale-land-lot?advertisement[owner]=1']
    types = ['Вторичка', 'Коттеджи', 'Участки']
    def parse(self, response):
        page_index = self.urls_pool.index(response.url)
        cards = response.css('.media.clearfix.object')
        type_ = self.types[self.urls_pool.index(response.url)]
        for card in cards:
            if card.css('.yandex_adfox_action'):
                cards.pop(cards.index(card))
        for card in cards:
            if cards.index(card) < 5:
                city = 0
                url = response.urljoin(card.css('.header_adv_short::attr(href)').get())
                house_id = card.css('::attr(element_id)').get()
                title_image = card.css('.object__gallery').css('img::attr(src)').get()
                title = card.css('.header_adv_short::text').get()
                price = card.css('span.formatRub::text').get()
                if 0 <= page_index < 3:
                    city = 0
                address = CITY_CHOICES[city][1] + " " + ' '.join(card.css('.text-location > a::text').getall())
                x_cord, y_cord, address = get_cord(address)
                yield ({
                    'mode': 0,
                    'house_id': int(house_id),
                    "link": url,
                    "title": title,
                    "price": price,
                    'address': address,
                    "img": title_image,
                    'time_created': '',
                    'data': '',
                    'host': self.allowed_domains[0],
                    'city': city,
                    'cords': [x_cord, y_cord],
                    'type': type_
                })
                yield scrapy.Request(url=url, callback=self.parse_info)
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def parse_info(self, response):
        house_id = re.sub(r'[^0-9]', '', response.css('span.small.text-muted::text').get())
        floor = floor_count = total_area = land_area = 0
        house_type = num_of_rooms = ''
        for item in response.css('ul.list-unstyled > li'):
            if item.css('::text').get() == 'этаж: ':
                floor = item.css('span::text').get()
            if item.css('::text').get() == 'этажей: ':
                floor_count = item.css('span::text').get()
            if item.css('::text').get() == 'площадь: ':
                total_area = item.css('span::text').get()
            if item.css('::text').get() == 'тип дома: ':
                house_type = item.css('span::text').get()
            if item.css('::text').get() == 'комнат: ':
                num_of_rooms = item.css('span::text').get()
            if item.css('::text').get() == 'площадь участка: ':
                land_area = item.css('span::text').get()
        if num_of_rooms != '':
            if int(num_of_rooms) >= 5:
                num_of_rooms = f'5к+ {num_of_rooms}'
            else:
                num_of_rooms = f'{num_of_rooms}к'
        data = response.css('.row').css('p::text').get()
        yield ({
            'mode': 1,
            'house_id': house_id,
            'type_of_participation': '',
            'official_builder': '',
            'name_of_build': '',
            'decoration': '',
            "floor": floor,
            "floor_count": floor_count,
            "house_type": house_type,
            "num_of_rooms": num_of_rooms,
            "total_area": float(total_area),
            "living_area": 0,
            "kitchen_area": 0,
            'land_area': float(land_area),
            "deadline": 0,
            'phone': '0',
            'images': response.css('.extendedFotoramaAction').css('img::attr(src)').getall() ,
            'data': data})

