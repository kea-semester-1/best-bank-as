from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("best_bank_as", "0003_account_account_status"),
    ]

    operations = [
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
                default=1,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Pending"), (2, "Approved"), (3, "Rejected")], default=1
            ),
        ),
    ]
