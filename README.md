## Plain setup:

1. Create virtual environment.
```bash
python -m venv venv
```
2. Activate it.

* On windows: 
```bash
venv/Scripts/activate
```

* On linux: 
```bash
source venv/bin/activate
```

3. Install requirements.
```bash
pip install -r requirements.txt
```
4. Download [poppler](https://github.com/oschwartz10612/poppler-windows/releases/).
5. Change credentials in `.env`.
```dotenv
# Telegram
TOKEN='Bot token'
IDEAS_GROUP_ID='id of ideas group'
APPROVED_IDEAS_GROUP_ID='id of approved ideas group'
BUGS_GROUP_ID='id of bugs group'

# Paths
SCHEDULE_PATH='Absolute path to schedule.json'
TEACHERS_PATH='Absolute path to teachers.json'
POPPLER_PATH='Absolute path to bin directory of poppler'
PROJECT_PATH='Absolute path to project directory'

# Postgres
POSTGRES_HOST='localhost'
POSTGRES_PORT=5432
POSTGRES_DB='1580'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'

# Redis
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_DB=0
```

6. Create tables.

```postgresql
CREATE TABLE users (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    class VARCHAR,
    building VARCHAR
);

CREATE TABLE staff (
    id SERIAL,
    tg VARCHAR,
    username VARCHAR,
    role VARCHAR
);

```

7. Run [main.py](main.py)

## Docker setup:
1. Install [docker](https://docs.docker.com/engine/install/).
2. Run app.

```bash
docker compose up --build
```