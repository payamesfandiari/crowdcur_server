# Generated by Django 2.0.3 on 2018-06-06 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facttable',
            name='worker',
            field=models.CharField(default='', max_length=999),
            preserve_default=False,
        ),
    ]