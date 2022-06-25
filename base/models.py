from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bank(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    amount = models.FloatField()
from datetime import datetime
class Transcation(models.Model):
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount_spend = models.FloatField(null=False,blank=False)
    balance_in_bank = models.FloatField()
    message = models.TextField()
    type = models.CharField(max_length=10,choices=(('credit','credit'),('debit','debit')))
    transaction_date = models.DateTimeField(default=datetime.now())