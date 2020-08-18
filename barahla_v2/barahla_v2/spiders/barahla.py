# -*- coding: utf-8 -*-
import csv
import re
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
from services import get_cord


class BarahlaSpider(scrapy.Spider):
    name = 'barahla'
    allowed_domains = ['barahla.net']
    urls_pool = ['https://tyumen.barahla.net/realty/217/', 'https://tyumen.barahla.net/realty/208/','https://tyumen.barahla.net/realty/216/']
    start_urls = ['https://tyumen.barahla.net/realty/217/']

    def parse(self, response):
        cards = response.css('.ads')
        page_index = self.urls_pool.index(response.url)
        city = 0
        for card in cards:
            house_id, price, time_to_create, title, title_image, title_link = self.parse_card_data(card, city, response)
            if self.check_db(house_id):
                yield ({
                    'mode': 0,
                    'title': title,
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
                yield scrapy.Request(url=title_link, callback=self.parse_info)
            else:
                print('This row is already exist')

        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)
    def parse_card_data(self, card, city, response):
        title = card.css('p.title > a::text').get().replace('  ', '')
        title_link = card.css('p.title > a::attr(href)').get().replace('  ', '')
        house_id = card.css('p.title > a::attr(href)').get().replace('  ', '').split("/")[-1].split('_')[0].replace(
            '.html', '')
        reg = re.compile('[^0-9]')
        if card.css('span.price > strong::text').get():
            print(card.css('span.price > strong::text').get())
            price = int(reg.sub('', card.css('span.price > strong::text').get()))
        else:
            price = 0
        title_image = card.css('.advert_image_block > a > img::attr(src)').get()
        time_to_create = card.css('.right-side > p::text').get()
        print('------------------------------------------\n')
        for url in self.start_urls:
            if url == response.url:
                print('This is city')
                self.start_urls.index(url)
        print(city)
        return house_id, price, time_to_create, title, title_image, title_link

    def check_db(self, house_id_val):
        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            return False
        else:
            return True

    def parse_info(self, response):
        yield from self.parse_info_data(response)
        # print('Start parse next page')

    def parse_info_data(self, response):
        # print(f'processing: {response.url}')
        type_of_participation = official_builder = name_of_build = decoration = floor = floor_count = house_type = \
            num_of_rooms = total_area = living_area = kitchen_area = deadline = land_area = ' '
        images = []
        # print('Start parse basic info...')
        h = response.url.replace('  ', '').split("/")[-1].split('_')[0].replace('.html', '')
        address = response.css('p.adress > span::text').get()
        user_id = response.css('.user-item-container::attr(data-user-id)').get()
        # print('Parsing house params...')
        if address:
            address = 'Тюмень, ' + address
            y_cords, x_cord, address = get_cord(address)
        else:
            x_cord = y_cords = None
            address = ''
        # print(f'Address: {address}')
        for label in response.css('div > span'):
            if isinstance(label.css('::text').get(),str):
                if label.css('::text').get().find('Общая площадь:') > 0:
                    if label.css('strong::text').get().find('сот.')> 0:
                        land_area = re.sub(r'кв.м.| | .', '', label.css('strong::text').get())
                    else:
                        total_area = re.sub(r'сот.| | .', '', label.css('strong::text').get())
        for param in response.css('div > span > strong::text').getall():
            new_param = re.sub(r'[\n ]', '', param)

            if param.index == 2:
                total_area = re.sub(r'кв.м.| | .', '', new_param)
                type_ = 'Вторичка'
            if param.index == 3:
                if int(new_param) > 5:
                    num_of_rooms = f'5к+ {new_param}'
                else:
                    num_of_rooms = f"{new_param}"
        if response.url.find('doma-kottedzhi-dachi') >= 0:
            type_ = 'Коттеджи'
        elif response.url.find('kvartiry-i-komnaty') >= 0:
            type_ = 'Вторичка'
        else:
            type_ = 'Участки'
        data = response.css('p.px18::text').get()
        phone = ''
        print('Parsing images...')
        for img in response.css('img.zoomable::attr(src)').getall():
            images.append(img)
        yield {
            'mode': 1,
            'user_id': user_id,
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
            'land_area' : land_area,
            "deadline": deadline,
            'phone': phone,
            'images': images,
            'data': data,
            'address': address,
            'cords': [x_cord, y_cords],
            'type':  type_
        }
