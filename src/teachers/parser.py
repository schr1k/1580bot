import json

import requests
from bs4 import BeautifulSoup

with open('public/json/teachers.json', 'r', encoding='utf-8') as f:
    teachers = json.load(f)

sl = {}


def parse_photo():
    data = requests.get('https://lycu1580.mskobr.ru/o-nas/pedagogicheskii-sostav')
    soup = BeautifulSoup(data.text, 'html.parser')
    for div in soup.findAll('div', class_='col-md-3 teacherblock'):
        if len(div.find('a', class_='fio').text.split()) == 3:
            surname, name, patronymic = div.find('a', class_='fio').text.split()
            if div.find('img') is not None:
                src = div.find('img', class_='photo_teacher')['src']
                for i, j in teachers.items():
                    if j['surname'] == surname and j['name'] == name and j['patronymic'] == patronymic:
                        teachers[i]['photo'] = True
                        p = requests.get(f'https://lycu1580.mskobr.ru/{src}')
                        with open(f'public/photo/teachers/{i}.jpg', 'wb') as f:
                            f.write(p.content)
        elif len(div.find('a', class_='fio').text.split()) == 2:
            surname, name = div.find('a', class_='fio').text.split()
            if div.find('img') is not None:
                src = div.find('img', class_='photo_teacher')['src']
                for i, j in teachers.items():
                    if j['surname'] == surname and j['name'] == name:
                        teachers[i]['photo'] = True
                        p = requests.get(f'https://lycu1580.mskobr.ru/{src}')
                        with open(f'src/public/photo/teachers/{i}.jpg', 'wb') as f:
                            f.write(p.content)

    if len(teachers.keys()) != 0:
        with open('public/json/teachers.json', 'w', encoding='utf-8') as f:
            json.dump(teachers, f, ensure_ascii=False, indent=4)


def parse_subject():
    data = requests.get('https://lycu1580.mskobr.ru/o-nas/pedagogicheskii-sostav')
    soup = BeautifulSoup(data.text, 'html.parser')
    for div in soup.findAll('div', class_='col-md-3 teacherblock'):
        if div.find('a', class_='fio') is not None:
            if len(div.find('a', class_='fio').text.split()) == 3:
                surname, name, patronymic = div.find('a', class_='fio').text.split()
                if div.find('div', class_='subject') is not None:
                    subject = div.find('div', class_='subject').text.strip()
                    for i, j in teachers.items():
                        if j['surname'] == surname and j['name'] == name and j['patronymic'] == patronymic:
                            teachers[i]['subject'] = subject
            elif len(div.find('a', class_='fio').text.split()) == 2:
                surname, name = div.find('a', class_='fio').text.split()
                if div.find('div', class_='subject') is not None:
                    subject = div.find('div', class_='subject').text.strip()
                    for i, j in teachers.items():
                        if j['surname'] == surname and j['name'] == name:
                            teachers[i]['subject'] = subject

    if len(teachers.keys()) != 0:
        with open('public/json/teachers.json', 'w', encoding='utf-8') as f:
            json.dump(teachers, f, ensure_ascii=False, indent=4)
