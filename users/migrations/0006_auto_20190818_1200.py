# Generated by Django 2.2.1 on 2019-08-18 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190818_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='image',
            field=models.CharField(default='null', max_length=200),
        ),
    ]
