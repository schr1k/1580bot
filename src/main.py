import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from src.one.main import make_schedule_1
from src.two.main import make_schedule_2
from src.three.high.main import make_schedule_3h
from src.three.primary.main import make_schedule_3p
from src.four.high.main import make_schedule_4h
from src.four.primary.main import make_schedule_4p
from src.food.main import parse_menu
from src.teachers.parser import parse_photo, parse_subject


logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


def schedules():
    make_schedule_1()
    make_schedule_2()
    make_schedule_3h()
    make_schedule_3p()
    make_schedule_4h()
    make_schedule_4p()
    print(f'Расписание обновлено ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')


def menus():
    parse_menu()
    print(f'Меню обновлено ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')


def teachers():
    parse_subject()
    parse_photo()
    print(f'Учителя обновлены ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')


async def create_schedule():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(schedules, "interval", hours=24, start_date='2023-01-01 20:00:00')
    scheduler.add_job(teachers, "interval", hours=12, start_date='2023-01-01 20:00:00')
    scheduler.add_job(menus, "interval", hours=6, start_date='2023-01-01 20:00:00')
    scheduler.start()
