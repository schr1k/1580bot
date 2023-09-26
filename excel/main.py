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

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


async def tasks():
    t1 = asyncio.create_task(make_schedule_1())
    t2 = asyncio.create_task(make_schedule_2())
    t3 = asyncio.create_task(make_schedule_3h())
    t4 = asyncio.create_task(make_schedule_3p())
    t5 = asyncio.create_task(make_schedule_4h())
    t6 = asyncio.create_task(make_schedule_4p())
    await t1
    await t2
    await t3
    await t4
    await t5
    await t6


def run_tasks():
    asyncio.run(tasks())
    logging.info('Successfully updated schedule')
    return sch.CancelJob


def main():
    sch.every().day.at('00:00').do(run_tasks)
    logging.info('Started scheduler')
    while True:
        sch.run_pending()
        time.sleep(1)
