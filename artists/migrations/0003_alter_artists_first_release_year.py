# Generated by Django 4.0 on 2023-06-05 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_alter_artists_first_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artists',
            name='first_release_year',
            field=models.CharField(max_length=4),
        ),
    ]
