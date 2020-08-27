import json
import os
import shutil

import requests as r
import xmltodict
import xmljson
import xml.etree.cElementTree as ET

url = 'https://api.reformagkh.ru/api'
headers = {'content-type': 'application/soap+xml'}
SERVICE_TYPES = ["Работы (услуги) по управлению многоквартирным домом",
                 "Работы по содержанию помещений, входящих в состав общего имущества в многоквартирном доме",
                 "Работы по обеспечению вывоза бытовых отходов",
                 "Работы по содержанию и ремонту конструктивных элементов (несущих конструкций и ненесущих конструкций) многоквартирных домов",
                 "Работы по содержанию и ремонту оборудования и систем инженерно-технического обеспечения, входящих в состав имущества в многоквартирном доме",
                 "Работы по содержанию и ремонту мусоропроводов в многоквартирном доме",
                 "Работы по содержанию и ремонту лифта (лифтов) в многоквартирном доме",
                 "Работы по обеспечению требований пожарной безопасности",
                 "Работы по содержанию и ремонту систем дымоудаления и вентиляции",
                 "Работы по содержанию и ремонту систем внутридомового газового оборудования",
                 "Обеспечение устранения аварий на внутридомовых инженерных системах в многоквартирном доме",
                 "Проведение дератизации и дезинсекции помещений, входящих в состав общего имущества в многоквартирном доме",
                 "Работы по содержанию земельного участка с элементами озеленения и благоустройства, иными объектами, предназначенными для обслуживания и эксплуатации многоквартирного дома",
                 "Прочая работа (услуга)"]
WALL_TYPES = ["Каменные, кирпичные",
              'Панельные',
              'Блочные',
              'Смешанные',
              'Деревянные',
              'Монолитные',
              'Иные',
              'Не заполнено',
              'Керамзитобетон (блоки)',
              'Железобетон',
              'Керамзитобетон',
              'Железобетонная панель',
              'Керамзитобетонная 1-слойная панель',
              'Ж/б 3-х слойная панель с утеплителем',
              'Шлакобетон (блоки)',
              'Шлакокерамзитобетонная 1-слойная панель']
HOUSE_HITTING_TYPE = ["Отсутствует",
                      "Центральное",
                      "Автономная котельная (крышная, встроенно-пристроенная)",
                      "Квартирное отопление (квартирный котел)",
                      "Печное",
                      "Электроотопление",
                      "Индивидуальный тепловой пункт (ИТП)",
                      "Газовая колонка"]
TRASH_TYPE = ["Отсутствует",
              "Квартирные",
              "На лестничной клетке",
              "Сухой (холодный)",
              "Сухой",
              "Холодный",
              "Огневой (горячий)",
              "Мокрый"]


def get_reporting_period_id(session_id):
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="https://api.reformagkh.ru/api_document_literal">
   <soapenv:Header>
      <authenticate>{session_id}</authenticate>
   </soapenv:Header>
   <soapenv:Body>
      <api:GetReportingPeriodList/>
   </soapenv:Body>
</soapenv:Envelope>"""
    a = r.post(url, data=body.encode('utf-8'))
    new_json_from_xml = xmltodict.parse(a.text)
    for item in new_json_from_xml['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetReportingPeriodListResponse']['return'][
        'item']:
        if item["is_988"]['#text'] == 'true':
            return item['id']['#text']


def get_house_info_by_jkh_id(house_id_for, session_id_for, report_id):
    print(house_id_for, session_id_for)
    body_ = f"""<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="https://api.reformagkh.ru/api">
<soapenv:Header>
    <authenticate>{session_id_for}</authenticate>
</soapenv:Header>
   <soapenv:Body>
      <api:GetHouseProfile988 soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <house_id xsi:type="xsd:int">{house_id_for}</house_id>
         <reporting_period_id xsi:type="xsd:int">{report_id}</reporting_period_id>
      </api:GetHouseProfile988>
   </soapenv:Body>
