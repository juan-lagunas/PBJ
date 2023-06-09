# Generated by Django 4.2.1 on 2023-05-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_darkmode_bg_darkmode_hover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='darkmode',
            name='body',
            field=models.CharField(default='drop-shadow-md bg-slate-200', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='hover',
            field=models.CharField(default='hover:bg-slate-700 hover:text-slate-200', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='nav',
            field=models.CharField(default='drop-shadow-md bg-slate-200', max_length=64),
        ),
    ]
