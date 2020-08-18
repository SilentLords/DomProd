# -*- coding: utf-8 -*-
import json
import re
from time import sleep,time
from inline_requests import inline_requests
import scrapy


def save_images(images):
    pass


class InfoSpider(scrapy.Spider):
    all_json_data = []
    total_time = 0
    links = []
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    phone = ''
    id_house = 0

    def start_requests(self):
        with open('links.csv') as f:
            self.links = f.read().splitlines()
            yield scrapy.Request(url=self.links[0], callback=self.parse)

    name = 'info_v1'
    allowed_domains = ['avito.ru']

    @inline_requests
    def parse(self, response):
        time_start = time()
        print(f'processing: {response.url}')
        Headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
            'accept': '*/*',
            'referer': response.url}
        type_of_participation, land_area, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
        images = []
        land_area = 0
        # print(response.url)
        if response.url.find('kvartiry') > 0:
            print('Квартиры')
            req = yield scrapy.Request(
                url=f'http://m.avito.ru/api/1/items/{response.url.split("._")[1]}/phone/?key={self.key}',
                headers=Headers)
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
            if re.findall('bad-request', req.body.decode("utf-8")):
                print('bad_req', req.body.decode("utf-8"))
                num = 000000000
            else:
                num = req.body.decode("utf-8").split('2B')[1].replace('"}}}', '')
            type_ = response.css('.breadcrumbs > span > a > span::text').getall()[-1]
            print(type_)
            for info_colum in response.css('li.item-params-list-item'):
                re_Info = info_colum
                re_Info = re.sub(r' |</li>', '', re_Info.extract().split(' </span>')[1])
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
                    floor = re_Info
                if re.search(r'в доме', info_colum):
                    # print(re_Info)
                    floor_count = re_Info
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
            if response.url.split("._").__len__() > 2:
                h_id = response.url.split("._")[2]
            else:
                h_id = response.url.split("._")[1]
            yield {
                'type': type_,
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
                "deadline": deadline,
                'phone': num,
                'images': images,
                'data': data}
        else:
            print('Дачи')
            if response.url.split("._").__len__() > 2:
                h_id = re.sub(r'[^0-9]', '', response.url.split("._")[2])
            else:
                if response.url.split("._").__len__() == 1:
                    h_id = re.sub(r'[^0-9]', '', response.url.split("_")[-1])
                else:
                    h_id = re.sub(r'[^0-9]', '', response.url.split("._")[1])
            req = yield scrapy.Request(
                url=f'http://m.avito.ru/api/1/items/{h_id}/phone/?key={self.key}',
                headers=Headers)
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
            if re.findall('bad-request', req.body.decode("utf-8")):
                print('bad_req', req.body.decode("utf-8"))
                num = 000000000
            else:
                num = req.body.decode("utf-8").split('2B')[1].replace('"}}}', '')
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
                'house_id': h_id,
                'type_of_participation': type_of_participation,
                'official_builder': official_builder,
                'name_of_build': name_of_build,
                'decoration': decoration,
                "floor": 0,
                "floor_count": floor_count,
                "house_type": house_type,
                "num_of_rooms": num_of_rooms,
                "total_area": total_area,
                "living_area": living_area,
                "kitchen_area": kitchen_area,
                "deadline": deadline,
                'phone': num,
                'images': images,
                'data': data,
                'land_area': land_area}

        self.id_house += 1
        print(f'Parsed links: {self.id_house} of{self.links.__len__()} ')
        self.total_time += int((time() - time_start) % 60)
        sleep(8)
        if self.links.__len__() > self.id_house:
            yield scrapy.Request(self.links[self.id_house],
                                 callback=self.parse, dont_filter=True)
        else:
            print('save', self.total_time)
