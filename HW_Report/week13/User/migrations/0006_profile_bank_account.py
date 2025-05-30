# Generated by Django 5.2 on 2025-05-17 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_notification_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bank_account',
            field=models.CharField(blank=True, help_text='Format: (XXX)XXXXXXXXXXXXXX', max_length=17, validators=[django.core.validators.RegexValidator(code='invalid_bank_account', message='Bank account must be in format (XXX)XXXXXXXXXXXXXX, where X are digits', regex='^\\(\\d{3}\\)\\d{14}$')]),
        ),
    ]
