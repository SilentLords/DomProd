# -*- coding: utf-8 -*-
import re

import scrapy
from inline_requests import inline_requests
from .services import get_cord


class InfoV1Spider(scrapy.Spider):
    all_json_data = []
    links = []
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    phone = ''
    id_house = 0
    max_params_len = 0
    max_params = []

    def start_requests(self):
        with open('links.csv') as f:
            self.links = f.read().splitlines()
            yield scrapy.Request(url=self.links[0], callback=self.parse)

    name = 'info_v1'
    allowed_domains = ['barahla.net']

    @inline_requests
    def parse(self, response):
        print(f'processing: {response.url}')
        type_of_participation = official_builder = name_of_build = decoration = floor = floor_count = house_type = \
            num_of_rooms = total_area = living_area = kitchen_area = deadline = ' '
        images = []
        print('Start parse basic info...')
        h = response.url.replace('  ', '').split("/")[-1].split('_')[0].replace('.html', '')
        address = response.css('p.adress > span::text').get()
        user_id = response.css('.user-item-container::attr(data-user-id)').get()
        print('Parsing house params...')
        if address:
            address = 'Тюмень, ' + address
            y_cords, x_cord = get_cord(address)
        else:
            x_cord = y_cords = None
            address = ''
        for param in response.css('div > span > strong::text').getall():
            new_param = re.sub(r'[\n ]', '', param)
            if param.index == 2:
                total_area = re.sub(r'кв.м.| | .', '', new_param)
            if param.index == 3:
                if int(new_param) > 5:
                    num_of_rooms = f'5к+ {new_param}'
                else:
                    num_of_rooms = f"{new_param}"
        print(f'Parsing data and phone number with user_id: {user_id}')

        data = response.css('p.px18::text').get()
        request = yield scrapy.Request(
            url=f'https://tyumen.barahla.net/ajax/get_contacts/?id={user_id}', dont_filter=True)
        phone = request.css('span::text').get()
        if phone.find(','):
            phone = re.sub(r'[\\n   \" }]', '', phone.split(',')[0])
        print(phone, h)
        print('Parsing images...')

        for img in response.css('img.zoomable::attr(src)').getall():
            images.append(img)
        yield {
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
            'address': address,
            'cords': [x_cord, y_cords],
            'type': 'Вторичка'}
        print('Start parse next page')

        self.id_house += 1
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            print('save')
