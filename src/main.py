import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from src.buildings.one import make_schedule_1
from src.buildings.two import make_schedule_2
from src.buildings.three_primary import make_schedule_3p
from src.buildings.three_high import make_schedule_3h
from src.buildings.four_high import make_schedule_4h
from src.buildings.four_primary import make_schedule_4p
from src.food import parse_menu
from src.teachers.parser import parse_photo, parse_subject


logging.basicConfig(level=logging.INFO)


def schedules():
    try:
        make_schedule_1()
        make_schedule_2()
        make_schedule_3h()
        make_schedule_3p()
        make_schedule_4h()
        make_schedule_4p()
        logging.info('Расписание обновлено.')
    except Exception as e:
        logging.exception(e)


def menus():
    try:
        parse_menu()
        logging.info('Меню обновлено.')
    except Exception as e:
        logging.exception(e)


def teachers():
    try:
        parse_subject()
        parse_photo()
        logging.info('Учителя обновлены.')
    except Exception as e:
        logging.exception(e)


async def create_schedule():
    scheduler = AsyncIOScheduler()
    schedules()
    menus()
    teachers()
    scheduler.add_job(schedules, "interval", hours=24, start_date='2023-01-01 20:00:00', name='schedules')
    scheduler.add_job(teachers, "interval", hours=12, start_date='2023-01-01 20:00:00', name='teachers')
    scheduler.add_job(menus, "interval", hours=6, start_date='2023-01-01 20:00:00', name='menus')
    scheduler.start()
