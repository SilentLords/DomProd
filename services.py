import requests as r

API_KEY = '0524ce2f-6067-4ba3-9506-6268f7348498&'
DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

def get_cord(address):
    req = r.get(
        f'https://geocode-maps.yandex.ru/1.x?geocode={address}&apikey={API_KEY}&format=json')
    decoded_hand = req.json()
    try:
        if decoded_hand['response']['GeoObjectCollection']['featureMember']:
            x = float(
                decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[
                    0])
            y = float(
                decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[
                    1])
            address = \
            decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            return x, y, address
        else:
            return 0, 0, address
    except:
        return 0, 0, address

