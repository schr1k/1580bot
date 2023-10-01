import asyncio
import logging
from excel.one.main import make_schedule_1
from excel.two.main import make_schedule_2
from excel.three.high.main import make_schedule_3h
from excel.three.primary.main import make_schedule_3p
from excel.four.high.main import make_schedule_4h
from excel.four.primary.main import make_schedule_4p
import schedule as sch
import time
from threading import Thread

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


def tasks():
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


def run_tasks():
    tasks()
    logging.info('Successfully updated schedule')
    return sch.CancelJob


def start_scheduler():
    sch.every().day.at('22:00').do(run_tasks)
    logging.info('Started scheduler')
    while True:
        sch.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
