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


def get_teachers_schedule(name, day, path_to_json):
    s = f'{day}:\n'
    st = {}
    for key, value in get_json(path_to_json).items():
        for k, v in value[day].items():
            if type(v) is dict:
                if name in v["teacher"]:
                    st[k] = v['cabinet']
    st = dict(OrderedDict(sorted(st.items())))
    for key, value in st.items():
        s += f'на {key}м уроке {name} в {st[key]}\n'
    if len(s) == len(day + ':\n'):
        s = f'В этот день {name} нет в школе'
    return s

