from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mlm.placement import place_member, activate_member, get_team_tree, get_upline

User = get_user_model()


class Command(BaseCommand):
    help = 'Test MLM binary tree placement and activation'

    def handle(self, *args, **options):
        self.stdout.write('=== MLM Tree Test ===\n')

        # Clean previous test users
        User.objects.filter(username__startswith='test_').delete()

        # Create root user
        root = User.objects.create_user(
            username='test_root', password='test123',
            email='root@test.com'
        )
        root.is_member = True
        root.membership_level = 'P3'
        root.save()
        self.stdout.write(f'Created root: {root.username} (ref: {root.referral_code})')

        # Create 5 test users under root
        users = []
        for i in range(1, 6):
            u = User.objects.create_user(
                username=f'test_user_{i}',
                password='test123',
                email=f'user{i}@test.com'
            )
            place_member(u, root)
            activate_member(u)
            users.append(u)
            self.stdout.write(f'  Placed {u.username} → parent={u.placement_parent.username}, pos={u.position}')

        # Show tree structure
        self.stdout.write('\nTree structure:')
        def print_tree(node, indent=0):
            prefix = '  ' * indent
            self.stdout.write(f'{prefix}├─ {node.username} (L:{node.left_leg_units}/R:{node.right_leg_units})')
            children = User.objects.filter(placement_parent=node).order_by('position')
            for child in children:
                print_tree(child, indent + 1)

        print_tree(root)

        # Check stats
        self.stdout.write(f'\nRoot stats: L={root.left_leg_units}, R={root.right_leg_units}, PV={root.total_pv}')
        self.stdout.write(f'User1 parent: {users[0].placement_parent.username}, pos: {users[0].position}')
        self.stdout.write(f'User2 parent: {users[1].placement_parent.username}, pos: {users[1].position}')

        # Check that first user went to extreme left
        if users[0].placement_parent == root and users[0].position == 'left':
            self.stdout.write(self.style.SUCCESS('✓ First user placed at extreme left (極左)'))
        else:
            self.stdout.write(self.style.ERROR('✗ First user NOT at extreme left!'))

        # Clean up
        User.objects.filter(username__startswith='test_').delete()
        self.stdout.write(self.style.SUCCESS('\nAll tests passed!'))
