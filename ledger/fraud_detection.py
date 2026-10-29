
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from .models import LedgerEntry


def assess_transaction(account, amount, to_account=None):
    """
    Calculate a risk score from 0 to 100.
    Run this before saving the proposed transfer.
    """

    amount = Decimal(str(amount))
    reasons = []
    score = 0

    # Get the sender's previous outgoing transfers.
    history = LedgerEntry.objects.filter(
        account=account,
        outflow__gt=0,
    ).order_by("-created_at")

    # Signal 1: Unusually large transfer (+30)
    if amount >= Decimal("1000.00"):
        score += 30
        reasons.append("Large transfer amount")

    # Signal 2: Rapid repeated transfers (+25)
    five_minutes_ago = timezone.now() - timedelta(minutes=5)

    recent_count = history.filter(
        created_at__gte=five_minutes_ago
    ).count()

    if recent_count >= 3:
        score += 25
        reasons.append("Multiple recent outgoing transfers")

    # Signal 3: Sudden change in transfer amount (+30)
    previous_amounts = list(
        history.values_list("outflow", flat=True)[:10]
    )

    if len(previous_amounts) >= 3:
        average_amount = sum(
            previous_amounts, Decimal("0")
        ) / len(previous_amounts)

        if (
            average_amount > 0
            and amount >= average_amount * Decimal("3")
        ):
            score += 30
            reasons.append(
                "Transfer is at least 3 times the recent average"
            )

    # Signal 4: First-time recipient (+15)
    if to_account is not None:
        previous_recipient = history.filter(
            to_account=to_account
        ).exists()

        if not previous_recipient:
            score += 15
            reasons.append("First-time recipient")

    # Keep the score within 0–100.
    score = min(score, 100)

    if score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
        "review_required": score >= 60,
    }
