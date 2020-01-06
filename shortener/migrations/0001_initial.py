# Generated by Django 3.0.2 on 2020-01-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(unique=True)),
                ('shortURL', models.TextField(unique=True)),
                ('visited', models.IntegerField(default=0)),
            ],
        ),
    ]
