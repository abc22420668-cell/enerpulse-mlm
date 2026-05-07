from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@login_required
def mlm_dashboard(request):
    """MLM team tree dashboard."""
    return render(request, 'mlm/dashboard.html')


@login_required
def mlm_tree(request):
    """Binary tree visualization."""
    return render(request, 'mlm/tree.html')


@login_required
def mlm_bonuses(request):
    """Bonus history page."""
    return render(request, 'mlm/bonuses.html')
