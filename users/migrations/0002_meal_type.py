# Generated by Django 2.2.1 on 2019-08-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='type',
            field=models.CharField(default='Main', max_length=15),
        ),
    ]
