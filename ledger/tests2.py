
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Account


class AccountBalanceConstraintTests(TestCase):

    def test_zero_balance_is_allowed(self):
        account = Account.objects.create(
            name="Zero Balance Account",
            balance=Decimal("0.00"),
        )

        self.assertEqual(account.balance, Decimal("0.00"))

    def test_positive_balance_is_allowed(self):
        account = Account.objects.create(
            name="Positive Balance Account",
            balance=Decimal("100.00"),
        )

        self.assertEqual(account.balance, Decimal("100.00"))

    def test_negative_balance_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Account.objects.create(
                    name="Negative Balance Account",
                    balance=Decimal("-10.00"),
                )
