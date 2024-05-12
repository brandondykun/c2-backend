# Generated by Django 5.0.4 on 2024-04-26 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core_app", "0002_alter_profile_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="Point",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("ENEMY", "Enemy"),
                            ("FRIENDLY", "Friendly"),
                            ("NEUTRAL", "Neutral"),
                            ("UNKNOWN", "Unknown"),
                            ("NAVIGATION", "Navigation"),
                        ],
                        default="NAVIGATION",
                        max_length=12,
                    ),
                ),
                ("label", models.CharField(max_length=64)),
                ("description", models.CharField(max_length=255)),
                ("lat", models.FloatField()),
                ("lng", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_points",
                        to="core_app.profile",
                    ),
                ),
                (
                    "mission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mission_points",
                        to="core_app.mission",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_points",
                        to="core_app.mission",
                    ),
                ),
            ],
        ),
    ]
