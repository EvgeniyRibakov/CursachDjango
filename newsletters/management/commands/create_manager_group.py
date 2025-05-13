# newsletters/management/commands/create_manager_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Creates the Managers group with specific permissions"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Managers")
        permissions = [
            "can_view_all_newsletters",
            "can_view_all_messages",
            "can_view_all_recipients",
            "can_disable_newsletters",
        ]
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)
        self.stdout.write(
            self.style.SUCCESS("Successfully created Managers group with permissions")
        )
