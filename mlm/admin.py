from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class PlacementFilter(admin.SimpleListFilter):
    """Filter users by whether they have a placement in the binary tree."""
    title = _('Tree Placement')
    parameter_name = 'has_placement'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Has placement')),
            ('no', _('No placement')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(placement_parent__isnull=True)
        if self.value() == 'no':
            return queryset.filter(placement_parent__isnull=True)
        return queryset


# Re-register User admin from accounts/admin.py with enhanced features
# (accounts/admin.py already has UserAdmin registered)
