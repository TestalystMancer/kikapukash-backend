# Generated by Django 5.1.7 on 2025-04-06 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_role',
            field=models.CharField(choices=[('admin', 'Admin'), ('member', 'member')], default='member', max_length=10),
        ),
    ]
