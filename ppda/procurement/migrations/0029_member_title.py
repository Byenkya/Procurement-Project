# Generated by Django 2.2.7 on 2019-11-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0028_auto_20191124_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='title',
            field=models.CharField(default='', max_length=30),
        ),
    ]
