import requests as r

API_KEY = '0524ce2f-6067-4ba3-9506-6268f7348498&'


# Тюмень ул. Николая Фёдорова, 17к1  р-н Восточный
def get_cord(address):
    print(address)
    req = r.get(
        f'https://geocode-maps.yandex.ru/1.x?geocode={address}&apikey={API_KEY}&format=json')
    decoded_hand = req.json()
    if decoded_hand['response']['GeoObjectCollection']['featureMember']:
        x = float(
            decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[
                0])
        y = float(
            decoded_hand['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[
                1])
        return x, y
    else:
        return 0, 0
