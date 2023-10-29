## Setup:
1. Create virtual environment.
```bash
python -m venv venv
```
2. Activate it.
```bash
venv/bin/activate
```
3. Install requirements.
```bash
pip install -r requirements.txt
```
4. Download [poppler](https://github.com/oschwartz10612/poppler-windows/releases/).
5. Change credentials in config.py.
```python
TOKEN = '6531558275:AAEm3wMfef9u26G8DtCGjztZ_QOP1X7nbxA'
IDEAS_GROUP_ID = '-1001796292186'
APPROVED_IDEAS_GROUP_ID = '-1001930546995'
BUGS_GROUP_ID = '-1002054325044'

SCHEDULE_PATH = 'Absolute path to schedule.json'
TEACHERS_PATH = 'Absolute path to teachers.json'
POPPLER_PATH = 'Absolute path to bin directory of poppler'
PROJECT_PATH = 'Absolute path to project directory'

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = '1580'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
```

## SQL:
1. #### Users:
```postgresql
CREATE TABLE users (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    class VARCHAR,
    building VARCHAR
)
```
2. #### Staff:
```postgresql
CREATE TABLE staff (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    role VARCHAR
)
```
