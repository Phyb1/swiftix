from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0002_seed_swiftix_branches"),
    ]

    operations = [
        migrations.AddField(
            model_name="branch",
            name="map_image",
            field=models.ImageField(
                blank=True,
                help_text=(
                    "Optional screenshot/photo showing this branch's "
                    "location (e.g. a Google Maps screenshot). Leave "
                    "blank to show just the directions button."
                ),
                null=True,
                upload_to="branches/",
            ),
        ),
    ]
