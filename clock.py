from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.base import BaseScheduler
from logging import log
sched = BlockingScheduler()
# sched = BasegScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    log(msg='AAAAAAAA',level=1)
    with open('sraka.txt','w') as f:
        f.write('123456\n')


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()