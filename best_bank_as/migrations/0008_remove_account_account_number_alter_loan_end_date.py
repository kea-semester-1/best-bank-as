# Generated by Django 4.2.5 on 2024-01-21 22:03

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0007_alter_ledger_amount_alter_loan_end_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="account_number",
        ),
        migrations.AlterField(
            model_name="loan",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2026, 1, 20, 22, 3, 32, 770083, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
