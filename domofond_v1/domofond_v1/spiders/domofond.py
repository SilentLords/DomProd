# -*- coding: utf-8 -*-
import os
import re
import sys
import scrapy
import requests as r
import json

DEBUG = True

if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/DomProd/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'
import datetime

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from services import get_cord

from apps.base.models import HouseModel, CITY_CHOICES


def correct_house_id(url):
    house_id = re.sub(r'[^0-9]', '', re.sub(r'/|\?osale2|\?osale1| ', '', url))
    if len(house_id) > 10:
        return int(house_id) % 10000000
    else:
        return int(house_id)


def delete_house_model(house_id):
    print(house_id)
    HouseModel.objects.filter(house_id=house_id).delete()
    print(HouseModel.objects.filter(house_id=house_id))


#
def get_phone(house_id):
    try:
        b = '''{"id":"1","jsonrpc":"2.0","method":"item.GetItemPhoneV1","params":{"meta":{"platform":"web","language":"ru"},"id":''' + house_id + ''',"itemType":"Listing"}}'''
        a = r.post(url='https://api.domofond.ru/rpc', data=b.encode('utf-8'))
        return a.json()['result']['phone']
    except:
        return '0'


def check_db(house_id_val, title):
    if HouseModel.objects.filter(house_id=house_id_val) or HouseModel.objects.filter(title=title):
        return False
    else:
        return True


