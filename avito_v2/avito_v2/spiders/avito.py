# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys
from time import sleep

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


def correct_price(text):
    return re.sub(r'\n|₽| ', '', text)


from apps.base.models import HouseModel, CITY_CHOICES


class AvitoSpider(scrapy.Spider):
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    name = 'avito'
    allowed_domains = ['avito.ru']
    urls_pool = ['https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&proprofile=1&f=ASgBAQICAUSSA8YQAUCQvg0Ulq41',
                 'https://www.avito.ru/tyumen/doma_dachi_kottedzhi?cd=1&s=104&user=1&proprofile=1']
    start_urls = ['https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&proprofile=1&f=ASgBAQICAUSSA8YQAUCQvg0Ulq41']

    def parse(self, response):
        city = 0
        page_index = self.urls_pool.index(response.url)
        print("processing: " + response.url)
        products = response.css('.item__line')
        i = 0
        ob_params = {
            'max_ob': 6
        }
        for item in products:
            if i < ob_params['max_ob']:
                if item.css('span.snippet-tag'):
                    pass
                else:
                    parse_info, link = yield from self.parse_card(item, page_index, response)
                    if parse_info:
                        yield scrapy.Request(url=link, callback=self.parse_info)
                    else:
                        print('This House already exist',self.get_house_id( item.css('a.snippet-link::attr(href)').get()))
                    i += 1
        if page_index < self.urls_pool.__len__() - 1:
            print(page_index, self.urls_pool[page_index + 1])
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def parse_card(self, item, page_index, response):
        data = ''
        if item.css('span.item-address-georeferences').get():
            geo = item.css(
                'span.item-address-georeferences-item__content::text').get()
        else:
            geo = ''
        url = item.css('a.snippet-link::attr(href)').get()
        h_id = self.get_house_id(url)
        if 0 <= page_index < 3:
            city = 0
        else:
            city = 0
        full_address = CITY_CHOICES[city][1] + item.css('span.item-address__string::text').get() + ' ' + geo
        y_cord, x_cord, full_address = get_cord(address=full_address)
        link = response.urljoin(item.css('h3.snippet-title > a.snippet-link::attr(href)').get())
        print(item.css('h3.snippet-title >a > span::text').get())
        if self.check_db(h_id):
            yield {
                'mode': 0,
                'house_id': h_id,
                'img': item.css('img.large-picture-img::attr(src)').get(),
                'title': item.css('h3.snippet-title >a > span::text').get(),
                'link': link,
                'price': int(correct_price(item.css('span.snippet-price::text').get())),
                'address': full_address,
                'data': data,
                'time_created': item.css('div.snippet-date-info::text').get(),
                'host': self.allowed_domains[0],
                'city': city,
                'cords': [x_cord, y_cord]
            }
            a = True
            return a, link
        else:
            a = False

            return a, link

    def check_db(self, house_id_val):
        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            return False
        else:
            return True

    def parse_info(self, response):
        Headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',

        # req = yield scrapy.Request(
        #     url=f'https://m.avito.ru/api/1/items/{response.url.split("._")[1]}/phone/?key={self.key}',
        #     headers=Headers)
        # print(req)
        # num = req.body.decode("utf-8").split('2B')[1].replace('"}}}', '')
        num = 0
        url = response.url
        h_id = self.get_house_id(url)
        images = []
        land_area = 0
        # print(response.url)
        h_id = yield from self.parse_house_info(Headers, deadline, decoration, floor, floor_count, h_id, house_type,
                                                images, kitchen_area, land_area, living_area, name_of_build, num,
                                                num_of_rooms, official_builder, response, total_area,
                                                type_of_participation, url)
        print(h_id)

    def parse_house_info(self, Headers, deadline, decoration, floor, floor_count, h_id, house_type, images,
                         kitchen_area, land_area, living_area, name_of_build, num, num_of_rooms, official_builder,
                         response, total_area, type_of_participation, url):
        if url.find('kvartiry') > 0:
            print('Квартиры')
            images_req = response.css('.gallery-img-frame')
            for image in images_req:
                images.append('https://' + image.css('::attr(data-url)').get().replace('//', ''))
            if response.css('.item-description-text > p'):
                print('Base text')
                data_set = response.css('.item-description-text > p::text').getall()
            if response.css('.item-description-html > p'):
                print('html text')
                data_set = response.css('.item-description-html > p::text').getall()
            elif response.css('.item-description-html::text'):
                data_set = response.css('.item-description-html::text').getall()
            data = ' '.join(data_set)
            type_ = response.css('.breadcrumbs > span > a > span::text').getall()[-1]
            print(type_)
            for info_colum in response.css('li.item-params-list-item'):

                re_Info = info_colum
                try:
                    re_Info = re.sub(r' |</li>', '', re_Info.extract().split(' </span>')[1])
                except:
                    re_Info = re.sub(r' |</li>', '', re_Info.extract().split('</span>')[0])
                info_colum = info_colum.css('span.item-params-label::text').get()
                # print(re.search(r'в доме', info_colum), re_Info)
                if re.search(r'Тип участия', info_colum):
                    type_of_participation = re_Info
                if re.search(r'Официальный застройщик', info_colum):
                    # print(re_Info)
                    official_builder = re_Info
                if re.search(r'Название новостройки', info_colum):
                    name_of_build = re_Info
                if re.search(r'Отделка', info_colum):
                    decoration = re_Info
                if re.search(r'Этаж:', info_colum):
                    floor = re_Info.split('из')[0]
                    floor_count = re_Info.split('из')[1]
                if re.search(r'Тип дома', info_colum):
                    house_type = re_Info
                if re.search(r'Количество комнат', info_colum):
                    num_of_rooms = re_Info
                if re.search(r'Общая площадь', info_colum):
                    total_area = re_Info
                if re.search(r'Жилая площадь', info_colum):
                    living_area = re_Info
                if re.search(r'Площадь кухни', info_colum):
                    kitchen_area = re_Info
                if re.search(r'Площадь участка', info_colum):
                    deadline = re_Info
            if url.split("._").__len__() > 2:
                h_id = response.url.split("._")[2]
            else:
                h_id = response.url.split("._")[1]
            yield {
                'type': type_,
                'house_id': h_id,
                'mode': 1,
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
                'images': images,
                'data': data,
                'headers': Headers}
        else:
            print('Дачи')
            type_ = 'Коттеджи'
            if url.split("._").__len__() > 2:
                h_id = re.sub(r'[^0-9]', '', url.split("._")[2])
            else:
                if url.split("._").__len__() == 1:
                    h_id = re.sub(r'[^0-9]', '', url.split("_")[-1])
                else:
                    h_id = re.sub(r'[^0-9]', '', url.split("._")[1])
            images_req = response.css('.gallery-img-frame')
            for image in images_req:
                images.append('https://' + image.css('::attr(data-url)').get().replace('//', ''))
            if response.css('.item-description-text > p'):
                print('Base text')
                data_set = response.css('.item-description-text > p::text').getall()
            if response.css('.item-description-html > p'):
                print('html text')
                data_set = response.css('.item-description-html > p::text').getall()
            elif response.css('.item-description-html::text'):
                data_set = response.css('.item-description-html::text').getall()
            data = ' '.join(data_set)
            type_ = response.css('.breadcrumbs > span > a > span::text').getall()[-1]
            if response.url.find('zemelnye_uchastki') > 0:
                type_ = 'Участки'
            print(type_)
            if type_ == 'Участки':
                land_area = response.css('.item-params > span').get().split('</span>')[-2].replace('сот.; ', '')
            else:
                for info_colum in response.css('li.item-params-list-item'):
                    re_Info = info_colum
                    re_Info = re.sub(r' |</li>', '', re_Info.extract().split(' </span>')[1])
                    info_colum = info_colum.css('span.item-params-label::text').get()
                    print(info_colum, re_Info)
                    # print(re.search(r'в доме', info_colum), re_Info)
                    if re.search(r'Тип участия', info_colum):
                        type_of_participation = re_Info
                    if re.search(r'Официальный застройщик', info_colum):
                        # print(re_Info)
                        official_builder = re_Info
                    if re.search(r'Название новостройки', info_colum):
                        name_of_build = re_Info
                    if re.search(r'Отделка', info_colum):
                        decoration = re_Info
                    if re.search(r'Этаж:', info_colum):
                        floor = re_Info
                    if re.search(r'в доме', info_colum):
                        # print(re_Info)
                        floor_count = re_Info
                    if re.search(r'Материал стен', info_colum):
                        house_type = re_Info
                    if re.search(r'Количество комнат', info_colum):
                        num_of_rooms = re_Info
                    if re.search(r'Площадь дома', info_colum):
                        total_area = re_Info
                    if re.search(r'Жилая площадь', info_colum):
                        living_area = re_Info

                    if re.search(r'Площадь участка', info_colum):
                        land_area = re_Info.replace('сот.', '')
                    if re.search(r'Площадь кухни', info_colum):
                        kitchen_area = re_Info

            yield {
                'type': type_,
                'mode': 1,
                'house_id': h_id,
                'type_of_participation': type_of_participation,
                'official_builder': official_builder,
                'name_of_build': name_of_build,
                'decoration': decoration,
                "floor": "0",
                "floor_count": floor_count,
                "house_type": house_type,
                "num_of_rooms": num_of_rooms,
                "total_area": total_area,
                "living_area": living_area,
                "kitchen_area": kitchen_area,
                "deadline": deadline,
                'images': images,
                'data': data,
                'land_area': land_area,
                'headers': Headers}
        type_ = response.css('.breadcrumbs > span > a > span::text').getall()[-1]
        if url.find('zemelnye_uchastki') > 0:
            type_ = 'Участки'
            print(type_)
            if type_ == 'Участки':
                land_area = response.css('.item-params > span').get().split('</span>')[-2].replace('сот.; ', '')
            yield {
                'type': type_,
                'mode': 1,
                'house_id': h_id,
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
                'headers': Headers}
            return h_id

    def get_house_id(self, url):
        if url.split("._").__len__() > 2:
            h_id = re.sub(r'[^0-9]', '', url.split("._")[2])
        else:
            if url.split("._").__len__() == 1:
                h_id = re.sub(r'[^0-9]', '', url.split("_")[-1])
            else:
                h_id = re.sub(r'[^0-9]', '', url.split("._")[1])
        return h_id
