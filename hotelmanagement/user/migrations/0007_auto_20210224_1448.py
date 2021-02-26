# Generated by Django 3.1.6 on 2021-02-24 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0006_auto_20210224_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='Id_proof',
            field=models.ImageField(null='True', upload_to='pics'),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='details',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
