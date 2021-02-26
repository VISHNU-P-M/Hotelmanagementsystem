# Generated by Django 3.1.6 on 2021-02-19 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin1', '0002_auto_20210215_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceptionBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('no_of_room', models.IntegerField(null=True)),
                ('no_of_guest', models.IntegerField(null=True)),
                ('pay_status', models.BooleanField(null=True)),
                ('checked_out', models.BooleanField(default=False, null=True)),
                ('reception', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.receptionist')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.roomoverview')),
            ],
        ),
    ]
