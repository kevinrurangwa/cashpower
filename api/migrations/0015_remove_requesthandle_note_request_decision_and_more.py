# Generated by Django 5.0.6 on 2024-05-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_request_service_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requesthandle',
            name='note',
        ),
        migrations.AddField(
            model_name='request',
            name='decision',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='note',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
