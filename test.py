import json

with open('excel.json', encoding='utf-8') as f:
    excel = json.load(f)

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

for i in range(len(excel)):
    sp = [excel[i][8]] + excel[i]
    excel[i] = sp

schedule = {}

for column in excel[2:-2:2]:
    for c, i in enumerate(range(0, len(column), 9)):
        class_name = column[0]
        day_schedule = {i: j for i, j in zip(range(1, 9), column[i + 1: i + 9])}
        if column[i] in schedule:
            if weekdays[c] in schedule[column[i]]:
                schedule[column[i]][weekdays[c]] = day_schedule
            else:
                schedule[column[i]][weekdays[c]] = {}
                schedule[column[i]][weekdays[c]] = day_schedule
        else:
            schedule[column[i]] = {}
            if weekdays[c] in schedule[column[i]]:
                schedule[column[i]][weekdays[c]] = day_schedule
            else:
                schedule[column[i]][weekdays[c]] = {}
                schedule[column[i]][weekdays[c]] = day_schedule

with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(schedule, f, indent=4, ensure_ascii=False)
