# Generated by Django 3.1.1 on 2020-09-08 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='product',
            name='details',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
