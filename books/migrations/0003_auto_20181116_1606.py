# Generated by Django 2.1.3 on 2018-11-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20181115_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='type_id',
            field=models.SmallIntegerField(choices=[(1, 'Python'), (3, 'algrithm and data sturcture'), (2, 'jacascript'), (4, 'mechinelearning'), (5, 'operating system'), (6, 'database management')], default=1, verbose_name='books category'),
        ),
    ]
