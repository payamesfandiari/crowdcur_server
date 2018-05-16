# Generated by Django 2.0.3 on 2018-05-14 21:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdcur', '0002_workermodelhistorymodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskfeaturesmodel',
            name='task_feature',
        ),
        migrations.AddField(
            model_name='taskfeaturesmodel',
            name='feature',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
