# Generated by Django 2.1.3 on 2018-11-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='type_id',
            field=models.SmallIntegerField(choices=[(1, 'Python'), (2, 'algrithm and data sturcture'), (4, 'mechinelearning'), (5, 'operating system'), (6, 'database management')], default=1, max_length=10, verbose_name='books category'),
        ),
    ]