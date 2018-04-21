# Generated by Django 2.0.3 on 2018-04-18 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estimators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('worker_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='estimators.Estimator')),
            ],
        ),
    ]