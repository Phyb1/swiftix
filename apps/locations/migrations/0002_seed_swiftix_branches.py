from django.db import migrations

# Deliberately no latitude/longitude here: we know the two addresses (they
# already lived in settings.BUSINESS_ADDRESS / GWERU_ADDRESS) but not the
# exact building coordinates, and a guessed pin is worse than no pin. Add
# them once via /admin/ — see Branch.latitude's help_text for how.
BRANCHES = [
    {
        "name": "Harare branch",
        "address": "No. 1 Tourle Rd, New Ardbennie, Southerton, Harare, Zimbabwe",
        "order": 1,
    },
    {
        "name": "Gweru branch",
        "address": "No. 6052, 58 Street, Shamrock, Gweru, Zimbabwe",
        "order": 2,
    },
]


def seed_branches(apps, schema_editor):
    Branch = apps.get_model("locations", "Branch")
    for data in BRANCHES:
        Branch.objects.get_or_create(name=data["name"], defaults=data)


def remove_seeded_branches(apps, schema_editor):
    Branch = apps.get_model("locations", "Branch")
    Branch.objects.filter(name__in=[b["name"] for b in BRANCHES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_branches, remove_seeded_branches),
    ]
