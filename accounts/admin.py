from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'membership_level', 'status',
        'sponsor', 'position', 'left_leg_units', 'right_leg_units',
        'is_member', 'date_joined',
    )
    list_filter = ('membership_level', 'status', 'is_member', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('MLM Information'), {
            'fields': (
                'sponsor', 'placement_parent', 'position',
                'membership_level', 'membership_expiry', 'is_member',
                'referral_code', 'status',
            ),
        }),
        (_('MLM Stats'), {
            'fields': ('left_leg_units', 'right_leg_units', 'total_pv'),
        }),
        (_('Contact Info'), {
            'fields': ('phone', 'country', 'avatar'),
        }),
    )
    
    readonly_fields = ('referral_code', 'join_date')
    
    actions = ['activate_members', 'deactivate_members']
    
    def activate_members(self, request, queryset):
        queryset.update(is_member=True, status='active')
    activate_members.short_description = _('Activate selected members')
    
    def deactivate_members(self, request, queryset):
        queryset.update(is_member=False, status='inactive')
    deactivate_members.short_description = _('Deactivate selected members')
