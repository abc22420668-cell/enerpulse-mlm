"""
Binary Tree Placement Service for EnerPulse MLM.

Rules (from OlyLife compensation plan):
1. First referral MUST go to extreme left (極左) — creates depth
2. After first left placement, alternate left/right to balance
3. Placement parent is the last member in the chain at the chosen position
4. First unit purchased: member is placed under their sponsor
"""
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


def find_placement(sponsor, preferred_position=None):
    """
    Find where a new member should be placed in the binary tree.
    
    Rules:
    - If sponsor has NO downline at all → place at extreme left (first rule: 極左)
    - If sponsor has only left leg → place at right
    - If sponsor has only right leg → place at left
    - If sponsor has both legs → find the shallower leg and go to its deepest available spot
    
    Returns (placement_parent, position)
    """
    # Get sponsor's direct children (people placed directly under sponsor)
    left_child = User.objects.filter(placement_parent=sponsor, position='left').first()
    right_child = User.objects.filter(placement_parent=sponsor, position='right').first()

    # Rule: first referral MUST go to extreme left
    if not left_child:
        return sponsor, 'left'

    # Rule: if only left exists, place at right
    if left_child and not right_child:
        return sponsor, 'right'

    # Both exist — pick the leg with more depth potential
    # (we always prefer placing on the side where the tree is less filled)
    left_children_count = User.objects.filter(
        placement_parent__in=_get_all_in_leg(left_child, 'left'),
        position='left'
    ).count() + User.objects.filter(
        placement_parent__in=_get_all_in_leg(left_child, 'right'),
        position='right'
    ).count()
    right_children_count = User.objects.filter(
        placement_parent__in=_get_all_in_leg(right_child, 'left'),
        position='left'
    ).count() + User.objects.filter(
        placement_parent__in=_get_all_in_leg(right_child, 'right'),
        position='right'
    ).count()

    # Place on the side with fewer members (weaker leg)
    if preferred_position == 'left':
        target_child = left_child
        pos = 'left'
    elif preferred_position == 'right':
        target_child = right_child
        pos = 'right'
    elif left_children_count <= right_children_count:
        target_child = left_child
        pos = 'left'
    else:
        target_child = right_child
        pos = 'right'

    # Find deepest node in that leg for placement
    deepest = _get_deepest_leaf(target_child, pos)
    return deepest, pos


def _get_deepest_leaf(node, position):
    """
    Recursively find the deepest leaf node on the given side.
    """
    children = User.objects.filter(placement_parent=node).order_by('date_joined')

    left_child = next((c for c in children if c.position == 'left'), None)
    right_child = next((c for c in children if c.position == 'right'), None)

    if position == 'left':
        if left_child:
            return _get_deepest_leaf(left_child, position)
        return node
    else:
        if right_child:
            return _get_deepest_leaf(right_child, position)
        return node


def _get_all_in_leg(node, leg):
    """
    Get all descendants of a node on a specific leg.
    Returns a flat list of User IDs.
    """
    result = []
    children = User.objects.filter(placement_parent=node, position=leg)
    for child in children:
        result.append(child.id)
        result.extend(_get_all_in_leg(child, 'left'))
        result.extend(_get_all_in_leg(child, 'right'))
    return result


def place_member(new_user, sponsor, preferred_position=None):
    """
    Place a new member in the binary tree under their sponsor.
    
    Args:
        new_user: The new User instance (must already be saved)
        sponsor: The sponsor User instance
        preferred_position: 'left' or 'right' (optional override)
    
    Returns:
        (placement_parent, position)
    """
    placement_parent, position = find_placement(sponsor, preferred_position)

    new_user.placement_parent = placement_parent
    new_user.position = position
    new_user.sponsor = sponsor
    new_user.save(update_fields=['placement_parent', 'position', 'sponsor'])

    return placement_parent, position


@transaction.atomic
def activate_member(user):
    """
    Activate a member after their first unit purchase.
    
    Sets:
    - is_member = True
    - membership_level = 'P3'
    - Updates sponsor's leg unit counts
    """
    user.is_member = True
    user.membership_level = 'P3'
    user.total_pv += 750
    user.save(update_fields=['is_member', 'membership_level', 'total_pv'])

    # Update sponsor's leg unit counts
    if user.placement_parent:
        _update_leg_units(user.placement_parent)

    return user


def _update_leg_units(user):
    """Recalculate and update leg unit counts for a user up the tree."""
    left_units = _count_units_in_leg(user, 'left')
    right_units = _count_units_in_leg(user, 'right')

    changed = False
    if user.left_leg_units != left_units:
        user.left_leg_units = left_units
        changed = True
    if user.right_leg_units != right_units:
        user.right_leg_units = right_units
        changed = True

    if changed:
        user.save(update_fields=['left_leg_units', 'right_leg_units'])

    # Recurse up to update all ancestors
    if user.placement_parent:
        _update_leg_units(user.placement_parent)


def _count_units_in_leg(user, leg):
    """
    Count total active member units in a leg (includes the member themself if they're active).
    This counts ALL members below the user on that side, recursively.
    """
    children = User.objects.filter(placement_parent=user, position=leg, is_member=True)
    total = 0
    for child in children:
        total += 1  # Count the child
        total += _count_units_in_leg(child, 'left')
        total += _count_units_in_leg(child, 'right')
    return total


def get_upline(user, levels=6):
    """
    Get upline chain for matching bonus calculation.
    Returns list of (user, generation) tuples up to 'levels' generations.
    """
    upline = []
    current = user.sponsor
    gen = 1
    while current and gen <= levels:
        upline.append((current, gen))
        current = current.sponsor
        gen += 1
    return upline


def get_downline_direct(user):
    """Get all directly sponsored members (first generation)."""
    return User.objects.filter(sponsor=user, is_member=True).order_by('date_joined')


def get_team_tree(user, max_depth=5):
    """
    Build the full binary tree structure for display.
    Returns nested dict.
    """
    def _build_node(u, depth):
        if depth > max_depth:
            return None
        children = User.objects.filter(placement_parent=u).order_by('position')
        left = None
        right = None
        for child in children:
            if child.position == 'left':
                left = _build_node(child, depth + 1)
            elif child.position == 'right':
                right = _build_node(child, depth + 1)
        return {
            'id': u.id,
            'username': u.username,
            'membership_level': u.membership_level,
            'is_member': u.is_member,
            'pv': u.total_pv,
            'left': left,
            'right': right,
        }
    return _build_node(user, 0)
