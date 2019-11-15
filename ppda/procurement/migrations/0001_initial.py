# Generated by Django 2.2.7 on 2019-11-06 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HeadOfDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=100)),
                ('hod', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='procurement.HeadOfDepartment')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=15)),
                ('hod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.HeadOfDepartment')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='user_department_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.UserDepartment'),
        ),
    ]
