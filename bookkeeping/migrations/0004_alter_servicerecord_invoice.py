# Generated by Django 5.2.1 on 2025-05-29 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookkeeping', '0003_invoice_servicerecord_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerecord',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='bookkeeping.invoice'),
        ),
    ]
