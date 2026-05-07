from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@login_required
def wallet_dashboard(request):
    """Virtual wallet page."""
    return render(request, 'wallet/dashboard.html')


@login_required
def wallet_transactions(request):
    """Transaction history page."""
    return render(request, 'wallet/transactions.html')


@login_required
def wallet_withdraw(request):
    """Withdrawal request page."""
    return render(request, 'wallet/withdraw.html')
