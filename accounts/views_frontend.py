from django.shortcuts import render
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def home(request):
    """Home page view."""
    return render(request, 'accounts/home.html')


def login_view(request):
    """Login page."""
    return render(request, 'accounts/login.html')


def register_view(request):
    """Registration page with referral code support."""
    referral_code = request.GET.get('ref', '')
    return render(request, 'accounts/register.html', {
        'referral_code': referral_code,
    })


def profile_view(request):
    """User profile dashboard."""
    return render(request, 'accounts/profile.html')
