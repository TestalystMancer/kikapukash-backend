# Generated by Django 5.1.7 on 2025-04-09 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_rename_type_transaction_transaction_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='from_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_wallet', to='wallet.wallet'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_wallet', to='wallet.wallet'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer')], max_length=10),
        ),
    ]
