# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys
import scrapy
from inline_requests import inline_requests

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = 'C:/Users/nick/PycharmProjects/Domafound/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from services import get_cord

from apps.base.models import HouseModel, CITY_CHOICES


def correct_house_id(url):
    house_id = re.sub(r'[^1-9]', '', re.sub(r'/|\?osale2|\?osale1| ', '', url.split('-')[-1]))
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


class MailSpider(scrapy.Spider):
    name = 'mail'
    allowed_domains = ['tumn.realty.mail.ru']
    urls_pool = ['https://tumn.realty.mail.ru/sale/living/?sort=date&sort_direct=desc',
                 'https://tumn.realty.mail.ru/sale/country/?types%5B0%5D=12&types%5B1%5D=13&types%5B2%5D=14','https://tumn.realty.mail.ru/sale/country-plot/']
    start_urls = ['https://tumn.realty.mail.ru/sale/living/?sort=date&sort_direct=desc']
    link_pool = []

    def parse(self, response):
        # Получаем список всех объявлений
        cards = response.css('.p-instance')
        page_index = self.urls_pool.index(response.url)
        city = 0
        for card in cards:
            if cards.index(card) < 1:
                house_id = correct_house_id(card.css('a.p-instance__title::attr(href)').get())
                if check_db(house_id):
                    link = yield from self.parse_card_info(card, city, house_id, page_index, response)
                    yield scrapy.Request(url=link, callback=self.parse_info)
                else:
                    print('This house already exist')
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def parse_card_info(self, card, city, house_id, page_index, response):
        if 0 <= page_index <= 3:
            city = 0
        y_cord, x_cord, address = get_cord(
            ''.join(card.css('a.p-instance__title::text').get().split(',')[1:]))
        if response.css('.p-instance__param_color_green'):
            _type = 'Новостройки'
        else:
            _type = 'Вторичка'
        if response.url == 'https://tumn.realty.mail.ru/sale/country/?types%5B0%5D=12&types%5B1%5D=13&types%5B2%5D=14':
            _type = 'Коттеджи'
        if response.url == 'https://tumn.realty.mail.ru/sale/country-plot/':
            _type = 'Участки'
        yield ({
            'mode': 0,
            'house_id': int(house_id),
            "link": card.css('a.p-instance__title::attr(href)').get(),
            "title": card.css('a.p-instance__title::text').get(),
            "price": int(
                "".join([x for x in card.css('span.p-instance__title::text').get() if ord(x) < 128])),
            'address': address,
            "img": card.css('img.photo__pic::attr(src)').get(),
            'time_created': card.css('.p-instance__param.js-ago::attr(datetime)').get(),
            'data': '',
            'host': self.allowed_domains[0],
            'city': city,
            'cords': [x_cord, y_cord],
            'type': _type
        })
        return card.css('a.p-instance__title::attr(href)').get()

    def parse_info(self, response):
        Headers = {
            ':authority': 'tumn.realty.mail.ru',
            'cookie': 'mrcu=A8955EA69253407588504E942B05; b=zEcBAAAtNVcAAQAC; OTVET-8088=3; x_user_id=1667777051169219; SLG_GWPT_Show_Hide_tmp=1; SLG_wptGlobTipTmp=1; VID=2V8KCI0W1fnx00000Q0qD4Hx::335783053:0-0-3c76e58-3bbed27:CAASEEIYHaAds7qa9qeE4dlKoP0acHbNqsAP-6HLu39TLJYMKY0QsaCF54puPXyQC234dZfUKZUrbaR0qNGv9dm3n6AVCIQ_YSkfAoLnrci7bhKB8BV0bUmZYGIaRmeKJtECve0ZpuOprHD-kN1rGGjW9FF2XYwbpRlyIHQsL5pJnZUYRBw; act=01e5e698ddb14a8fa226f66fb2a428dc; i=AQBSs/BeCQATAAgTBp0AAWIBARoCAYwDAWcKAW0KAbsBCAQBAQABkwIIZyJuAAHFAAFwAQEBAgECAgEIAgEJAgENAgESAgEXAgFsAgFgBQFhBQFoBQF0BQF2BQGgBQGhBQGkBQGmBQGpBQEQBgF6BgHFCwHICwHJCwHMCwHNCwFwDQF0DQF4DQGGDQHXDQG5YwHcBAgEAQEAAeEECQEB4gQKBBACzwc6BQgWByoCAQgEAQkEAWsEAZoEAQsIAUYKAdYGCAQBAQABvQcIBAGZFQE=; p=ED0CANfX6QAA; Mpop=1592833093:535d7b4e4972497e1905000017031f051c054f6c5150445e05190401041d55565d5657564c56551e505358525b5847434b5044594a135f5950551f4b40:domafound.admenistrator@mail.ru:; t=obLD1AAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAACAAAcDrgcA; o=domafound.admenistrator@mail.ru:233:AA==.s; s=ww=1639|wh=981|dpr=2|rt=1|octavius=1; realty_geo=2021596',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.142',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline, land_area = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        images = []
        images_req = response.css('.grid__item::attr("data-original")').getall()
        for image in images_req:
            images.append(image)
        if response.css('.p-gallery-wrap > .js-module::attr(onclick)').get():
            num = response.css('.p-gallery-wrap > .js-module::attr(onclick)').get().split('phone_full":')[1].replace(
                '}}}}}}', '').replace('"', '')
        else:
            num = 00000000000
        par_list = []
        for item in response.css('.p-params__item'):
            par_list.append(
                [item.css('span.p-params__name::text').get(), item.css('span.p-params__value > span::text').getall()])
        for item in par_list:
            if item[0] == 'Комнат':
                num_of_rooms = item[1][0]
            if item[0] == 'Количество комнат к продаже':
                num_of_rooms = item[1][0]
            if item[0] == 'Этаж / Всего':
                floor = item[1][0].split('/')[0].replace(' ', '')
                floor_count = item[1][0].split('/')[1].replace(' ', '')
            if item[0].find('Площадь') > -1:
                for i in item[1]:
                    if i == 'общая':
                        total_area = item[1][item[1].index(i) - 1]
                    if i == 'жилая':
                        living_area = item[1][item[1].index(i) - 1]
                    if i == 'кухня':
                        kitchen_area = item[1][item[1].index(i) - 1]
                    if i == 'участок':
                        land_area = item[1][item[1].index(i) - 1]
            if item[0] == 'Этажность':
                floor_count = item[1][0]
            if item[0] == 'Тип дома':
                house_type = item[1][0]
        data = response.css(".toggle__item > div::text").get()
        house_id = correct_house_id(response.url)
        yield ({
            'mode': 1,
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
            'land_area': land_area,
            "deadline": deadline,
            'phone': num,
            'images': images,
            'data': data})
