# Generated by Django 4.2.5 on 2023-09-23 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0005_remove_ledger_account_number1_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="TransactionTable",
            new_name="Transaction",
        ),
        migrations.RenameField(
            model_name="ledger",
            old_name="transaction",
            new_name="transaction_id",
        ),
        migrations.RemoveField(
            model_name="ledger",
            name="id",
        ),
        migrations.AddField(
            model_name="ledger",
            name="ledger_id",
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