</soapenv:Envelope>"""

    a_ = r.post(url=url, data=body_.encode('utf-8'), headers=headers)
    return a_.text


def get_fias_id(addr='обл. Тюменская, г. Тюмень, ул. Камчатская, д. 1'):
    body = {
        'addr': f'{addr}'
    }
    request = r.post('https://gate.brainysoft.ru/outside/fias/fastmoney/getFiasId', data=body)
    try:
        fias_id = request.json()['data']['fias_id']
    except:
        fias_id = None
    return fias_id


def get_jkh_info(address):
    body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="https://api.reformagkh.ru/api_document_literal">
       <soapenv:Header/>
       <soapenv:Body>
          <api:Login>
             <login>OtsoSilver</login>
             <password>Vbhevbh123</password>
          </api:Login>
       </soapenv:Body>
    </soapenv:Envelope>"""
    a = r.post(url=url, data=body.encode('utf-8'), headers=headers)
    with open('1.xml', 'w') as f:
        f.write(a.text)
    root = ET.parse('1.xml').getroot()
    for item in root.iter('return'):
        session_id = item.text
    report_id = get_reporting_period_id(session_id)
    fias_id = get_fias_id(addr=address)
    body = f'''
             <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:api="https://api.reformagkh.ru/api_document_literal">
       <soapenv:Header>
          <authenticate>{session_id}</authenticate>
       </soapenv:Header>
       <soapenv:Body>
          <api:GetHouseInfo>
             <address>
                <!--You may enter the following 6 items in any order-->
                <houseguid>{fias_id}</houseguid>
             </address>
          </api:GetHouseInfo>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    print(fias_id)
    a = r.post(url=url, data=body.encode('utf-8'), headers=headers)
    xml_response= xmltodict.parse(a.text)
    print(json.dumps(xml_response, indent=3, sort_keys=True))
    house_id = xml_response['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetHouseInfoResponse']['return']['item']['house_id']['#text']
    print(house_id)
    xml_dict = xmltodict.parse(get_house_info_by_jkh_id(house_id, session_id, report_id))
    print(xml_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body'])
    house_data = xml_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:GetHouseProfile988Response']['return'][
        'house_profile_data']
    if house_data['house_type']['#text'] == 1:
        house_type = 'Многоквартирный дом '
    if house_data['house_type']['#text'] == 2:
        house_type = 'Жилой дом блокированной застройки '
    if house_data['house_type']['#text'] == 3:
        house_type = 'Специализированный жилищный фонд '
    else:
        house_type = ''
    service_data = []
    with open('1.json', 'w') as f:
        f.write(json.dumps(house_data, sort_keys=True, indent=4))
    for item in house_data['services']['item']:
        try:
            service_data.append({'name': f'Название услуги: {SERVICE_TYPES[int(item["name"]["#text"]) - 1]}',
                                 'date': f'Дата оказания услуги: {item["costs"]["item"]["year"]["#text"]}'})
        except:
            service_data.append({'name': f'Название услуги: {SERVICE_TYPES[int(item["name"]["#text"]) - 1]}',
                                 'date': f'Дата оказания услуги: {item["costs"]["item"][0]["year"]["#text"]}'})
    if house_data['overhaul'].__len__() <= 1:
        overhaul = {}
    else:
        if house_data['overhaul']['provider_inn'].__len__() <=1:
            overhaul = {}
        else:
            overhaul = {
                'provider_inn': 'ИНН провайдера ' + house_data['overhaul']['provider_inn']['#text'],
                'provider_name': 'Имя провайдера ' + house_data['overhaul']['provider_name']['#text'],
                # 'cost_per_month': 'Цена за месяц ' + house_data['overhaul']['cost_per_month']['#text']
            }
    p = {
        "is_alarm": "Признак аварийности " + ('+' if house_data['is_alarm']["#text"] == 'true' else '-'),
        "exploitation_start_year": "Год введения в эксплутацию" + house_data['exploitation_start_year']['#text'],
        "built_year": "Год постройки" + house_data['built_year']['#text'],
        'services': service_data,
        'house_type': f'Тип дома: {house_type}',
        'project_type': f'Серия, тип постройки здания {house_data["built_year"]["#text"]}',
        'overhaul': overhaul,
        'elevators_count': 'Количество Лифтов: ' + house_data['elevators_count']["#text"],
        'wall_material': 'Материал стен: ' + WALL_TYPES[int(house_data['wall_material']["#text"]) - 1],
        'heating_type': 'Идентификатор типа системы теплоснабжения: ' + HOUSE_HITTING_TYPE[
            int(house_data['heating_type']["#text"]) - 1],
        'chute_type': 'Тип мусоропровода: ' + TRASH_TYPE[int(house_data['chute_type']["#text"]) - 1],
        'entrance_count': 'Количество подъездов, ед.: ' + house_data['entrance_count']["#text"],
        'floor_count_max': "Колво этажей наибольшее: " + house_data['floor_count_max']["#text"],
        'floor_count_min': "Колво этажей наименьшее: " + house_data['floor_count_min']["#text"],
        'has_playground': 'Детская площадка: ' + ('+' if house_data['has_playground']["#text"] == 'true' else '-'),
        'has_sportsground': 'Спорт площадка: ' + ('+' if house_data['has_sportsground']["#text"] == 'true' else '-')
    }
    print(p)
    return p


def create_archive_of_photos(photos, house_id):
    DEBUG = False

    if DEBUG:
        path = 'C:/Users/TalisMan701/PycharmProjects/Domafound/'
    else:
        path = '/var/www/dom/src/'
    try:
        os.makedirs(path + f'media/photos/{house_id}')
    except:
        pass
    for photo in photos:
        downloaded_file = r.get(photo)

        name_of_file = f'{path}media/photos/{house_id}/{photos.index(photo)}_{house_id}.jpg'
        with open(name_of_file, 'wb') as file:
            file.write(downloaded_file.content)

    shutil.make_archive(f'{path}media/{house_id}', 'zip', f'media/photos/{house_id}/')
    return f'https://api-domafound.ru/media/{house_id}.zip'
