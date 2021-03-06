# Generated by Django 2.0.3 on 2018-06-06 02:42

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ETLHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_inserted_id', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('number_of_records', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FactTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=500)),
                ('task_requester', models.CharField(max_length=999)),
                ('task_payment', models.FloatField()),
                ('time_it_took', models.FloatField()),
                ('age', models.PositiveIntegerField()),
                ('education', models.CharField(choices=[('BS', "Bachelor's degree"), ('MS', "Master's degree"), ('PHD', 'Doctorate'), ('PROF', 'Higher level of Education')], max_length=4, verbose_name='Level of education')),
                ('nationality', models.CharField(max_length=4)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('day', models.PositiveIntegerField()),
                ('day_of_week', models.CharField(max_length=999)),
                ('time_of_day', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SimilarWorkersBasedOnModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar_workers', django.contrib.postgres.fields.jsonb.JSONField()),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
