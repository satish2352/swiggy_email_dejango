# Generated by Django 4.2.8 on 2024-02-16 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_searcheddate_delete_searched_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searcheddate',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]