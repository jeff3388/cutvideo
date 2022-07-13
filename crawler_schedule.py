import asyncio
from twseo_crawler import main
from insert_que import insert_que
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def daily_job_crawler_tw1():
    main("tw1")

def daily_job_insert_que_tw1():
    insert_que("tw1")

def daily_job_crawler_twseo():
    main("twseo")

def daily_job_insert_que_twseo():
    insert_que("twseo")

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()  # 異步非阻塞式
    scheduler.add_job(daily_job_crawler_twseo, 'interval', minutes=2)
    scheduler.add_job(daily_job_insert_que_twseo, 'interval', minutes=1)

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)