# Generated by Django 3.1.4 on 2021-10-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='0546882609', max_length=15),
            preserve_default=False,
        ),
    ]
