from django.db import models

class Borrowers(models.Model):
    name = models.CharField(max_length=255)
    loan_id = models.IntegerField()
    state = models.CharField(max_length=255)
    loan_amt = models.IntegerField()
    amt_paid = models.IntegerField()

    def __str__(self):
        return self.name+"_"+self.state +"_"+str(self.loan_id)
