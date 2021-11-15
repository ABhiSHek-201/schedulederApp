from apscheduler.schedulers.background import BackgroundScheduler
from loanStat.views import StateLoansView
from apscheduler.triggers.cron import CronTrigger

def start():
    scheduler = BackgroundScheduler()
    loan_rep = StateLoansView()
    scheduler.add_job(loan_rep.send_mails_daily,trigger=CronTrigger(hour="10"),id="loanRep",max_instances=1,replace_existing=True)
    scheduler.start()