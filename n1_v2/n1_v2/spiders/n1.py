# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys

import scrapy

DEBUG = True
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/DomProd/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from apps.base.models import HouseModel, HouseInfo, Image
from services import get_cord


def correct_house_id(url):
    house_id = re.sub(r'[^0-9]', '', re.sub(r'/|\?osale2|\?osale1| ', '', url.split('ru')[-1]))
    if len(house_id) > 10:
        return int(house_id) % 10000000
    else:
        return int(house_id)


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


class N1Spider(scrapy.Spider):
    name = 'n1'
    allowed_domains = ['n1.ru']
    start_urls = ['https://tumen.n1.ru/kupit/kvartiry/?sort=-date&limit=50&author=owner']
    urls_pool = ['https://tumen.n1.ru/kupit/kvartiry/?sort=-date&limit=50&author=owner',
                 'https://tumen.n1.ru/kupit/doma/?sort=-date&author=owner',
                 'https://tumen.n1.ru/kupit/zemlya/?sort=-date&author=owner']
    max_params_len = 0
    max_params = []

    def parse(self, response):
        if response.url == 'https://tumen.n1.ru/kupit/zemlya/?sort=-date&author=owner':
            cards = response.css('.land-list-card')
        else:
            cards = response.css('.living-list-card')
        page_index = self.urls_pool.index(response.url)
        city = 0
        for card in cards:
            if cards.index(card) < 5:
                house_id = correct_house_id(card.css('a.link::attr(href)').get())
                if check_db(house_id):
                    link = yield from self.parse_card_info(card, city, house_id, page_index, response)
                    print(link)
                    yield scrapy.Request(url=link, callback=self.parse_info)
                else:
                    print('This House is already exist')
        if page_index < self.urls_pool.__len__() - 1:
            print(self.urls_pool[page_index + 1])
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def parse_info(self, response):
        house_id = correct_house_id(response.url)
        type_of_participation = official_builder = name_of_build = decoration = house_type = deadline = ' '
        images = []
        floor = floor_count = num_of_rooms = total_area = living_area = kitchen_area = land_area = 0
        if response.css('ol.breadcrumbs__list').css('span.ui-kit-link__inner > span::text').getall()[2] == 'Квартиры':
            type_ = response.css('ol.breadcrumbs__list').css('span.ui-kit-link__inner > span::text').getall()[3]
        else:
            type_ = response.css('ol.breadcrumbs__list').css('span.ui-kit-link__inner > span::text').getall()[2]
        print(type_)
        if type_ == 'Новостройки':
            num_of_rooms = response.css('.deal-title::text').get().split(' ')[1]

        if type_ == 'Вторичное жильё':
            type_ = 'Вторичка'
            num_of_rooms = response.css('.deal-title::text').get().split(' ')[1]

        if type_ == 'Дома, коттеджи':
            num_of_rooms = '0-к'
            type_ = 'Коттеджи'
        if type_ == 'Земля':
            num_of_rooms = '0-к'
            type_ = 'Участки'
        images_req = response.css('.media-container > a::attr(href)').getall()
        for image in images_req:
            images.append(image)
        num = response.css('a.offer-card-contacts-phones__phone::attr(href)').get().replace('tel:+', '')
        if type_ == 'Участки':
            params = response.css('li.card-land-content-params-list__item')
        else:
            params = response.css('li.card-living-content-params-list__item')
        par_list = []
        for par in params:
            par_list.append(par.css("span::text").getall())
        for item in par_list:
            print(item)
            if item[0] == "Общая площадь":
                total_area = float(re.sub(r',', '', re.sub(r'[^0-9]', '', item[1])))
            if item[0] == "Жилая площадь":
                living_area = float(re.sub(r',', '', re.sub(r'[^0-9]', '', item[1])))
            if item[0] == 'Этаж':
                floor = int(item[1].split(' из ')[0])
                floor_count = int(item[1].split(' из ')[1])
            if item[0] == 'Этажей':
                floor_count = int(item[1])
            if item[0] == 'Материал дома':
                house_type = item[1]
            if item[0] == 'Кухня':
                kitchen_area = float(re.sub(r',', '', re.sub(r'[^0-9]', '', item[1])))
            if item[0] == 'Комнат':
                num_of_rooms = item[1] + '-к'
            if item[0] == 'Площадь участка':
                land_area = float(re.sub(r',', '', re.sub(r'[^0-9]', '', item[1])))

        data = response.css('.foldable-description  > div::text').get()
        item = {
            'mode': 1,
            'type': type_,
            'house_id': house_id,
            'type_of_participation': type_of_participation,
            'official_builder': official_builder,
            'name_of_build': name_of_build,
            'decoration': decoration,
            "floor": floor,
            "floor_count": floor_count,
            "house_type": house_type,
            "num_of_rooms": num_of_rooms,
            "total_area": total_area,
            "living_area": living_area,
            "kitchen_area": kitchen_area,
            "deadline": deadline,
            'phone': num,
            'images': images,
            "data": data,
            'land_area': land_area
        }
        yield item
        print(item)
        print('######################################################\n')

    def parse_card_info(self, card, city, house_id, page_index, response):
        if card.css('.living-list-card-newbuilding'):
            type_ = 'Новостройки'
        else:
            type_ = 'Вторичка'
        if 0 <= page_index <= 3:
            city = 0
        link = response.urljoin(card.css('a.link::attr(href)').get())
        print(response.url.find('zemlya'))
        if response.url.find('zemlya') > -1:
            address = card.css('.land-list-card__district::text').get()
        else:
            try:
                if card.css('a.link > span::text').get().split(',') and (card.css(
                        '.living-list-card__inner-block::text').get() or card.css(
                    'span.living-list-card-city-with-estate__item::text').get()):
                    address = card.css('a.link > span::text').get().split(',')[1] + ' ' + \
                              card.css('a.link > span::text').get().split(',')[2] + ' ' + card.css(
                        '.living-list-card__inner-block::text').get() + ' ' + card.css(
                        'span.living-list-card-city-with-estate__item::text').get()
                else:
                    address = ''
            except:
                address = ''

            x_cord, y_cord, address = get_cord(address)
            if response.url.find('zemlya') > -1:
                price_class = '.land-list-card__price::attr(title)'
            else:
                price_class = '.living-list-card-price__item::text'
            yield ({
                'mode': 0,
                'type': type_,
                'house_id': house_id,
                "link": response.urljoin(card.css('a.link::attr(href)').get()),
                "title": card.css('a.link > span::text').get(),
                "price": re.sub(r'[^0-9]', '', card.css(price_class).get()),
                'address': address,
                "img": card.css('.offer-list-preview__item > img::attr(src)').get(),
                'time_created': '',
                'data': '',
                'host': 'tumen.n1.ru',
                'city': city,
                'cords': [x_cord, y_cord]
            })

        return link
