import json

import pandas as pd

df = pd.read_json('schedule.json').T

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

js = dict()
for col in range(2, len(df)):
    psl = {}
    for i in weekdays:
        psl[i] = {i: j for i, j in zip(range(1, 9), df[col][:8])}
    js[df[col][8]] = psl


print(json.dumps(js, indent=4, ensure_ascii=False))
