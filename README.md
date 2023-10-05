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
4. Change credentials in config.py.
```python
TOKEN = 'Token from BotFather'
IDEAS_GROUP_ID = '-1001796292186'
APPROVED_IDEAS_GROUP_ID = '-1001930546995'

SCHEDULE_PATH = '<absolute path to schedule.json>'
TEACHERS_PATH = '<absolute path to teachers.json>'
PROJECT_PATH = '<absolute path to project directory>'

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
    role VARCHAR
)
```
