# -*- coding: utf-8 -*-
import scrapy
from time import sleep


class InfoV1Spider(scrapy.Spider):
    name = 'info_v1'
    allowed_domains = ['cian.ru']
    id_house = 0

    def start_requests(self):
        with open('links.csv') as f:
            self.links = f.read().splitlines()
            yield scrapy.Request(url=self.links[0], callback=self.parse)

    def parse(self, response):
        type_of_participation = official_builder = name_of_build = decoration = floor = floor_count = house_type = \
            num_of_rooms = total_area = living_area = kitchen_area = deadline = ' '
        images = []
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
            'type': _type})
        self.id_house += 1
        sleep(3)
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            print('save')
