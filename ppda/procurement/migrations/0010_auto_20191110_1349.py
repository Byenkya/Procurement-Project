# Generated by Django 2.2.7 on 2019-11-10 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0009_auto_20191107_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProcurementStage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stage_name', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=200)),
                ('office_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Office')),
            ],
        ),
        migrations.AddField(
            model_name='headofdepartment',
            name='signature',
            field=models.ImageField(default='123.png', upload_to=''),
        ),
        migrations.AddField(
            model_name='member',
            name='signature',
            field=models.ImageField(default='123.png', upload_to=''),
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reference_number', models.CharField(max_length=15)),
                ('financial_year', models.CharField(max_length=4)),
                ('pde_code', models.CharField(max_length=10)),
                ('sequence_number', models.CharField(max_length=10)),
                ('requisition_type', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=10)),
                ('plan_reference', models.CharField(max_length=10)),
                ('delivery_location', models.CharField(max_length=10)),
                ('date_required', models.DateField()),
                ('initiation', models.DateField()),
                ('member_confirmation', models.BooleanField()),
                ('hod_confirmation', models.BooleanField()),
                ('member_confirmation_date', models.DateField()),
                ('hod_confirmation_date', models.DateField()),
                ('date_of_submission', models.DateField()),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Member')),
                ('procurement_stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.ProcurementStage')),
                ('user_department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.UserDepartment')),
            ],
        ),
        migrations.CreateModel(
            name='OfficeMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('telephone', models.CharField(max_length=15)),
                ('signature', models.ImageField(upload_to='')),
                ('office_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Office')),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('unit_of_measure', models.IntegerField()),
                ('estimated_cost', models.IntegerField()),
                ('currency', models.CharField(max_length=10)),
                ('market_price', models.IntegerField()),
                ('requisition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='procurement.Requisition')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='office_member_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='procurement.OfficeMember'),
        ),
    ]