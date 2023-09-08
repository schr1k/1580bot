import pandas as pd
import json

df = pd.read_excel('https://lycu1580.mskobr.ru/files/attach_files/rasp1k.xlsx', sheet_name='Расписание').T.values.tolist()

for i in df:
    for j in range(2, 10):
        print(i[j])
with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(df, f, indent=4, ensure_ascii=False)
