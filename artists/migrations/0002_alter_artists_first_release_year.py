# Generated by Django 4.0 on 2023-06-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artists',
            name='first_release_year',
            field=models.DateField(),
        ),
    ]