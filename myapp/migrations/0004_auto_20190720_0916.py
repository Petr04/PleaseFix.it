# Generated by Django 2.2.3 on 2019-07-20 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20190720_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='id',
            field=models.AutoField(auto_created=True, default=123, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='problem',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
