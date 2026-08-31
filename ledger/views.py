from django.shortcuts import render, redirect
from .forms import LedgerEntryForm
from .models import Account, LedgerEntry
from django.db import transaction 


def home(request):
    accounts = Account.objects.all()

    return render(request, 'ledger/home.html', {
        'accounts': accounts
    })



def create_entry(request):
    if request.method == 'POST':
        form = LedgerEntryForm(request.POST)

        if form.is_valid():
            with transaction.atomic():

                entry = form.save()

                account = Account.objects.select_for_update().get(
                    id=entry.account.id
                )

                if entry.inflow > 0:
                    account.balance += entry.inflow

                elif entry.outflow > 0:
                    account.balance -= entry.outflow

                account.save()

            return redirect('home')

    else:
        form = LedgerEntryForm()

    return render(request, 'ledger.html', {
        'form': form
    })


def account_detail(request, account_id):
    account = Account.objects.get(id=account_id)
    #find the account using ID

    entries = LedgerEntry.objects.filter(
        account=account
    ).order_by('-created_at')
    #find transactino belong to that account and sorted them by date

    return render(request, 'ledger/account_detail.html', {
        'account': account,
        'entries': entries
        #Show the transaction to the user
    })