from django import forms
from .models import LedgerEntry


class LedgerEntryForm(forms.ModelForm):
    class Meta:
        model = LedgerEntry
        fields = ['account', 'inflow', 'outflow']

    def clean(self):
        cleaned_data = super().clean()

        account = cleaned_data.get('account')
        inflow = cleaned_data.get('inflow') or 0
        outflow = cleaned_data.get('outflow') or 0

        # Cannot have both
        if inflow > 0 and outflow > 0:
            raise forms.ValidationError(
                "A transaction cannot have both inflow and outflow."
            )

        # Must enter something
        if inflow == 0 and outflow == 0:
            raise forms.ValidationError(
                "Enter an inflow or an outflow."
            )

        # Check withdrawal
        if account and outflow > 0:
            if outflow > account.balance:
                raise forms.ValidationError(
                    "Withdrawal cannot be greater than the account balance."
                )

        return cleaned_data