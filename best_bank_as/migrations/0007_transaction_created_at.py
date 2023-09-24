# Generated by Django 4.2.5 on 2023-09-23 11:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0006_rename_transactiontable_transaction_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
