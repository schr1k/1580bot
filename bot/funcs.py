import json
from bot.config import SCHEDULE_PATH, TEACHERS_PATH


def get_json():
    with open(SCHEDULE_PATH, encoding='utf-8') as f:
        return json.load(f)


def get_teachers():
    with open(TEACHERS_PATH, encoding='utf-8') as f:
        return json.load(f)


def get_student_day_schedule(group: str, day: str) -> str:
    day_schedule = get_json()[group][day]
    s = f'Расписание для {group} на {day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict and 'cabinet' in value.keys():
            s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>, в <b>{value["cabinet"]}</b>.\n'
        elif type(value) is dict:
            s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>.\n'
    if s == f'Расписание для {group} на {day}:\n':
        return f'В {day} у {group} нет уроков.'
    return s


def get_teachers_day_schedule(surname: str, day: str) -> str:
    s = f'{day}:\n'
    st = {}
    c = 0
    for i in get_teachers():
        if surname in i:
            c = 1
            break
    if c != 1:
        return 'Учитель не найден.'
    for key, value in get_json().items():
        if day in value.keys():
            for k, v in value[day].items():
                if type(v) is dict:
                    if v is not None and v["teacher"] is not None and surname in v["teacher"]:
                        st[k] = {}
                        st[k]["cabinet"] = v['cabinet']
                        st[k]['teacher'] = v["teacher"]
                        st[k]["building"] = v["building"]
    sst = {}
    for i in sorted(list(st.keys()), key=lambda x: int(x)):
        sst[i] = st[i]
    for key, value in sst.items():
        if 'cabinet' in value.keys():
            s += f'На <b>{key}</b> уроке <b>{value["teacher"]}</b> в <b>{value["cabinet"]}(в {value["building"]} корпусе)</b>.\n'
        else:
            s += f'Не указан кабинет, в котором <b>{value["teacher"]}</b> на <b>{key}</b> уроке.'
    if len(s) == len(day + ':\n'):
        s = f'В {day} у выбранного учителя нет уроков.'
    return s

