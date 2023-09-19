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
ADMINS = ['Your telegram id']
SCHEDULE_PATH = '<absolute path to>/schedule.json'

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'
POSTGRES_DB = '1580'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
```

## SQL:
1. users table.
```postgresql
CREATE TABLE users (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    class VARCHAR
)
```