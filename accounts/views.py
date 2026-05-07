from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .serializers import (
    UserRegistrationSerializer,
    UserDetailSerializer,
    UserMinimalSerializer,
)
from mlm.placement import activate_member, get_team_tree, get_downline_direct

UserModel = get_user_model()


# --- Separate register view (bypasses DRF ViewSet for CSRF safety) ---

@csrf_exempt
@require_POST
def register_view(request):
    """Register a new user. If referral_code is provided,
    they're placed in the sponsor's binary tree."""
    import json
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    serializer = UserRegistrationSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse(
            UserDetailSerializer(user).data,
            status=201,
        )
    return JsonResponse(serializer.errors, status=400)


# --- Main ViewSet ---

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for user management and MLM tree."""
    queryset = UserModel.objects.all()

    def get_serializer_class(self):
        return UserDetailSerializer

    def get_permissions(self):
        if self.action in ('me', 'activate', 'tree', 'downline', 'referral_info'):
            return [permissions.IsAuthenticated()]
        # list/retrieve require auth too
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile with MLM info."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def activate(self, request):
        """Activate current user as a member (triggered after first purchase)."""
        user = request.user
        if user.is_member:
            return Response(
                {'error': _('Already a member.')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = activate_member(user)
        return Response(UserDetailSerializer(user).data)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get the binary tree structure for the current user (5 levels deep)."""
        user = request.user
        tree_data = get_team_tree(user, max_depth=5)
        return Response(tree_data)

    @action(detail=False, methods=['get'])
    def downline(self, request):
        """Get direct downline (first-gen referrals) for current user."""
        downline = get_downline_direct(request.user)
        return Response(UserMinimalSerializer(downline, many=True).data)

    @action(detail=False, methods=['get'])
    def referral_info(self, request):
        """Get referral link and stats for current user."""
        user = request.user
        return Response({
            'referral_code': str(user.referral_code),
            'referral_link': user.get_referral_link(),
            'referral_count': user.sponsored_members.count(),
            'downline_count': user.get_team_count(),
            'left_leg_units': user.left_leg_units,
            'right_leg_units': user.right_leg_units,
            'weak_leg_units': user.get_weak_leg_units(),
            'strong_leg_units': user.get_strong_leg_units(),
        })
