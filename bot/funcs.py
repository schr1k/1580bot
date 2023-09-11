import json


def get_json(path_to_json):
    with open(path_to_json, encoding='utf-8') as f:
        return json.load(f)


def get_student_day_schedule(group: str, day: str, path_to_json: str) -> str:
    day_schedule = get_json(path_to_json)[group][day]
    s = f'Расписание для {group} в {day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict:
            s += f'{key} урок - {value["lesson"]}, в {value["cabinet"]}.\n'
    if s == f'Расписание для {group} в {day}:\n':
        return f'В {day} у {group} нет уроков'
    return s
# TODO(Матвей): выдавать 'В <день> у <класс> нет уроков при отсутствии уроков'
# TODO(Матвей): выдавать 'Расписание для <класс> в <день>'


def get_teachers_day_schedule(surname: str, day: str, path_to_json: str) -> str:
    s = f'{day}:\n'
    st = {}
    c = 0
    for key, value in get_json(path_to_json).items():
        for k, v in value[day].items():
            if type(v) is dict:
                if surname in v["teacher"]:
                    st[k] = v['cabinet']
                    c += 1
    sst = {}
    for i in sorted(list(st.keys()), key=lambda x: int(x)):
        sst[i] = st[i]
    for key, value in sst.items():
        s += f'На {key} уроке {surname} в {sst[key]}.\n'
    if c == 0:
        s = 'Учитель не найден'
    elif len(s) == len(day + ':\n'):
        s = f'В этот день {surname} нет в школе'
    return s
