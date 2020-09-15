# -*- coding: utf-8 -*-
import django
import os
import re
import scrapy
import sys

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/DomProd'
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


def check_db(house_id_val, title):
    if HouseModel.objects.filter(house_id=house_id_val) or HouseModel.objects.filter(title=title):
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


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    urls_pool = [
        'https://www.avito.ru/tyumen/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1&s=104&proprofile=1&f=ASgBAQICAUSSA8YQAkDmBxSMUpC~DRSWrjU',
        'https://www.avito.ru/tyumen/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?cd=1&s=104&proprofile=1&f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSWrjU',
        'https://www.avito.ru/tyumen/doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA9AQ?cd=1&s=104&user=1&proprofile=1',
        'https://www.avito.ru/tyumen/zemelnye_uchastki/prodam-ASgBAgICAUSWA9oQ?cd=1&s=104&user=1&proprofile=1',
        'https://www.avito.ru/tyumen/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?cd=1&s=104&user=1&proprofile=1&f=ASgBAgICAkSwCNJW8hKg2gE',
        'https://www.avito.ru/tyumen/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104&user=1&proprofile=1',
        'https://www.avito.ru/tyumen/doma_dachi_kottedzhi/sdam-ASgBAgICAUSUA9IQ?cd=1&s=104&user=1&proprofile=1',
        'https://www.avito.ru/tyumen/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?cd=1&s=104&user=1&proprofile=1&f=ASgBAgICAkSwCNRW9BKk2gE'
    ]
    start_urls = [urls_pool[0]]
    parsing_params = {
        'card_to_parse': 4,
        'key_to_phone': 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
        'card_selector': '.item__line',
        'house_type_set': ['Вторичка', 'Новостройки', 'Коттеджи', 'Участки','Коммерческаянедвижимость'],
        'ignore_selector': 'span.snippet-tag',
        'link_selector': 'a.snippet-link::attr(href)',
        'geo_selector': 'span.item-address-georeferences',
        'geo_data_selector': 'span.item-address-georeferences-item__content::text',
        'address_selector': 'span.item-address__string::text',
        'title_image_selector': 'img.large-picture-img::attr(src)',
        'title_selector': 'h3.snippet-title >a > span::text',
        'price_selector': 'span.snippet-price::text'
    }
    parsing_info_params = {'image_set_selector': '.gallery-img-frame',
                           'image_data_selector': '::attr(data-url)',
                           'data_selectors': [['.item-description-text > p', '.item-description-text > p::text'],
                                              ['.item-description-html::text', '.item-description-html > p::text'],
                                              ['.item-description-html::text', '.item-description-html::text']],
                           'views_selector': '.title-info-metadata-views::text',
                           'info_selectors': [['li.item-params-list-item', 'span::text', '::text'],
                                              ['.item-params > span', 'span > span::text', '::text']]
                           }

    def parse(self, response):
        page_index = self.urls_pool.index(response.url)
        cards = response.css(self.parsing_params['card_selector'])
        print(f'Processing: {response.url}')
        if page_index == 5:
            type_of_house = self.parsing_params['house_type_set'][0]
        elif page_index == 6:
            type_of_house = self.parsing_params['house_type_set'][2]
        elif page_index == 7:
            type_of_house = self.parsing_params['house_type_set'][-1]
        else:
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
                title = card.css(self.parsing_params['title_selector']).get()

                _ = yield from self.parse_card(card, type_of_house, house_id, house_link, page_index)
                yield scrapy.Request(url=house_link, callback=self.parse_info)
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def get_views_count(self, response):
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).getall()[-1]
                                 .split(' ')[0]))
        return views_count

    def parse_card(self, card, type_of_house, house_id, link, page_index=0):
        city = 0
        geo = ''
        if 0 <= page_index < 5:
            city = 0
            offer_type = 0
        else:
            offer_type = 1
        if card.css(self.parsing_params['geo_selector']):
            geo = card.css(self.parsing_params['geo_data_selector']).get()
        address = CITY_CHOICES[city][1] + card.css(self.parsing_params['address_selector']).get() + geo
        x_cord, y_cord, address = get_cord(address)
        title_image = card.css(self.parsing_params['title_image_selector']).get()
        title = card.css(self.parsing_params['title_selector']).get()
        price = correct_price(card.css(self.parsing_params['price_selector']).get())
        item = {
            'mode': 0,
            'offer_type': offer_type,
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
        # print(item)
        yield item
        return ''

    def parse_info(self, response):
        headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.1; AOLBuild 4334.34; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
            'accept': '*/*',
            'referer': response.url}
        house_id = get_house_id(response.url)
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).getall()[-1]
                                 .split(' ')[0]))
        print(views_count)
        if views_count <= 100:
            floor = floor_count = total_area = living_area = kitchen_area = land_area = 0
            name_of_build = data = num_of_rooms = decoration = official_builder = type_of_participation = house_type = ''
            type_ = get_house_type(house_id)
            image_set = response.css(self.parsing_info_params['image_set_selector'])
            images = []
            for image in image_set: images.append(
                f'{image.css(self.parsing_info_params["image_data_selector"]).get()}')
            if response.css(self.parsing_info_params['data_selectors'][0][0]):
                data = ''.join(response.css(self.parsing_info_params['data_selectors'][0][1]).getall())
            if response.css(self.parsing_info_params['data_selectors'][1][0]):
                data = ''.join(response.css(self.parsing_info_params['data_selectors'][1][1]).getall())
            elif response.css(self.parsing_info_params['data_selectors'][2][0]):
                data = ''.join(response.css(self.parsing_info_params['data_selectors'][2][1]).getall())
            if not type_ == self.parsing_params['house_type_set'][-1]:
                query_selector = self.parsing_info_params['info_selectors'][0][0]
            else:
                query_selector = self.parsing_info_params['info_selectors'][1][0]
            for info in response.css(query_selector):
                values = []
                for i in info.css('::text').getall():
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
                if re.search(r'Этаж:', name_of_field):
                    value_of_field = re.sub(r'[^0-9из]', '', value_of_field)
                    floor = int(value_of_field.split('из')[0])
                    floor_count = int(value_of_field.split('из')[1])
                if re.search(r'Тип дома', name_of_field):
                    house_type = value_of_field
                if re.search(r'Количество комнат', name_of_field):
                    num_of_rooms = value_of_field.replace(' ', '')

                    if num_of_rooms == 'студии' or num_of_rooms == "своб.планировка" or num_of_rooms == 'студия':
                        print('Студия или своб. планировка')
                    else:
                        if int(num_of_rooms.split('к')[0]) >= 5:
                            num_of_rooms = f"5к+ {int(num_of_rooms.split('к')[0])}"
                        else:
                            num_of_rooms = f"{int(num_of_rooms.split('к')[0])}к"

                if re.search(r'Общая площадь', name_of_field):
                    total_area = float(re.sub(r'[^0-9.]', '', value_of_field))
                if re.search(r'Материал стен', name_of_field):
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
                'headers': headers,
                'data': data,
                'img_set': images}
            print(item)
            yield item
        else:
            print('Too many views (>100)')
            delete_house_model(house_id)
