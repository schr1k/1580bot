import logging
import schedule as sch
import time
from threading import Thread
from datetime import datetime

from src.one.main import make_schedule_1
from src.two.main import make_schedule_2
from src.three.high.main import make_schedule_3h
from src.three.primary.main import make_schedule_3p
from src.four.high.main import make_schedule_4h
from src.four.primary.main import make_schedule_4p
from src.food.main import parse_menu


logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


def schedules():
    t1 = Thread(target=make_schedule_1)
    t2 = Thread(target=make_schedule_2)
    t3 = Thread(target=make_schedule_3h)
    t4 = Thread(target=make_schedule_3p)
    t5 = Thread(target=make_schedule_4h)
    t6 = Thread(target=make_schedule_4p)
    t1.run()
    t2.run()
    t3.run()
    t4.run()
    t5.run()
    t6.run()


def menus():
    t1 = Thread(target=parse_menu)
    t1.run()


def run_schedules():
    schedules()
    print(f'Расписание обновлено ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')


def run_menus():
    menus()
    print(f'Меню обновлено ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')


def start_scheduler():
    sch.every().day.at('20:00').do(run_schedules)
    sch.every().hour.do(run_menus)
    while True:
        sch.run_pending()
        time.sleep(1)

