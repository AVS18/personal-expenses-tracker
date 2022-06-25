from django.contrib import admin

from base.models import Transcation,Bank

# Register your models here.
class BankRef(admin.ModelAdmin):
    list_display=['name','amount']
    list_filter=['name','user']

class TransactionRef(admin.ModelAdmin):
    list_display = ['message','amount_spend','balance_in_bank','type','transaction_date']
    list_filter = ['bank__name','user','transaction_date','type']

admin.site.register(Bank,BankRef)
admin.site.register(Transcation,TransactionRef)