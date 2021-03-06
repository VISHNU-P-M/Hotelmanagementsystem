# Generated by Django 3.1.6 on 2021-02-15 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenities', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Receptionist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RoomOverView',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('rooms', models.BigIntegerField()),
                ('available', models.BigIntegerField()),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('pic1', models.ImageField(null='True', upload_to='pics')),
                ('pic2', models.ImageField(null='True', upload_to='pics')),
                ('pic3', models.ImageField(null='True', upload_to='pics')),
                ('pic4', models.ImageField(null='True', upload_to='pics')),
                ('pic5', models.ImageField(null='True', upload_to='pics')),
                ('pic6', models.ImageField(null='True', upload_to='pics')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admin1.category')),
            ],
        ),
        migrations.CreateModel(
            name='AmenitiesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.amenities')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.roomoverview')),
            ],
        ),
    ]
