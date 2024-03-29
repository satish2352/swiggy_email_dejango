# Generated by Django 4.2.8 on 2024-02-16 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_alter_searcheddate_from_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='searcheddate',
            name='check_updated',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='searcheddate',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
