# Generated by Django 4.1 on 2023-05-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libsystem', '0002_bookrental_loanee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ratings',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
