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


class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['cian.ru']
    urls_pool = [
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=2&offer_type=flat&region=5024&totime=3600',
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&object_type%5B0%5D=1&offer_type=flat&region=5024&totime=3600',
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&object_type%5B0%5D=1&offer_type=suburban&region=5024&suburban_offer_filter=2&totime=3600',
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&is_by_homeowner=1&object_type%5B0%5D=3&offer_type=suburban&region=5024&totime=3600'
        'https://tyumen.cian.ru/cat.php?deal_type=sale&engine_version=2&estate_type%5B0%5D=1&offer_type=offices&office_type%5B0%5D=1&office_type%5B10%5D=12&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=4&office_type%5B4%5D=5&office_type%5B5%5D=6&office_type%5B6%5D=7&office_type%5B7%5D=9&office_type%5B8%5D=10&office_type%5B9%5D=11&region=5024&totime=3600',
        'https://tyumen.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=5024&totime=3600&type=4',
        'https://tyumen.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&object_type%5B0%5D=1&offer_type=suburban&region=5024&totime=3600&type=4',
        'https://tyumen.cian.ru/cat.php?deal_type=rent&engine_version=2&estate_type%5B0%5D=1&offer_type=offices&office_type%5B0%5D=1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=4&office_type%5B4%5D=5&office_type%5B5%5D=6&office_type%5B6%5D=7&office_type%5B7%5D=9&office_type%5B8%5D=12&region=5024&totime=3600'
    ]
    start_urls = [urls_pool[0]]
    parsing_params = {
        'card_to_parse': 4,
        'card_selector': ['._93444fe79c--card--_yguQ', '.c6e8ba5398--container--Y5gG9'],
        'house_type_set': ['Новостройки','Вторичка',  'Коттеджи', 'Участки', 'Коммерческаянедвижимость'],
        'ignore_selector': 'span.snippet-tag',
        'link_selector': ['a.c6e8ba5398--header--1fV2A::attr(href)', 'a.c6e8ba5398--header--1fV2A::attr(href)'],
        'geo_selector': 'span.item-address-georeferences',
        'geo_data_selector': 'span.item-address-georeferences-item__content::text',
        'address_selector': '.c6e8ba5398--address-links--1tfGW > span::attr(content)',
        'title_image_selector': 'img.c6e8ba5398--image--3ua1b::attr(src)',
        'title_selector': ['.c6e8ba5398--subtitle--UTwbQ::text', '.c6e8ba5398--title--2CW78::text'],
        'price_selector': ['.c6e8ba5398--header--1dF9r::text', '.c6e8ba5398--header--1df-X::text']
    }
    parsing_info_params = {'image_set_selector': '.gallery-img-frame',
                           'image_data_selector': '::attr(data-url)',
                           'data_selector': 'p.a10a3f92e9--description-text--3Sal4::text',
                           'views_selector': '.a10a3f92e9--link--1t8n1::text',
                           'info_selectors': ['.a10a3f92e9--info--3XiXi','.a10a3f92e9--info-value--18c8R::text','.a10a3f92e9--info-title--2bXM9::text'],
                           'phone_selector': 'a.a10a3f92e9--phone--3XYRR::text'
                           }

    def parse(self, response):
        page_index = self.urls_pool.index(response.url)
        if response.css(self.parsing_params['card_selector'][0]):
            cards = response.css(self.parsing_params['card_selector'][0])
            other_cards = response.css(self.parsing_params['card_selector'][1])
        else:
            cards = response.css(self.parsing_params['card_selector'][1])
            other_cards = []
        cards += other_cards
        print(f'Processing: {response.url}')
        # TODO CORRECT
        if page_index < 4:
            type_of_house = self.parsing_params['house_type_set'][page_index]
        else:
            type_of_house = self.parsing_params['house_type_set'][page_index-4]
        counter = 0
        print(f'Deleted lines: {counter}')
        for card in cards:
            if cards.index(card) < self.parsing_params['card_to_parse']:
                if card.css(self.parsing_params['link_selector'][0]).get():
                    house_link = response.urljoin(card.css(self.parsing_params['link_selector'][0]).get())
                    title = card.css(self.parsing_params['title_selector'][0]).get()
                else:
                    house_link = response.urljoin(card.css(self.parsing_params['link_selector'][1]).get())
                    title = card.css(self.parsing_params['title_selector'][1]).get()

                house_id = get_house_id(house_link)
                if check_db(house_id, title):
                    _ = yield from self.parse_card(card, type_of_house, house_id, house_link, page_index)
                    yield scrapy.Request(url=house_link, callback=self.parse_info)
                else:
                    print('This house is already exist')
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
        if card.css(self.parsing_params['price_selector'][0]).get():
            address = card.css(self.parsing_params['address_selector']).get() + geo
            if card.css(self.parsing_params['title_selector'][0]).get():
                title = card.css(self.parsing_params['title_selector'][0]).get()
            else:
                title = card.css('.c6e8ba5398--single_title--22TGT::text').get()
            price = correct_price(card.css(self.parsing_params['price_selector'][0]).get())
        else:
            if card.css(self.parsing_params['title_selector'][1]).get():
                title = card.css(self.parsing_params['title_selector'][1]).get()
            else:
                title = card.css('.c6e8ba5398--single_title--22TGT::text').get()
            address = card.css(self.parsing_params['address_selector']).get() + geo
            print('hu2')
            price = correct_price(card.css(self.parsing_params['price_selector'][1]).get())

        x_cord, y_cord, address = get_cord(address)
        title_image = card.css(self.parsing_params['title_image_selector']).get()
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
        print(item)
        yield item
        return ''

    def parse_info(self, response):
        house_id = get_house_id(response.url)
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).get()))
        print(views_count)
        if views_count <= 100:
            floor = floor_count = total_area = living_area = kitchen_area = land_area = 0
            name_of_build = data = num_of_rooms = decoration = official_builder = type_of_participation = house_type = ''
            type_ = get_house_type(house_id)
            image_set = response.css(self.parsing_info_params['image_set_selector'])
            images = []
            data = response.css(self.parsing_info_params['data_selector']).get()
            query_selector = self.parsing_info_params['info_selectors']
            for info in response.css(query_selector[0]):
                name_of_field = info.css(query_selector[2]).get()
                value_of_field = info.css(query_selector[1]).get()
                print(name_of_field, value_of_field)
                if re.search(r'Тип участия', name_of_field):
                    type_of_participation = value_of_field
                if re.search(r'Официальный застройщик', name_of_field):
                    official_builder = value_of_field
                if re.search(r'Название новостройки', name_of_field):
                    name_of_build = value_of_field
                if re.search(r'Отделка', name_of_field):
                    decoration = value_of_field
                if re.search(r'Этаж', name_of_field):
                    try:
                        value_of_field = re.sub(r'[^0-9из]', '', value_of_field)
                        floor = int(value_of_field.split('из')[0])
                        floor_count = int(value_of_field.split('из')[1])
                    except:
                        floor_count = int(value_of_field)
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

                if re.search(r'Общая', name_of_field):
                    total_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace(',', '.')))
                if re.search(r'Площадь', name_of_field):
                    if re.search(r'сот.', value_of_field):
                        land_area =  float(re.sub(r'[^0-9.]', '', value_of_field.replace('сот.', '')))
                    else:
                        total_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace(',', '.')))
                if re.search(r'Материал стен', name_of_field):
                    house_type = value_of_field
                if re.search(r'Жилая', name_of_field):
                    living_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace(',', '.')))
                if re.search(r'Кухня', name_of_field):
                    kitchen_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace(',', '.')))
                if re.search(r'Площадь дома', name_of_field):
                    total_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace(',', '.')))
                if re.search(r'Участок', name_of_field):
                    land_area = float(re.sub(r'[^0-9.]', '', value_of_field.replace('сот.', '')))
            try:
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
            except:
                num_of_rooms = ''

            phone = re.sub(r'[^0-9]','',response.css(self.parsing_info_params['phone_selector']).get().replace(' ', ''))

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
                'phone': phone,
                # 'headers': headers,
                'data': data,
                'img_set': images,
            'deadline': ''}
            print(item)
            yield item
        else:
            print('Too many views (>100)')
            delete_house_model(house_id)