class DomofondSpider(scrapy.Spider):
    name = 'domofond'
    allowed_domains = ['domofond.ru']
    house_id_global = 0
    start_urls = [
        'https://www.domofond.ru/prodazha-kvartiry-tyumen-c2547?ApartmentSaleType=New&PrivateListingType=PrivateOwner&SortOrder=Newest']
    urls_pool = [
        'https://www.domofond.ru/prodazha-kvartiry-tyumen-c2547?ApartmentSaleType=New&PrivateListingType=PrivateOwner&SortOrder=Newest',
        'https://www.domofond.ru/prodazha-kvartiry-tyumen-c2547?ApartmentSaleType=Resale&PrivateListingType=PrivateOwner&SortOrder=Newest',
        'https://www.domofond.ru/prodazha-doma-tyumen-c2547?PrivateListingType=PrivateOwner',
        'https://www.domofond.ru/prodazha-uchastkizemli-tyumen-c2547?PrivateListingType=PrivateOwner',
        'https://www.domofond.ru/prodazha-kommercheskay-nedvizhimost-tyumen-c2547?PrivateListingType=PrivateOwner&SortOrder=Newest',
        'https://www.domofond.ru/arenda-kvartiry-tyumen-c2547?RentalRate=Month&PrivateListingType=PrivateOwner&SortOrder=Newest',
        'https://www.domofond.ru/arenda-doma-tyumen-c2547?RentalRate=Month&PrivateListingType=PrivateOwner&SortOrder=Newest']
    types = ['Новостройки', 'Вторичка', 'Коттеджи', 'Участки', 'Коммерческаянедвижимость']

    def parse(self, response):
        cards = response.css('a.long-item-card__item___ubItG')
        page_index = self.urls_pool.index(response.url)
        for card in cards:
            if cards.index(card) < 5:
                link = response.urljoin(card.css('::attr(href)').get())
                house_id = correct_house_id(link)
                title = card.css('span.long-item-card__title___16K7W::text').get()
                if check_db(house_id, title):
                    _ = yield from self.parse_card(card, response, page_index)
                    yield scrapy.Request(url=link, callback=self.parse_info)
                else:
                    print('THIS HOUSE ALREADY EXIST')
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(url=self.urls_pool[page_index + 1], callback=self.parse)

    def parse_card(self, card, response, page_index):
        city = 0
        if 0 <= page_index < 5:
            city = 0
            offer_type = 0
        else:
            city = 0
            offer_type = 1
        title = card.css('span.long-item-card__title___16K7W::text').get()
        link = response.urljoin(card.css('::attr(href)').get())
        house_id = correct_house_id(link.split('-')[-1])
        self.house_id_global = correct_house_id(link.split('-')[-1])
        price = re.sub(r'[^0-9]', '', card.css('span.long-item-card__price___3A6JF::text').get())
        address = card.css('span.long-item-card__address___PVI5p::text').get()
        if address.find(CITY_CHOICES[city][1]) == -1:
            address = CITY_CHOICES[city][1] + ' ' + address
        x_cord, y_cord, address = get_cord(address)
        title_image = card.css('img.card-photo__image___31CHC::attr(src)').get()
        if 0 <= page_index < 5:
            type_ = self.types[self.urls_pool.index(response.url)]
        else:
            type_ = self.types[self.urls_pool.index(response.url) - 4]
        print('suka')
        yield ({
            'mode': 0,
            'offer_type': offer_type,
            'type': type_,
            'house_id': house_id,
            "link": link,
            "title": title,
            "price": price,
            'address': address,
            "img": title_image,
            'time_created': '',
            'data': '',
            'host': self.allowed_domains[0],
            'city': city,
            'cords': [x_cord, y_cord]
        })
        return ''

    def get_photos(self, response):
        text = response.text
        images = []
        try:
            if text.find('PhotoGallery') > -1:
                text = text.split('"galleries":[')[-1].split('],"phone":')[0]
                json_text = json.loads(text)
                for image in json_text['images']:
                    # print(image)
                    images.append(image[0]['url'])
                # print(images)
                return images
            else:
                return []
        except:
            return []

    def parse_info(self, response):
        is_today = False
        num_of_rooms = type_ = house_type = ''
        house_id_for_phone = floor = land_area = floor_count = total_area = living_area = kitchen_area = house_id = 0
        for item in response.css('.detail-information__row___29Fu6'):
            sub_item = item.css('span::text').getall()
            if sub_item.__len__() - 1 > 1:
                if sub_item[0] == 'Дата обновления объявления':
                    date = datetime.datetime(int(sub_item[2].split('/')[-1]), int(sub_item[2].split('/')[1]),
                                             int(sub_item[2].split('/')[0]))
                    if date.date() == datetime.datetime.today().date():
                        is_today = True
        house_id = correct_house_id(response.url.split('-')[-1])
        if is_today:
            for item in response.css('.detail-information__row___29Fu6'):
                sub_item = item.css('span::text').getall()
                if sub_item.__len__() - 1 > 1:
                    if sub_item[0] == "Тип объекта":
                        type_ = sub_item[2].replace('Новостройка', self.types[0]).replace('Вторичная',
                                                                                          self.types[1]).replace(
                            'Дом', self.types[2]).replace('Участок', self.types[3])
                    if sub_item[0] == 'Комнаты':
                        num_of_rooms = sub_item[2]
                        if num_of_rooms != '':
                            if num_of_rooms == 'Студия':
                                num_of_rooms = 'студии'
                            else:
                                if int(num_of_rooms) >= 5:
                                    num_of_rooms = f'5к+ {num_of_rooms}'
                                else:
                                    num_of_rooms = f'{num_of_rooms}к'
                    if sub_item[0] == 'Этаж':
                        floor = sub_item[2].split('/')[0]
                        floor_count = sub_item[2].split('/')[1]
                    if sub_item[0] == 'Площадь':
                        if not type_ == self.types[3]:
                            total_area = re.sub(r'[^0-9.]', '', sub_item[2])
                        else:
                            land_area = re.sub(r'[^0-9.]', '', sub_item[2])
                    if sub_item[0] == 'Площадь кухни (м²)':
                        kitchen_area = re.sub(r'[^0-9.]', '', sub_item[2])
                    if sub_item[0] == 'Жилая площадь (м²)':
                        living_area = re.sub(r'[^0-9.]', '', sub_item[2])
                    if sub_item[0] == 'Материал здания':
                        house_type = sub_item[2]
                    if sub_item[0] == 'Номер в каталоге':
                        house_id_for_phone = sub_item[2]
            data = response.css('.description__description___2FDOM::text').get()
            phone_val = re.sub(r'[^0-9]', '', get_phone(house_id_for_phone))
            images = self.get_photos(response)
            yield ({
                'mode': 1,
                'type': type_,
                'house_id': house_id,
                'type_of_participation': '',
                'official_builder': '',
                'name_of_build': '',
                'decoration': '',
                "floor": floor,
                "floor_count": floor_count,
                "house_type": house_type,
                "num_of_rooms": num_of_rooms,
                "total_area": total_area,
                "living_area": living_area,
                "kitchen_area": kitchen_area,
                "deadline": '',
                'phone': phone_val,
                'images': images,
                "data": data,
                'land_area': land_area
            })
        else:
            print('Old house')
            delete_house_model(house_id)
