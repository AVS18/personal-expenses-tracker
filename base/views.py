from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from .models import Bank,Transcation
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    return render(request,"login.html")

def check_user_authenticated(request):
    if not request.user.is_authenticated:
        return redirect('/login')

def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        obj =authenticate(username=username,password=password)
        if obj is not None:
            auth.login(request,obj)
            return redirect('/dashboard')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Wrong Username/Password')
            return render(request,"login.html")

def get_bank_balance(request):
    banks = Bank.objects.filter(user=request.user)
    if len(banks)==0:
        total = 0
    else:
        total = sum([bank.amount for bank in banks])
    return {'banks':banks,'total':total}

def dashboard(request):
    check_user_authenticated(request)
    bank_balance = get_bank_balance(request)
    return render(request,"dashboard.html",bank_balance)

def addExpense(request):
    check_user_authenticated(request)
    if request.method=="POST":
        transaction_date = request.POST["transaction_date"]
        type = request.POST["type"]
        bank = request.POST["bank"]
        amount_spend = request.POST['amount']
        message = request.POST["message"]
        bank = Bank.objects.filter(id=bank,user=request.user)
        if len(bank)==0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'No Such Bank Exist. Check Bank Addition Page')
        else:
            if type=="credit":
                final_amount = bank[0].amount + float(amount_spend)
                bank[0].amount = final_amount
                Transcation.objects.create(type=type,bank=bank[0],user=request.user,transaction_date=transaction_date,message=message,amount_spend=amount_spend,balance_in_bank = final_amount)
                bank[0].save()
                storage = messages.get_messages(request)
                storage.used=True
                messages.info(request,"Transaction Added Successfully")
                return redirect('/dashboard')
            elif type=='debit':
                final_amount = bank[0].amount - float(amount_spend)
                bank[0].amount = final_amount
                Transcation.objects.create(type=type,bank=bank[0],user=request.user,transaction_date=transaction_date,message=message,amount_spend=amount_spend,balance_in_bank = final_amount)
                bank[0].save()
                storage = messages.get_messages(request)
                storage.used=True
                messages.info(request,"Transaction Added Successfully")
                return redirect('/dashboard')
            else:
                storage = messages.get_messages(request)
                storage.used=True
                messages.info(request,"Wrong Type")
                return redirect('/dashboard')
    bank_balance = get_bank_balance(request)
    return render(request,"addExpense.html",bank_balance)

def addBank(request):
    check_user_authenticated(request)
    if request.method=="POST":
        name = request.POST["name"]
        amount = request.POST["amount"]
        Bank.objects.create(name=name,amount=amount,user=request.user)
        storage = messages.get_messages(request)
        storage.used=True
        messages.info(request,"Bank Added Successfully")
        return redirect('/dashboard')
    bank_balance = get_bank_balance(request)
    return render(request,'addBank.html',bank_balance)

def displayExpense(request):
    check_user_authenticated(request)
    bank_balance = get_bank_balance(request)
    if 'start_date' not in request.GET:
        transactions = Transcation.objects.filter(user=request.user).order_by('transaction_date')
        amount_debit = sum([transaction.amount_spend for transaction in transactions if transaction.type=='debit'])
        amount_credit = sum([transaction.amount_spend for transaction in transactions if transaction.type=='credit'])
        return render(request,"displayExpense.html",{'transactions':transactions,'amount_credit':amount_credit,'amount_debit':amount_debit,'banks':bank_balance['banks'],'total':bank_balance['total']})
    elif request.method=="GET":
        start_date = request.GET["start_date"]
        end_date = request.GET["end_date"]
        bank = request.GET["bank"]
        bank_obj = Bank.objects.filter(user=request.user,id=bank)
        if len(bank_obj)==0:
            storage = messages.get_messages(request)
            storage.used=True
            messages.info(request,"Wrong Type")
            return redirect('/dashboard')
        transactions = Transcation.objects.filter(transaction_date__range=(start_date,end_date),bank=bank_obj[0],user=request.user).order_by('transaction_date')
        amount_debit = sum([transaction.amount_spend for transaction in transactions if transaction.type=='debit'])
        amount_credit = sum([transaction.amount_spend for transaction in transactions if transaction.type=='credit'])
        return render(request,"displayExpense.html",{'transactions':transactions,'amount_credit':amount_credit,'amount_debit':amount_debit,'banks':bank_balance['banks'],'total':bank_balance['total']})
    else:
        storage = messages.get_messages(request)
        storage.used=True
        messages.info(request,"Something went wrong")        
        return redirect('/dashboard')

def deleteTransaction(request,tid):
    check_user_authenticated(request)
    transaction_obj = Transcation.objects.filter(user=request.user,id=tid)
    if len(transaction_obj)>0:
        if transaction_obj[0].type=='credit':
            bank_obj = Bank.objects.filter(id=transaction_obj[0].bank.id,user=request.user)
            current_amount_in_bank = bank_obj[0].amount
            transaction_amount = transaction_obj[0].amount_spend
            final_amount = current_amount_in_bank - transaction_amount
            Bank.objects.filter(id = bank_obj[0].id,user=request.user).update(amount=final_amount)
            Transcation.objects.filter(id=transaction_obj[0].id,user=request.user).delete()
            storage = messages.get_messages(request)
            storage.used=True
            messages.info(request,"Transaction Deleted Successfully")
        elif transaction_obj[0].type=='debit':
            bank_obj = Bank.objects.filter(id=transaction_obj[0].bank.id,user=request.user)
            current_amount_in_bank = bank_obj[0].amount
            transaction_amount = transaction_obj[0].amount_spend
            final_amount = current_amount_in_bank + transaction_amount
            Bank.objects.filter(id = bank_obj[0].id,user=request.user).update(amount=final_amount)
            Transcation.objects.filter(id=transaction_obj[0].id,user=request.user).delete()
            storage = messages.get_messages(request)
            storage.used=True
            messages.info(request,"Transaction Deleted Successfully")
    else:
        storage = messages.get_messages(request)
        storage.used=True
        messages.info(request,"No Such Transaction Exists")
    return redirect('/displayExpense')

def logout(request):
    check_user_authenticated(request)
    auth.logout(request)
    return redirect('/')