# Generated by Django 3.1.3 on 2020-12-05 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='date',
            field=models.DateField(blank=True, default='2020-12-05'),
        ),
    ]
