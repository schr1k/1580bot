import pandas as pd
import simplejson as json

from src.config import Config

config = Config()


def make_schedule_4h():  # https://lycu1580.mskobr.ru/files/schedule/rasp_symbol_2.xlsx
    df = pd.read_excel('https://lycu1580.mskobr.ru/files/schedule/sch4k_1.xls', header=None).T.values.tolist()
    with open('public/json/buildings/4h.json', 'w', encoding='utf-8') as f:
        json.dump(df, f, indent=4, ensure_ascii=False, ignore_nan=True)

    with open('public/json/buildings/4h.json', encoding='utf-8') as f:
        excel = json.load(f)

    excel = excel[2:46] + excel[48:]

    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

    schedule = {}

    for column in range(len(excel))[::2]:
        group = str(excel[column][0]).lower()
        for c, i in enumerate(range(0, len(excel[column]), 9)):
            lessons = list(zip(excel[column][i + 1: i + 9], excel[column + 1][i + 1: i + 9]))
            for j in range(len(lessons)):
                if lessons[j] is not None and lessons[j][0] is not None:
                    sp = lessons[j][0].split('\n')
                    sp.append(lessons[j][1])
                    if len(sp) == 3:
                        sl = {'lesson': sp[0], 'teacher': sp[1], 'cabinet': sp[2], 'building': '4'}
                    else:

                        sl = {'lesson': sp[0][:36], 'teacher': sp[0][37:], 'cabinet': sp[1], 'building': '4'}
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
