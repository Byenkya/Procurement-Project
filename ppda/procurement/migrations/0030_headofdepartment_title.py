# Generated by Django 2.2.7 on 2019-11-25 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0029_member_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='headofdepartment',
            name='title',
            field=models.CharField(default='', max_length=30),
        ),
    ]
