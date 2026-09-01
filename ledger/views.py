from .forms import LedgerEntryForm
from .models import Account, LedgerEntry
from django.db import transaction
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect


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

                sender = Account.objects.select_for_update().get(
                    id=entry.account.id
                )

                receiver = Account.objects.select_for_update().get(
                    id=entry.to_account.id
                )

                sender.balance -= entry.outflow
                receiver.balance += entry.outflow

                sender.save()
                receiver.save()

                LedgerEntry.objects.create(
                    account=receiver,
                    inflow=entry.outflow
                )

            return redirect('home')

    else:
        form = LedgerEntryForm()

    return render(request, 'ledger.html', {
        'form': form
    })


def account_detail(request, account_id):
    account = Account.objects.get(id=account_id)

    entries = LedgerEntry.objects.filter(
        account=account
    ).order_by('-created_at')

    return render(request, 'ledger/account_detail.html', {
        'account': account,
        'entries': entries
    })

def add_card(request):
    accounts = Account.objects.all()

    return render(request, 'add_card.html', {
        'accounts': accounts,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

def save_card(request):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Invalid request'},
            status=400
        )

    data = json.loads(request.body)

    account_id = data.get('account_id')
    payment_method_id = data.get('payment_method_id')

    try:
        account = Account.objects.get(id=account_id)

        account.stripe_payment_method_id = payment_method_id
        account.save()

        return JsonResponse({'success': True})

    except Account.DoesNotExist:
        return JsonResponse(
            {'error': 'Account not found'},
            status=404
        )