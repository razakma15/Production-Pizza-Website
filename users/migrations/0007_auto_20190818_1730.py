# Generated by Django 2.2.1 on 2019-08-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190818_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.CharField(default='null', max_length=1000),
        ),
    ]
