import pandas as pd
import json
from src.config import Config

config = Config()


def parse_teachers():
    df = pd.read_excel(f'{config.PROJECT_PATH}/src/teachers/emails.xlsx').values.tolist()
    teachers = {}
    for i in df:
        teachers[i[0]] = {
            'surname': i[1].strip(),
            'name': i[2].strip(),
            'patronymic': i[3].strip(),
            'email': i[4].strip(),
            'photo': False,
            'subject': None
        }

    with open('public/json/teachers.json', 'w', encoding='utf-8') as f:
        json.dump(teachers, f, indent=4, ensure_ascii=False)
