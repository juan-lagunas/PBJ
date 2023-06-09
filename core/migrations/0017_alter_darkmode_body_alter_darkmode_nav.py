# Generated by Django 4.2.1 on 2023-05-14 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_darkmode_body_alter_darkmode_hover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='darkmode',
            name='body',
            field=models.CharField(default='bg-slate-300 text-slate-800', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='nav',
            field=models.CharField(default='drop-shadow-sm bg-slate-200', max_length=64),
        ),
    ]
