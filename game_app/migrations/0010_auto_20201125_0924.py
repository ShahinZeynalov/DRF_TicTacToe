# Generated by Django 3.1.3 on 2020-11-25 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0009_auto_20201125_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.IntegerField(blank=True, choices=[(1, 'Uwin'), (2, 'Cwin'), (-1, 'Draw'), (0, 'Nd')], default=0, null=True),
        ),
    ]
