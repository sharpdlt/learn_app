# Generated by Django 4.0.5 on 2022-07-05 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='position',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='track',
            name='position',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
