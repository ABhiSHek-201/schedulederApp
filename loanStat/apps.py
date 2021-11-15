from django.apps import AppConfig

class LoanstatConfig(AppConfig):
    name = 'loanStat'

    def ready(self):
        print('start...')
        from .loan_mail_scheduler import mailer
        mailer.start()
