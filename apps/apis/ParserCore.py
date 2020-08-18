from bs4 import BeautifulSoup
import requests
import time
import csv
import asyncio

URL = 'https://www.avito.ru/tyumen/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?cd=1&rn=25928'
Headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129',
    'accept': '*/*'}
PATH = '../../Data/ParcerCards/res.csv'
PATH_domofond = 'resdom.csv'
PATH_n1 = 'resn1.csv'
HOST = "https://www.avito.ru/"
HOSTD = "https://www.domofond.ru"
hostn1 = "https://tumen.n1.ru"
PROXY_LIST = [{
    'http': 'http://Selmrniki002:T2d2DiW@37.44.198.207:45785',
}]

domofond = {
    'url': 'https://www.domofond.ru/prodazha-kvartiry-tyumen-c2547?PrivateListingType=PrivateOwner',
    'card_data': ['a', 'long-item-card__item___ubItG'],
    "title": ["span", "long-item-card__title___16K7W"],
    "link": ["a", "long-item-card__item___ubItG"],
    "price": ["span", "long-item-card__price___3A6JF"],
    'address': ["span", "long-item-card__address___PVI5p"],
    "data": ["div", "description__descriptionBlock___3KWc1"],
    "time_ago": ["span", "long-item-card__listDate___1AWok"],
    "pagination": ['li', "pagination__page___2dfw0", -1],
    "paginator_params": 'Page'
}
avito = {
    'url': "https://www.avito.ru/tyumen/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?cd=1&rn=25928",
    'card_data': ['div', 'item__line'],
    "title": ["a", "snippet-link"],
    "link": ["a", "snippet-link"],
    "price": ["span", "snippet-price"],
    'address': ["div", "address"],
    "data": ["div", "data"],
    "time_ago": ["div", "snippet-date-info"],
    "pagination": ['span', "pagination-item-1WyVp", -2],
    "paginator_params": 'p'
}

n1 = {
    'url': "https://tumen.n1.ru/kupit/kvartiry/",
    'card_data': ['div', 'living-search-item'],
    "title": ["span", "link-text"],
    "link": ["span", "link-text"],
    "price": ["div", "living-list-card-price__item _object"],
    'address': ["div", "search-item-district"],
    "data": ["div", "living-list-card__params "],
    "time_ago": ["", ""],
    "pagination": ['li', "paginator-pages__item", -2],
    "paginator_params": 'page'
}


class Parser:
    def __init__(self, site_data, path, host, proxy_list, headers, page_count=2, full_parse=False):
        self.i = 0
        self.url = site_data["url"]
        self.site_data = site_data
        self.path = path
        self.host = host
        self.proxy_list = proxy_list
        self.headers = headers
        self.page_count = page_count
        self.full_parse = full_parse

    def get_html(self, params=None):
        r = requests.get(self.url, headers=self.headers, timeout=15, params=params)
        return r

    def get_parser_name(self):
        print("Parser for site " + self.url)

    def get_page_count(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return int(soup.find_all(self.site_data['pagination'][0], class_=self.site_data['pagination'][1])[
                       self.site_data['pagination'][2]].get_text(strip=True))

    def get_content(self, html):
        final_res = []
        soup = BeautifulSoup(html, 'html.parser')

        houses = soup.find_all(self.site_data['card_data'][0], class_=self.site_data['card_data'][1])
        for house in houses:
            if self.host == "https://www.domofond.ru":
                final_res.append({
                    'id': self.i,
                    "title": house.find(self.site_data['title'][0], class_=self.site_data['title'][1]).get_text(
                        strip=True),
                    "link": self.host + house.get('href'),
                    "price": house.find(self.site_data['price'][0], class_=self.site_data['price'][1]).get_text(
                        strip=True).replace("\n", ''),
                    'address': house.find(self.site_data['address'][0], class_=self.site_data['address'][1]).get_text(
                        strip=True),
                    "data": house.find(self.site_data['data'][0], class_=self.site_data['data'][1]).get_text(
                        strip=True),
                    "time_ago": house.find(self.site_data['time_ago'][0],
                                           class_=self.site_data['time_ago'][1]).get_text(
                        strip=True),
                })
            elif self.host == "https://tumen.n1.ru":
                final_res.append({
                    'id': self.i,
                    "title": house.find(self.site_data['title'][0], class_=self.site_data['title'][1]).get_text(
                        strip=True),
                    "link": self.host + house.find(self.site_data['link'][0], class_=self.site_data['link'][1]).get(
                        'href'),
                    "price": house.find(self.site_data['price'][0], class_=self.site_data['price'][1]).get_text(
                        strip=True).replace("\n", ''),
                    'address': house.find(self.site_data['address'][0], class_=self.site_data['address'][1]).get_text(
                        strip=True),
                    "data": "",
                    "time_ago": house.find(self.site_data['time_ago'][0],
                                           class_=self.site_data['time_ago'][1]).get_text(
                        strip=True),
                })
            else:
                final_res.append({
                    'id': self.i,
                    "title": house.find(self.site_data['title'][0], class_=self.site_data['title'][1]).get_text(
                        strip=True),
                    "link": self.host + house.find(self.site_data['link'][0], class_=self.site_data['link'][1]).get(
                        'href'),
                    "price": house.find(self.site_data['price'][0], class_=self.site_data['price'][1]).get_text(
                        strip=True).replace("\n", ''),
                    'address': house.find(self.site_data['address'][0], class_=self.site_data['address'][1]).get_text(
                        strip=True),
                    "data": house.find(self.site_data['data'][0], class_=self.site_data['data'][1]).get_text(
                        strip=True),
                    "time_ago": house.find(self.site_data['time_ago'][0],
                                           class_=self.site_data['time_ago'][1]).get_text(
                        strip=True),
                })
            self.i += 1
        return final_res

    def save_data(self, result):
        with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["id", "Название", 'Ссылка', "Цена", "Адресс", "Застройщик", "Время создания"])
            for item in result:
                print(item['time_ago'])
                writer.writerow(
                    [item['id'], item['title'], item['link'], item['price'], item['address'], item['data'],
                     item['time_ago']])

    async def parse(self):
        final_res = []
        page = self.get_html()
        if page.status_code == 200:
            # if page.text.find("Подождите, идет загрузка"):
            #     print("CAPTCHA Error")
            if self.full_parse:
                page_count = self.get_page_count(page.text) + 1
            else:
                page_count = self.page_count + 1
            # page_count = 2
            for i in range(1, page_count):
                page = self.get_html({self.site_data['paginator_params']: i})
                await asyncio.sleep(5)
                final_res += self.get_content(page.text)
                print(
                    f'Папсинг страницы {i} из {self.get_page_count(page.text)}, на сайте {self.host}, количество объявлений: ' + str(
                        final_res.__len__()))
            self.save_data(final_res)
        else:
            print("Error")


async def main():
    pd = Parser(site_data=domofond, path=PATH_domofond, host=HOSTD, proxy_list=PROXY_LIST, headers=Headers)
    p = Parser(site_data=avito, path=PATH, host=HOST, proxy_list=PROXY_LIST, headers=Headers)
    # pn = Parser(site_data=n1, path=PATH_n1, host=hostn1, proxy_list=PROXY_LIST, headers=Headers)
    task = asyncio.create_task(p.parse())
    await asyncio.gather(task)


asyncio.run(main())
