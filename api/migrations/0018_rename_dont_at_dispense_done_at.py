# Generated by Django 5.0.6 on 2024-05-25 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_dispense_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dispense',
            old_name='dont_at',
            new_name='done_at',
        ),
    ]
