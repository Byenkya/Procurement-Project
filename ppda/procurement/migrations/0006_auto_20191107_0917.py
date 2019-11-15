# Generated by Django 2.2.7 on 2019-11-07 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0005_auto_20191107_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hod',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procurement.HeadOfDepartment'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='procurement.Member'),
        ),
    ]
