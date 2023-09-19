import json
from bot.config import SCHEDULE_PATH


def get_json():
    with open(SCHEDULE_PATH, encoding='utf-8') as f:
        return json.load(f)


def get_student_day_schedule(group: str, day: str) -> str:
    day_schedule = get_json()[group][day]
    s = f'Расписание для {group} в {day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict and 'cabinet' in value.keys():
            s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>, в <b>{value["cabinet"]}</b>.\n'
        elif type(value) is dict:
            s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>\n'
    if s == f'Расписание для {group} в {day}:\n':
        return f'В {day} у {group} нет уроков'
    return s


def get_teachers_day_schedule(surname: str, day: str) -> str:
    s = f'{day}:\n'
    st = {}
    c = 0
    for key, value in get_json().items():
        for k, v in value[day].items():
            if type(v) is dict:
                if surname in v["teacher"]:
                    st[k] = {}
                    st[k]["cabinet"] = v['cabinet']
                    st[k]['teacher'] = v["teacher"]
                    c += 1
    sst = {}
    for i in sorted(list(st.keys()), key=lambda x: int(x)):
        sst[i] = st[i]
    for key, value in sst.items():
        s += f'На <b>{key}</b> уроке <b>{value["teacher"]}</b> в <b>{value["cabinet"]}</b>.\n'
    if c == 0:
        s = 'Учитель не найден'
    elif len(s) == len(day + ':\n'):
        s = f'В этот день {surname} нет в школе'
    return s
