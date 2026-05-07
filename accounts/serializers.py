from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from mlm.placement import place_member

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)
    position = serializers.ChoiceField(
        choices=['left', 'right'],
        required=False,
        allow_blank=True,
        write_only=True,
    )

    class Meta:
        model = UserModel
        fields = (
            'username', 'email', 'password', 'password2',
            'referral_code', 'position', 'phone', 'country',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': _('Passwords do not match.')
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        referral_code = validated_data.pop('referral_code', None)
        preferred_position = validated_data.pop('position', None)

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            country=validated_data.get('country', ''),
        )

        if referral_code:
            try:
                sponsor = UserModel.objects.get(referral_code=referral_code)
                place_member(user, sponsor, preferred_position=preferred_position)
            except UserModel.DoesNotExist:
                pass

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    sponsor_username = serializers.CharField(
        source='sponsor.username', read_only=True, default=None
    )
    placement_parent_username = serializers.CharField(
        source='placement_parent.username', read_only=True, default=None
    )
    referral_link = serializers.SerializerMethodField()
    referral_link_left = serializers.SerializerMethodField()
    referral_link_right = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            'id', 'username', 'email', 'phone', 'country',
            'membership_level', 'is_member', 'referral_code',
            'referral_link', 'referral_link_left', 'referral_link_right',
            'sponsor', 'sponsor_username',
            'placement_parent', 'placement_parent_username',
            'position', 'left_leg_units', 'right_leg_units',
            'total_pv', 'join_date', 'status',
        )
        read_only_fields = (
            'membership_level', 'is_member', 'referral_code',
            'referral_link', 'referral_link_left', 'referral_link_right',
            'left_leg_units', 'right_leg_units', 'total_pv',
        )

    def get_referral_link(self, obj):
        from django.conf import settings
        return f"{settings.SITE_URL}/register/?ref={obj.referral_code}"

    def get_referral_link_left(self, obj):
        from django.conf import settings
        return f"{settings.SITE_URL}/register/?ref={obj.referral_code}&pos=left"

    def get_referral_link_right(self, obj):
        from django.conf import settings
        return f"{settings.SITE_URL}/register/?ref={obj.referral_code}&pos=right"


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'membership_level', 'position', 'is_member', 'total_pv')
