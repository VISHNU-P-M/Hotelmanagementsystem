# Generated by Django 3.1.6 on 2021-02-26 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0008_auto_20210226_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(null='True', upload_to='pics')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.roomoverview')),
            ],
        ),
    ]
