import asyncio
from one.main import make_schedule_1
from two.main import make_schedule_2
from three.high.main import make_schedule_3h
from three.primary.main import make_schedule_3p
from four.high.main import make_schedule_4h
from four.primary.main import make_schedule_4p
import schedule as sch
import time


async def main():
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


def run_main():
    asyncio.run(main())
    return sch.CancelJob


if __name__ == "__main__":
    sch.every().day.at('00:00').do(run_main)

    while True:
        sch.run_pending()
        time.sleep(1)
