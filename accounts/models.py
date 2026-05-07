import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with MLM-specific fields."""
    
    # MLM tree fields
    sponsor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sponsored_members',
        verbose_name=_('Sponsor'),
        help_text=_('The member who referred this user'),
    )
    placement_parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children',
        verbose_name=_('Placement Parent'),
        help_text=_('The member under whom this user is placed in the binary tree'),
    )
    position = models.CharField(
        max_length=5, choices=[('left', 'Left'), ('right', 'Right')],
        null=True, blank=True,
        verbose_name=_('Position'),
        help_text=_('Position in the binary tree (left or right leg)'),
    )
    
    # Membership
    MEMBERSHIP_CHOICES = [
        ('none', _('Non-Member')),
        ('P3', _('P3')),
        ('P4', _('P4')),
        ('P5', _('P5')),
    ]
    membership_level = models.CharField(
        max_length=10, choices=MEMBERSHIP_CHOICES,
        default='none',
        verbose_name=_('Membership Level'),
    )
    membership_expiry = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_('Membership Expiry'),
    )
    is_member = models.BooleanField(
        default=False,
        verbose_name=_('Is Member'),
        help_text=_('Whether this user is an active member'),
    )
    
    # Registration
    referral_code = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False,
        verbose_name=_('Referral Code'),
    )
    join_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Join Date'),
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('Active')),
            ('inactive', _('Inactive')),
            ('suspended', _('Suspended')),
        ],
        default='active',
        verbose_name=_('Status'),
    )
    
    # Personal info
    phone = models.CharField(
        max_length=20, blank=True,
        verbose_name=_('Phone'),
    )
    country = models.CharField(
        max_length=100, blank=True,
        verbose_name=_('Country'),
    )
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True,
        verbose_name=_('Avatar'),
    )
    
    # MLM Stats (cached for quick lookup)
    left_leg_units = models.IntegerField(default=0, verbose_name=_('Left Leg Units'))
    right_leg_units = models.IntegerField(default=0, verbose_name=_('Right Leg Units'))
    total_pv = models.IntegerField(default=0, verbose_name=_('Total PV'))
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_full_name() or self.email})"
    
    def get_referral_link(self, request=None):
        """Generate the referral link for this user."""
        from django.conf import settings
        base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        return f"{base_url}/register/?ref={self.referral_code}"
    
    def get_team_count(self):
        """Get total number of members in downline."""
        return self.sponsored_members.count()
    
    def get_weak_leg_units(self):
        """Get the smaller leg's unit count (for pairing bonus)."""
        return min(self.left_leg_units, self.right_leg_units)
    
    def get_strong_leg_units(self):
        """Get the larger leg's unit count."""
        return max(self.left_leg_units, self.right_leg_units)
