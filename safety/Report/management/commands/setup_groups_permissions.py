from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Setup initial Groups and Permissions mapping"

    def handle(self, *args, **options):
        # สร้าง ContentType กลางสำหรับ custom permissions
        content_type, _ = ContentType.objects.get_or_create(
            app_label="Report", model="basereport"
        )

        permissions = [
            ("add_report", "Can create hazard/incident/BBS report"),
            ("view_hazard_log", "Can view hazard log"),
            ("assess_risk", "Can perform risk assessment"),
            ("manage_cap", "Can create, update, and close CAP"),
            ("verify_cap", "Can verify CAP"),
            ("access_investigation", "Can access accident investigation module"),
            ("manage_evidence", "Can view and manage evidence in oversight cases"),
        ]

        # สร้าง permission objects
        perm_objects = {}
        for codename, name in permissions:
            perm, _ = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={"name": name},
            )
            perm.name = name  # update description เผื่อแก้ไขภายหลัง
            perm.save()
            perm_objects[codename] = perm

        # 👥 mapping group → permissions
        groups = {
            "Operator": ["add_report", "view_hazard_log"],
            "FlightBoard": ["view_hazard_log", "assess_risk", "manage_cap"],
            "FlightCommander": ["view_hazard_log", "assess_risk", "manage_cap", "verify_cap"],
            "RTAFInspector": ["view_hazard_log", "assess_risk", "manage_cap", "verify_cap", "access_investigation"],
            "Executive": ["view_hazard_log", "verify_cap", "access_investigation", "manage_evidence"],
            "UnitAdmin": ["add_report", "view_hazard_log", "assess_risk", "manage_cap", "verify_cap"],
            "CentralAdmin": list(perm_objects.keys()),  # full access
        }

        # สร้าง groups + assign perms
        for group_name, perm_codenames in groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()
            for codename in perm_codenames:
                group.permissions.add(perm_objects[codename])
            self.stdout.write(self.style.SUCCESS(f"✅ Group '{group_name}' updated."))

        self.stdout.write(self.style.SUCCESS("🎉 Groups and Permissions setup completed!"))
