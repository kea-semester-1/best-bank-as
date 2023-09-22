# Generated by Django 4.2.5 on 2023-09-22 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('best_bank_as', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerLevel',
            fields=[
                ('customer_level_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_level_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='customer_level_name',
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='best_bank_as.customerlevel'),
            preserve_default=False,
        ),
    ]
