# Generated by Django 4.2.5 on 2024-01-21 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0005_bank_alter_account_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="ledger",
            name="registration_number",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.bank",
            ),
        ),
    ]
