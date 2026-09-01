from django import forms
from .models import LedgerEntry


class LedgerEntryForm(forms.ModelForm):
    class Meta:
        model = LedgerEntry
        fields = ['account', 'to_account', 'outflow']

    def clean(self):
        cleaned_data = super().clean()

        account = cleaned_data.get('account')
        to_account = cleaned_data.get('to_account')
        outflow = cleaned_data.get('outflow') or 0

        # Cannot send to yourself
        if account and to_account and account == to_account:
            raise forms.ValidationError(
                "You cannot send money to the same account."
            )

        # Must enter an amount
        if outflow <= 0:
            raise forms.ValidationError(
                "Enter an amount greater than 0."
            )

        # Check withdrawal
        if account and outflow > account.balance:
            raise forms.ValidationError(
                "Withdrawal cannot be greater than the account balance."
            )

        return cleaned_data