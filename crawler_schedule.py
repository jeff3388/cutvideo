import asyncio
from twseo_crawler import main
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def daily_job_A():
    main()

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()  # 異步非阻塞式
    scheduler.add_job(daily_job_A, 'interval', minutes=1)

    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)