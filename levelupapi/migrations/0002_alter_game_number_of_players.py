# Generated by Django 4.2 on 2023-05-02 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='number_of_players',
            field=models.CharField(max_length=20),
        ),
    ]