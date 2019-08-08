# Generated by Django 2.1.5 on 2019-08-06 20:26

from django.db import migrations, models
import easyvolunteer.models


class Migration(migrations.Migration):

    dependencies = [
        ('easyvolunteer', '0003_auto_20190805_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNum',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[easyvolunteer.models.phone_number_validator], verbose_name='전화번호'),
        ),
    ]
