from .models import HouseModel, HouseInfo, Image


def get_info():
    with open(r'/Users/nikitatonkoskurov/PycharmProjects/domofound2/Data/ParcerInfo/res_info.www.avito.ru.csv', 'r',
              encoding='utf8') as file:
        a = file.read().splitlines()
    a.pop(0)
    _id = []
    for lines in a:
        splited_line = lines.split(';')
        for i in range(len(splited_line)):
            print(splited_line[i], i)

        house_id = HouseInfo.objects.update_or_create(
            type_of_participation=splited_line[1],
            official_builder=splited_line[2],
            name_of_build=splited_line[3],
            decoration=splited_line[4],
            floor=splited_line[5],
            floor_count=splited_line[6],
            house_type=splited_line[7],
            num_of_rooms=1,
            total_area=splited_line[9],
            kitchen_area=splited_line[10],
            deadline=splited_line[12],
            phone=splited_line[13])
        print(house_id)
    get_photos()
    return _id


def reparse():
    with open(r'/Users/nikitatonkoskurov/PycharmProjects/domofound2/Data/ParcerCards/res.csv', 'r',
              encoding='utf8') as file:
        a = file.read().splitlines()
    a.pop(0)
    _id = get_info()
    i = 0
    for lines in a:
        splited_line = lines.split(';')
        print(splited_line)
        HouseModel.objects.update_or_create(title=splited_line[1], link=splited_line[2],
                                            price=int(splited_line[3].replace('₽', '').replace(' ', '')),
                                            address=splited_line[4], data=splited_line[5], Host='http://avito.ru',
                                            house_info=HouseInfo.objects.get(id=_id[i] if i < _id.__len__() else 1))
        i += 1
    print("reparse complete")


def get_photos():
    pass
