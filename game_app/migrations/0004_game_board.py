# Generated by Django 3.1.3 on 2020-11-25 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0003_remove_game_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='board',
            field=models.CharField(default='*********', max_length=9),
        ),
    ]
