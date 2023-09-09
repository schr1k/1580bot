import pandas as pd
import simplejson as json

df = pd.read_excel('https://lycu1580.mskobr.ru/files/attach_files/rasp1k.xlsx', sheet_name='Расписание').T.values.tolist()

with open('excel.json', 'w', encoding='utf-8') as f:
    json.dump(df, f, indent=4, ensure_ascii=False, ignore_nan=True)
