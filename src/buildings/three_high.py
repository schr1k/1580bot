import pandas as pd
import simplejson as json

from src.config import Config

config = Config()


def make_schedule_3h():  # https://lycu1580.mskobr.ru/files/schedule/rasp_3k_ns.xlsx
    df = pd.read_excel('https://lycu1580.mskobr.ru/files/schedule/sch3k_2.xlsx', header=None, engine='openpyxl').T.values.tolist()
    with open('public/json/buildings/3h.json', 'w', encoding='utf-8') as f:
        json.dump(df, f, indent=4, ensure_ascii=False, ignore_nan=True)

    with open('public/json/buildings/3h.json', encoding='utf-8') as f:
        excel = json.load(f)

    excel = excel[2:]

    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    schedule = {}

    for column in range(len(excel)):
        group = str(excel[column][0]).lower()
        for c, i in enumerate(range(1, len(excel[column]), 8)):
            lessons = excel[column][i: i + 8]
            for j in range(len(lessons)):
                if lessons[j] is not None:
                    sp = str(lessons[j]).split('\n')
                    if len(sp) == 2:
                        sl = {'lesson': sp[0].strip(), 'teacher': sp[1].strip(), 'building': '3'}
                    elif len(sp) == 3:
                        sl = {'lesson': ' '.join(sp[:2]).strip(), 'teacher': sp[2].strip(), 'building': '3'}
                    else:
                        st = sp[0]
                        if st == 'Русский язык Петковская В.Н.':
                            sl = {'lesson': 'Русский язык', 'teacher': 'Петковская В.Н.', 'building': '3'}
                        elif st == 'Математика Петковская В.Н.':
                            sl = {'lesson': 'Математика', 'teacher': 'Петковская В.Н.', 'building': '3'}
                        elif st == 'Хочу всё знать Котлярова Я.Ю ДО':
                            sl = {'lesson': 'Хочу всё знать', 'teacher': 'Котлярова Я.Ю', 'building': '3'}
                        elif st == 'Физическая культура':
                            sl = {'lesson': 'Физическая культура', 'teacher': 'Неизвестно', 'building': '3'}
                        elif st == 'Музыка Котлярова Я.Ю.':
                            sl = {'lesson': 'Музыка', 'teacher': 'Котлярова Я.Ю.', 'building': '3'}
                        elif st == 'расписание':
                            sl = {'lesson': 'расписание', 'teacher': 'Неизвестно', 'building': '3'}
                        else:
                            sl = {'lesson': st, 'teacher': 'Неизвестно', 'building': '3'}
                    lessons[j] = sl
            day_schedule = {}
            for lesson_number, j in zip(range(1, 9), list(lessons)):
                day_schedule[lesson_number] = j
            day_schedule = {i: j for i, j in zip(range(1, 9), lessons)}
            if group in schedule:
                if c < len(weekdays):
                    if weekdays[c] in schedule[group]:
                        schedule[group][weekdays[c]] = day_schedule
                    else:
                        schedule[group][weekdays[c]] = {}
                        schedule[group][weekdays[c]] = day_schedule
            else:
                schedule[group] = {}
                if weekdays[c] in schedule[group]:
                    schedule[group][weekdays[c]] = day_schedule
                else:
                    schedule[group][weekdays[c]] = {}
                    schedule[group][weekdays[c]] = day_schedule

    with open('public/json/schedule.json', 'r', encoding='utf-8') as f:
        all_schedule = json.load(f)

    for i, j in schedule.items():
        all_schedule[i] = j

    with open('public/json/schedule.json', 'w', encoding='utf-8') as f:
        json.dump(all_schedule, f, indent=4, ensure_ascii=False)
