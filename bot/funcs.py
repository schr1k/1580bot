import json
from collections import OrderedDict


def get_json(path_to_json):
    with open(path_to_json, encoding='utf-8') as f:
        return json.load(f)


def get_day_schedule(group, day, path_to_json):
    day_schedule = get_json(path_to_json)[group][day]
    s = f'{day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict:
            s += f'{key}й урок - {value["lesson"]}, в {value["cabinet"]}\n'
    return s


def get_teachers_day_schedule(surname: str, day: str, path_to_json) -> str:
    s = f'{day}:\n'
    st = {}
    c = 0
    for key, value in get_json(path_to_json).items():
        for k, v in value[day].items():
            if type(v) is dict:
                if surname in v["teacher"]:
                    st[k] = v['cabinet']
                    c += 1
    st = dict(OrderedDict(sorted(st.items())))
    for key, value in st.items():
        s += f'на {key}м уроке {surname} в {st[key]}\n'
    if c == 0:
        s = 'Такого учителя нет в корпусе'
    elif len(s) == len(day + ':\n'):
        s = f'В этот день {surname} нет в школе'
    return s

