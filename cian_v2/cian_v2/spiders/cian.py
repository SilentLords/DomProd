# -*- coding: utf-8 -*-
import csv
import re

import scrapy

import os
import sys
import django

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = r'/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'

django.setup()
from apps.base.models import HouseModel
from services import get_cord


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


def parse_info(card):
    title = card.css('a.c6e8ba5398--header--1fV2A > ::text').get()
    if title:
        pass
    else:
        title = card.css('.c6e8ba5398--subtitle--UTwbQ::text').get()
    link = card.css('a.c6e8ba5398--header--1fV2A::attr(href)').get()
    house_id = card.css('a.c6e8ba5398--header--1fV2A::attr(href)').get().split('/')[-2]
    address = card.css('.c6e8ba5398--address-links--1tfGW > span::attr(content)').get()
    price = re.sub(r'[^0-9]', '', card.css('.c6e8ba5398--header--1dF9r::text').get())
    time_created = card.css('.c6e8ba5398--absolute--9uFLj::text').get()
    title_image = card.css('img.c6e8ba5398--image--3ua1b::attr(src)').get()
    print('Parse info finish')
    return address, house_id, link, price, time_created, title, title_image


class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['cian.ru']
    start_urls = [
        'https://tyumen.cian.ru/kupit-kvartiru-bez-posrednikov/']
    urls_pool = [
        'https://tyumen.cian.ru/kupit-kvartiru-bez-posrednikov/',
        # 'https://tyumen.cian.ru/kupit-dom-bez-posrednikov/',
        'https://tyumen.cian.ru/kupit-zemelniy-uchastok-bez-posrednikov/']

    def parse(self, response):
        cards = response.css('._93444fe79c--card--_yguQ')
        page_index = self.urls_pool.index(response.url)

        city = 0
        print('Processing...')
        ob_params = {
            'max_ob': 1
        }
        for card in cards:
            if cards.index(card) < 1:
                address, house_id, link, price, time_created, title, title_image = parse_info(card)
                if check_db(house_id):
                    print('Database check completed')
                    if 0 <= page_index < 3:
                        city = 0
                    else:
                        city = 0
                    print(f'City index is: {city}')
                    y_cord, x_cord, address = get_cord(address)
                    print(f"House cords is: {x_cord}, {y_cord}")
                    yield ({'mode': 0,
                            'title': title,
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
                    yield scrapy.Request(url=link, callback=self.parse_info_of_card)
                else:
                    print('This row is already exist')
                if page_index < self.urls_pool.__len__() - 1:
                    yield scrapy.Request(url=self.urls_pool[page_index + 1], callback=self.parse)

    def parse_info_of_card(self, response):
        type_of_participation = official_builder = name_of_build = decoration = floor = floor_count = house_type = \
            num_of_rooms = total_area = living_area = kitchen_area = deadline = land_area = ' '
        images = []
        house_or_area = False
        print(response)
        h = response.url.split('/')[-2]
        _type = ''
        if response.css('a.a10a3f92e9--link--1t8n1 > h2::text').get():
            official_builder = response.css('a.a10a3f92e9--link--1t8n1 > h2::text').get()
        name_of_build = response.css('.a10a3f92e9--container--3dDSQ > div > span::text').get()
        for param in response.css('li.a10a3f92e9--item--_ipjK'):
            if param.css('span.a10a3f92e9--name--3bt8k::text').get() == 'Тип жилья':
                if param.css('span.a10a3f92e9--value--3Ftu5::text').get().find(' '):
                    if param.css('span.a10a3f92e9--value--3Ftu5::text').get().split(' ')[0] == 'Новостройка':
                        _type = 'Новостройки'
                    else:
                        _type = 'Вторичка'
            if param.css('span.a10a3f92e9--name--3bt8k::text').get() == 'Отделка':
                decoration = param.css('span.a10a3f92e9--value--3Ftu5::text').get()
        for param in response.css('a.a10a3f92e9--link--378yo > span::text').getall():
            if param == 'Продажа домов в Тюмени':
                _type = 'Коттеджи'
            if param == 'Продажа земельных участков в Тюмени':
                _type = 'Участки'
        for param in response.css('.a10a3f92e9--item--2Ig2y'):
            if param.css('.a10a3f92e9--name--22FM0::text').get() == 'Тип дома':
                house_type = param.css('.a10a3f92e9--value--38caj::text').get()
        for param in response.css('.a10a3f92e9--info--3XiXi'):
            print(param.css('.a10a3f92e9--info-title--2bXM9::text').get())
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Общая':
                total_area = param.css('.a10a3f92e9--info-value--18c8R::text').get()
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Жилая':
                living_area = param.css('.a10a3f92e9--info-value--18c8R::text').get()
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Кухня':
                kitchen_area = param.css('.a10a3f92e9--info-value--18c8R::text').get()
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Этаж':
                floor = int(param.css('.a10a3f92e9--info-value--18c8R::text').get().split(' из ')[0])
                floor_count = int(param.css('.a10a3f92e9--info-value--18c8R::text').get().split(' из ')[1])
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Срок сдачи':
                deadline = param.css('.a10a3f92e9--info-value--18c8R::text').get()
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Участок':
                house_or_area = True
                land_area = param.css('.a10a3f92e9--info-value--18c8R::text').get()
            if param.css('.a10a3f92e9--info-title--2bXM9::text').get() == 'Площадь':
                house_or_area = True
                land_area = param.css('.a10a3f92e9--info-value--18c8R::text').get()
        if house_or_area:
            pass
        else:
            if response.css('h1.a10a3f92e9--title--2Widg::text').get().split(',')[0] == 'Студия' or \
                    response.css('h1.a10a3f92e9--title--2Widg::text').get().split(',')[
                        0] == 'Апартаменты свободной планировки':
                num_of_rooms = 'студии'
            else:
                room_count = int(response.css('h1.a10a3f92e9--title--2Widg::text').get().split(',')[0].split('-')[0])
                if room_count > 5:
                    num_of_rooms = f'5к+ {room_count}'
                else:
                    num_of_rooms = f'{room_count}к'
        phone = response.css('a.a10a3f92e9--phone--3XYRR::text').get().replace(' ', '')
        # if response.css('span.a10a3f92e9--value--3Ftu5::text').get().find(' '):
        #     if response.css('span.a10a3f92e9--value--3Ftu5::text').get().split(' ')[0] == 'Новостройка':
        for image in response.css('img.fotorama__img::attr(src)').getall():
            images.append(image)
        data = response.css('p.a10a3f92e9--description-text--3Sal4::text').get()
        yield ({
            'mode': 1,
            'house_id': h,
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
            'phone': phone,
            'images': images,
            'data': data,
            'type': _type,
            'land_area': land_area})
