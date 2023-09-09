import json

with open('../excel/schedule.json', encoding='utf-8') as f:
    sl = json.load(f)


def make_schtext(group, day):
    day_schedule = sl[group][day]
    s = f'{day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict:
            s += f'{key}й урок - {value["lesson"]}, в {value["cabinet"]}\n'
    return s


def text_find_teacher(name, day):
    s = f'{day}:\n'
    for key, value in sl.items():
        for k, v in value[day].items():
            if type(v) is dict:
                if name in v["teacher"] and f'на {k}м уроке' not in s:
                    s += f'на {k}м уроке {name} в {v["cabinet"]}\n'
    return s


print(text_find_teacher('Богатин А.А.', 'Среда'))
