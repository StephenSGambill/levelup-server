# Generated by Django 4.2 on 2023-05-03 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0003_alter_game_number_of_players_alter_game_skill_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='creator',
            new_name='gamer',
        ),
    ]
