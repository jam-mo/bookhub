# Generated by Django 4.1 on 2023-05-07 20:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libsystem', '0004_bookrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.CharField(default=' ', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='ratings',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterUniqueTogether(
            name='bookrating',
            unique_together={('book', 'user')},
        ),
    ]
