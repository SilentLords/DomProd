import asyncio
import csv
import re
import requests
from bs4 import BeautifulSoup
PROXY_LIST = [{
    'http': 'Selmrniki002:T2d2DiW@194.38.11.45:45785',
}]
DEBUG = False
house_info = []
async def avitoparse(parser_num, parsers_count=6):
    with open('../../Data/ParcerCards/res.csv', 'r') as file:
        a = file.read().splitlines()
    a.pop(0)
    adding = 0
    count = a.__len__() // parsers_count
    mod = a.__len__() % parsers_count
    if parser_num == parsers_count:
        print('last')
        adding = mod
    print(
        f'Parser num: {parser_num}, Parser count: {parsers_count}, Count: {count}, Count for num: {count * parser_num + adding}')
    if DEBUG:
        pass
    else:
        await get_data(a, parser_num, count, adding)


async def get_data(a, parser_num, count, adding):
    for item in range(0,3):
        splited_line = a[item].split(';')
        Headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.129',
            'accept': '*/*',
            'referer': splited_line[2]}




        print(splited_line[2])
        r = requests.get(splited_line[2], headers=Headers, timeout=5, proxies = PROXY_LIST[0])
        imgs = []
        soup = BeautifulSoup(r.text, 'html.parser')
        divs = soup.find_all('div', {'class': 'gallery-img-wrapper'})
        for d in divs:
            imgs.append(d.find('div', {'class': 'gallery-img-frame'}))
        # print(divs)
        # print(imgs)
        # i = 0
        # for img in imgs:
        #     style = img.get('data-url')
        #     href = style.replace('https://', '').replace('http://', '').replace("//", '')
        #     await save_img(href, id=splited_line[0], i=i)
        #     i += 1
        # i = 0
        links = soup.find('ul', {'class': 'item-params-list'})
        result = links.get_text().split(' \n ')
        num = await get_phone(Headers, splited_line)
        await collect_and_save_info(num, result, splited_line)
        print(parser_num, 'wait')
        await asyncio.sleep(6)


async def save_img(link, id, i):
    with open(f'../../media/photos/{id}_photo_{i}.jpg', 'bw')as photo:
        r = requests.get(" http://" + link)
        photo.write(r.content)


async def collect_and_save_info(num, result, splited_line):
    type_of_participation, official_builder, name_of_build, decoration, floor, floor_count, house_type, num_of_rooms, total_area, living_area, kitchen_area, deadline = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    for info_colum in result:
        info_colum = info_colum.replace('\n', '').replace(r"\xa", '')
        # print(info_colum)
        if re.findall(r"Этажей в доме", info_colum):
            info_colum = info_colum.replace('Этажей', '')
        # await asyncio.sleep(2)
        if re.search(r'Тип участия', info_colum):
            type_of_participation = info_colum.split(':')[1]
        elif re.search(r'Официальный застройщик', info_colum):
            official_builder = info_colum.split(':')[1]
        elif re.search(r'Название новостройки', info_colum):
            name_of_build = info_colum.split(':')[1]
        elif re.search(r'Отделка', info_colum):
            decoration = info_colum.split(':')[1]
        elif re.search(r'Этаж', info_colum):
            floor = info_colum.split(':')[1]
        elif re.search(r'в доме', info_colum):
            floor_count = info_colum.split(':')[1]
        elif re.search(r'Тип дома', info_colum):
            house_type = info_colum.split(':')[1]
        elif re.search(r'Количество комнат', info_colum):
            num_of_rooms = info_colum.split(':')[1]
        elif re.search(r'Общая площадь', info_colum):
            total_area = info_colum.split(':')[1]
        elif re.search(r'Жилая площадь', info_colum):
            living_area = info_colum.split(':')[1]
        elif re.search(r'Площадь кухни', info_colum):
            kitchen_area = info_colum.split(':')[1]
        elif re.search(r'Срок сдачи', info_colum):
            deadline = info_colum.split(':')[1]
    house_info.append({
        'id': splited_line[0],
        "type_of_participation": type_of_participation,
        "official_builder": official_builder,
        "name_of_build": name_of_build,
        "decoration": decoration,
        "floor": floor,
        "floor_count": floor_count,
        "house_type": house_type,
        "num_of_rooms": num_of_rooms,
        "total_area": total_area,
        "living_area": living_area,
        "kitchen_area": kitchen_area,
        "deadline": deadline,
        'phone': num
    })


async def get_phone(Headers, splited_line):
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    url_to_phone = f'https://m.avito.ru/api/1/items/{splited_line[2].split("._")[1]}/phone'
    number_req = requests.get(url_to_phone, headers=Headers, params={'key': key})
    num = number_req.text.split('2B')[1].replace('"}}}', '')
    return num


class ParseInfo:
    def __init__(self, host_id, parser_num):
        self.host_id = host_id
        self.parser_num = parser_num

    async def main(self):
        if self.host_id == 1:
            await avitoparse(parser_num=self.parser_num, parsers_count=6)


w1 = ParseInfo(1, 1)
w2 = ParseInfo(1, 2)
w3 = ParseInfo(1, 3)
w4 = ParseInfo(1, 4)
w5 = ParseInfo(1, 5)
w6 = ParseInfo(1, 6)


def save_data(result, host):
    with open(f'../../Data/ParcerInfo/res_info.{host}.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        print(result)
        writer.writerow(
            ["id", "type_of_participation", 'official_builder', "name_of_build", "decoration", "floor", "floor_count",
             'house_type', 'num_of_rooms', 'total_area', 'living_area', 'kitchen_area', 'deadline', 'phone'])
        for item in result:
            writer.writerow(
                [item["id"], item["type_of_participation"], item['official_builder'], item["name_of_build"],
                 item["decoration"], item["floor"], item["floor_count"], item['house_type'], item['num_of_rooms'],
                 item['total_area'], item['living_area'], item['kitchen_area'], item['deadline'], item['phone']])


async def main():
    task1 = asyncio.create_task(w1.main())
    # task2 = asyncio.create_task(w2.main())
    # task3 = asyncio.create_task(w3.main())
    # task4 = asyncio.create_task(w4.main())
    # task5 = asyncio.create_task(w5.main())
    # task6 = asyncio.create_task(w6.main())
    # await asyncio.gather(task1, task2, task3, task4, task5, task6)
    await asyncio.gather(task1)
    save_data(house_info, host='www.avito.ru')


asyncio.run(main())
