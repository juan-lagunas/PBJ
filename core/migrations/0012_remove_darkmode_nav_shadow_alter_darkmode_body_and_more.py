# Generated by Django 4.2.1 on 2023-05-12 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='darkmode',
            name='nav_shadow',
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='body',
            field=models.CharField(default='bg-gray-300 text-black', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='mode',
            field=models.CharField(default='Light', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='nav',
            field=models.CharField(default='bg-gray-200 drop-shadow-sm', max_length=64),
        ),
        migrations.AlterField(
            model_name='darkmode',
            name='user',
            field=models.CharField(max_length=64),
        ),
    ]
