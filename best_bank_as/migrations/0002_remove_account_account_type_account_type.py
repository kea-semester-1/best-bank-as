# Generated by Django 4.2.5 on 2023-10-09 19:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="account_type",
        ),
        migrations.AddField(
            model_name="account",
            name="type",
            field=models.IntegerField(
                choices=[(1, "Savings"), (2, "Checking")], default=0
            ),
        ),
    ]
