import requests as r

API_KEY = '0524ce2f-6067-4ba3-9506-6268f7348498&'


def get_cord(address):
    req = r.get(
        f'https://geocode-maps.yandex.ru/1.x?geocode={address}&apikey={API_KEY}&format=json')
    decoded_hand = req.json()
    y = float(
        decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[0])
    x = float(
        decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[1])
    return y, x
