from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.base import BaseScheduler
from logging import log
sched = BlockingScheduler()
# sched = BasegScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('clock')
    # log(msg='AAAAAAAA clock',level=1)+
    with open('sraka.txt','a') as f:
        f.write('123456\n')
    with open('sraka.txt','r') as d:
        print('clock',d.read())


# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()