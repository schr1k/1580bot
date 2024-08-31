from celery import Celery

from src.bot.db import config

app = Celery(
    'async_parser',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL,
    include=['async_parser.tasks'],
    accept=['json']
)

app.start()
