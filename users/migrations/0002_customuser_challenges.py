# Generated by Django 4.1 on 2023-04-22 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='challenges',
            field=models.IntegerField(default=0),
        ),
    ]
