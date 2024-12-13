from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse
from .forms import UserRegistrationForm, DepositWithdrawForm, BillPaymentForm, TransferForm
from django.contrib.auth import logout as auth_logout
from .models import Account, Transaction
# Create your views here.
def Index(requset):
    return render(requset, 'index.html')



def Registration(request):
 if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registersuccess.html', {'account_number': user.account.account_number})
 else:
    form = UserRegistrationForm()
        
        
 return render(request, 'registration.html', {'form': form})

def RegisterSuccess(requset):
    return render(requset, 'registersuccess.html')

def Login(requset):
    if requset.method == 'POST':
        username = requset.POST['username']
        password = requset.POST['password']
        user = authenticate(requset, username=username, password=password)
        if user is not None:
            login(requset, user)
            return redirect('account')
    return render(requset, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def Main(requset):
    return render(requset, 'main.html')

def ProfileAccount(requset):
    account = requset.user.account
    transactions = Transaction.objects.filter(account=account)
    return render(requset, 'account.html', {'account': account, 'transactions': transactions, })

def Update_Account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('updated')
    else:
        form = UserRegistrationForm(instance=request.user)
    return render(request, 'updateprofile.html', {'form': form})

def deposit(request):
    if request.method == 'POST':
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return redirect('account')
    else:
        form = DepositWithdrawForm()
    return render(request, 'deposit.html', {'form': form})

def withdraw(request):
    if request.method == 'POST':
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = request.user.account
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return redirect('account')
    else:
        form = DepositWithdrawForm()
    return render(request, 'withdraw.html', {'form': form})


def bill_payment(request):
     if request.method == 'POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            bill_type = form.cleaned_data['bill_type']
            amount = form.cleaned_data['amount']
            account = request.user.account
            
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='bill_payment')
                
                # Integrate with payment gateway here
                payment_response = process_payment(bill_type, amount)
                
                if payment_response['status'] == 'success':
                    return redirect('payment_success')
                else:
                    return render(request, 'payment_failed.html', {'error': payment_response['message']})
            else:
                return render(request, 'bill_payment.html', {'form': form, 'error': 'Insufficient balance.'})
     else:
        form = BillPaymentForm()
     return render(request, 'bill_payment.html', {'form': form})

def process_payment(bill_type, amount):
    # Simulate payment processing
    # Replace with actual payment gateway integration
    return {'status': 'success', 'message': 'Payment processed successfully.'}

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_account_number = form.cleaned_data['recipient_account_number']
            account = request.user.account
            try:
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Account transfer')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Account to resive')
                    return redirect('account')
            except Account.DoesNotExist:
                form.add_error('recipient_account_number', 'Account does not exist.')
    else:
        form = TransferForm()
    return render(request, 'accounttransfer.html', {'form': form})

def Updated(request):
    return render(request, 'updatedsuccessful.html')