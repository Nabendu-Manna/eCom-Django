# Generated by Django 3.1.1 on 2020-09-15 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='status',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
