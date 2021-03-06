# Generated by Django 2.1.3 on 2018-11-16 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='delete mark')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
                ('recipient_name', models.CharField(max_length=20, verbose_name='signer_name')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='signer_address')),
                ('zip_code', models.CharField(max_length=6, verbose_name='postalcode')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='signer_phone')),
                ('is_default', models.BooleanField(default=False, verbose_name='the default address')),
                ('passport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Passport', verbose_name='user account')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
