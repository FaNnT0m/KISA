from django.db import migrations
from apps.main.data import (
    CLIENT_GROUP,
    DRIVER_GROUP,
)

def apply_migration(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Group = apps.get_model("auth", "Group")
    Group.objects.using(db_alias).bulk_create(
        [
            Group(name=CLIENT_GROUP),
            Group(name=DRIVER_GROUP),
        ]
    )

def revert_migration(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=
        [
            CLIENT_GROUP,
            DRIVER_GROUP,
        ]
    ).delete()

class Migration(migrations.Migration):
    
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
