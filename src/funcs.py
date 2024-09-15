import json
from src.config import Config

config = Config()


def get_schedule() -> dict:
    """
    Get full school schedule in json format
    :return: :class:`dict`: full school schedule in json format
    """
    with open('public/json/schedule.json', encoding='utf-8') as f:
        return json.load(f)


def get_teachers() -> dict:
    """
    Get full teacher schedule in json format
    :return: :class:`dict`: full teacher schedule in json format
    """
    with open('public/json/teachers.json', encoding='utf-8') as f:
        return json.load(f)


def get_students_day_schedule(group: str, day: str) -> str:
    """
    Get formated schedule for provided group on specified weekday
    :param group: group name
    :param day: weekday
    :return: :class:`str`: formated schedule for provided group on specified weekday
    """
    if day not in get_schedule()[group].keys():
        return f'В {day} у {group} нет уроков.'
    day_schedule = get_schedule()[group][day]
    s = f'Расписание для {group} на {day}:\n'
    for key, value in day_schedule.items():
        if type(value) is dict:
            if 'cabinet' in value.keys():
                if value['cabinet'] is not None:
                    s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>, в <b>{value["cabinet"]}</b>\n'
                else:
                    s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>\n'
            else:
                s += f'<b>{key}</b> урок - <b>{value["lesson"]}</b>\n'
    if s == f'Расписание для {group} на {day}:\n':
        return f'В {day} у {group} нет уроков.'
    return s


def get_teachers_day_schedule(surname: str, day: str) -> str:
    """
    Get formated schedule for provided teacher on specified weekday
    :param surname: Teacher's surname
    :param day: weekday
    :return: :class:`str`: formated schedule for provided teacher on specified weekday
    """
    s = f'{day}:\n'
    st = {}
    for key, value in get_schedule().items():
        if day in value.keys():
            for k, v in value[day].items():
                if type(v) is dict:
                    if v is not None and v["teacher"] is not None and surname == v["teacher"].split(' ')[0]:
                        st[k] = {}
                        if "cabinet" in v.keys():
                            st[k]["cabinet"] = v['cabinet']
                        st[k]['teacher'] = v["teacher"]
                        st[k]["building"] = v["building"]
    sst = {}
    for i in sorted(list(st.keys()), key=lambda x: int(x)):
        sst[i] = st[i]
    for key, value in sst.items():
        if 'cabinet' in value.keys():
            s += f'На <b>{key}</b> уроке <b>{value["teacher"]}</b> в <b>{value["cabinet"] if value["cabinet"] is not None else "неопознанном кабинете"} (в {value["building"]} корпусе)</b>\n'
        else:
            s += f'Не указан кабинет, в котором <b>{value["teacher"]}</b> на <b>{key}</b> уроке\n'
    if len(s) == len(day + ':\n'):
        s = f'В {day} у выбранного учителя нет уроков'
    return s
