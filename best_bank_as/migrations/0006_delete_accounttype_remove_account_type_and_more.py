# Generated by Django 4.2.5 on 2024-01-21 21:42

import datetime

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0005_alter_loanapplication_status"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AccountType",
        ),
        migrations.RemoveField(
            model_name="account",
            name="type",
        ),
        migrations.RemoveField(
            model_name="ledger",
            name="account_number",
        ),
        migrations.RemoveField(
            model_name="ledger",
            name="transaction_id",
        ),
        migrations.AddField(
            model_name="account",
            name="account_type",
            field=models.IntegerField(
                choices=[(1, "Savings"), (2, "Checking"), (3, "Loan"), (4, "Internal")],
                default=1,
            ),
        ),
        migrations.AddField(
            model_name="ledger",
            name="account",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.account",
            ),
        ),
        migrations.AddField(
            model_name="ledger",
            name="transaction",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.transaction",
            ),
        ),
        migrations.AddField(
            model_name="loan",
            name="loan_account",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.account",
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="account_number",
            field=models.IntegerField(blank=True, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name="account",
            name="account_status",
            field=models.IntegerField(
                choices=[
                    (1, "Active"),
                    (2, "Inactive"),
                    (3, "Pending"),
                    (4, "Rejected"),
                ],
                default=2,
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="customer",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.customer",
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="end_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2026, 1, 20, 21, 42, 54, 870233, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="start_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="loanapplication",
            name="customer",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="best_bank_as.customer",
            ),
        ),
    ]
