# -*- coding: utf-8 -*-
import django
import os
import re
import scrapy
import sys

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
django.setup()
from services import get_cord
from apps.base.models import HouseModel, CITY_CHOICES


def get_house_id(url):
    if url.split("._").__len__() > 2:
        h_id = re.sub(r'[^0-9]', '', url.split("._")[2])
    else:
        if url.split("._").__len__() == 1:
            h_id = re.sub(r'[^0-9]', '', url.split("_")[-1])
        else:
            h_id = re.sub(r'[^0-9]', '', url.split("._")[1])
    return h_id


def get_phone_num(text):
    phone = '7' + text
    phone = re.sub(r'a', '1', phone)
    phone = re.sub(r'b', '2', phone)
    phone = re.sub(r'c', '3', phone)
    phone = re.sub(r'd', '4', phone)
    phone = re.sub(r'e', '5', phone)
    phone = re.sub(r'g', '6', phone)
    phone = re.sub(r'i', '7', phone)
    phone = re.sub(r'f', '8', phone)
    phone = re.sub(r'h', '9', phone)
    phone = re.sub(r'j', '0', phone)
    print(phone)
    return phone


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


def correct_price(text):
    return int(re.sub(r'[^0-9]', '', text))


def get_house_type(house_id):
    try:
        return HouseModel.objects.get(house_id=house_id).type
    except:
        return ''


def delete_house_model(house_id):
    HouseModel.objects.filter(house_id=house_id).delete()


class TyumenNedvizimostSpider(scrapy.Spider):
    name = 'tyumen-nedvizimost'
    allowed_domains = ['tyumen-nedvizimost.ru']
    urls_pool = [
        'https://tyumen-nedvizimost.ru/kvartiry/prodam/bezposrednikov/',
        'https://tyumen-nedvizimost.ru/doma_dachi_kottedzhi/prodam/bezposrednikov/',
    ]
    start_urls = [urls_pool[0]]
    parsing_params = {
        'card_to_parse': 2,
        'card_selector': '.a_blok5',
        'house_type_set': ['Вторичка', 'Коттеджи'],
        'ignore_selector': 'span.snippet-tag',
        'link_selector': '.a_blok5_txt > h3 > a::attr(href)',
        'address_selector': '.areas::text',
        'title_image_selector': 'img.a_blok5_img::attr(src)',
        'title_selector': '.a_blok5_txt > h3 > a::attr(title)',
        'price_selector': '.a_blok_txt_r::text'
    }
    parsing_info_params = {'image_set_selector': '.img_small',
                           'image_data_selector': '::attr(src)',
                           'data_selectors': "p::text",
                           'info_selectors': ['.about-object > div', 'span::text'],
                           'phone_selector': '#a_tel::text'
                           }

    def parse(self, response):
        page_index = self.urls_pool.index(response.url)
        cards = response.css(self.parsing_params['card_selector'])
        print(f'Processing: {response.url}')
        type_of_house = self.parsing_params['house_type_set'][page_index]
        counter = 0
        for correct_card in cards:
            if correct_card.css(self.parsing_params['ignore_selector']):
                cards.pop(cards.index(correct_card))
                counter += 1
        print(f'Deleted lines: {counter}')
        for card in cards:
            if cards.index(card) < self.parsing_params['card_to_parse']:
                house_link = response.urljoin(card.css(self.parsing_params['link_selector']).get())
                house_id = get_house_id(house_link)
                if check_db(house_id):
                    _ = yield from self.parse_card(card, type_of_house, house_id, house_link, response, page_index)
                    yield scrapy.Request(url=house_link, callback=self.parse_info)
                else:
                    print('This house is already exist')
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def get_views_count(self, response):
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).getall()[-1]
                                 .split(' ')[0]))
        return views_count

    def parse_card(self, card, type_of_house, house_id, link, response, page_index=0):
        city = 0
        address = CITY_CHOICES[city][1] + card.css(self.parsing_params['address_selector']).get()
        x_cord, y_cord, address = get_cord(address)
        title_image = response.urljoin(card.css(self.parsing_params['title_image_selector']).get())
        title = card.css(self.parsing_params['title_selector']).get()
        price = correct_price(card.css(self.parsing_params['price_selector']).get())
        item = {
            'mode': 0,
            'house_id': house_id,
            'img': title_image,
            'title': title,
            'link': link,
            'price': price,
            'address': address,
            'host': self.allowed_domains[0],
            'city': city,
            'cords': [x_cord, y_cord],
            'house_type': type_of_house
        }
        print(item)
        yield item
        return ''

    def parse_info(self, response):
        house_id = get_house_id(response.url)
        floor = floor_count = total_area = living_area = kitchen_area = land_area = 0
        name_of_build = data = num_of_rooms = decoration = official_builder = type_of_participation = house_type = ''
        image_set = response.css(self.parsing_info_params['image_set_selector'])
        images = []
        for image in image_set:
            images.append(f'https://{self.allowed_domains[0]}{image.css(self.parsing_info_params["image_data_selector"]).get()}')
        data = ''.join(response.css(self.parsing_info_params['data_selectors']).getall())
        query_selector = self.parsing_info_params['info_selectors'][0]
        for info in response.css(query_selector):
            values = []
            for i in info.css(self.parsing_info_params['info_selectors'][1]).getall():
                if not (i == '' or i == ' '):
                    values.append(i)
            name_of_field = values[0]
            value_of_field = values[1]
            if re.search(r'Тип участия', name_of_field):
                type_of_participation = value_of_field
            if re.search(r'Официальный застройщик', name_of_field):
                official_builder = value_of_field
            if re.search(r'Название новостройки', name_of_field):
                name_of_build = value_of_field
            if re.search(r'Отделка', name_of_field):
                decoration = value_of_field
            if re.search(r'Этаж', name_of_field):
                value_of_field = re.sub(r'[^0-9из]', '', value_of_field)
                floor = int(value_of_field)
            if re.search(r'Всего этажей в доме', name_of_field):
                value_of_field = re.sub(r'[^0-9из]', '', value_of_field)
                floor_count = int(value_of_field)
            if re.search(r'Тип дома', name_of_field):
                house_type = value_of_field
            if re.search(r'Количество комнат', name_of_field):
                num_of_rooms = value_of_field.replace(' ', '')

                if num_of_rooms == 'студии' or num_of_rooms == "своб.планировка":
                    print('Студия или своб. планировка')
                else:
                    if int(num_of_rooms) >= 5:
                        num_of_rooms = f"5к+ {int(num_of_rooms.split('к')[0])}"
                    else:
                        num_of_rooms = f"{int(num_of_rooms.split('к')[0])}к"

            if re.search(r'Общая площадь', name_of_field):
                total_area = float(re.sub(r'[^0-9.]', '', value_of_field))
            if re.search(r'Материал дома', name_of_field):
                house_type = value_of_field
            if re.search(r'Жилая площадь', name_of_field):
                living_area = float(re.sub(r'[^0-9.]', '', value_of_field))
            if re.search(r'Площадь кухни', name_of_field):
                kitchen_area = float(re.sub(r'[^0-9.]', '', value_of_field))
            if re.search(r'Площадь дома', name_of_field):
                total_area = float(re.sub(r'[^0-9.]', '', value_of_field))
            if re.search(r'Площадь участка', name_of_field):
                land_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace('сот.', '')))
            if re.search(r'Площадь:', name_of_field):
                land_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace('сот.', '')))
        phone_num = get_phone_num(response.css(self.parsing_info_params['phone_selector']).get())
        item = {
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
            'data': data,
            'img_set': images,
            'phone_num': phone_num}
        print(item)
        yield item
