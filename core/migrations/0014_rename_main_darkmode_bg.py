# Generated by Django 4.2.1 on 2023-05-12 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_darkmode_main_alter_darkmode_body_alter_darkmode_nav'),
    ]

    operations = [
        migrations.RenameField(
            model_name='darkmode',
            old_name='main',
            new_name='bg',
        ),
    ]
