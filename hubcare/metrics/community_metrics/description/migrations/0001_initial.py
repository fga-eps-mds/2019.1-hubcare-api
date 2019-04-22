# Generated by Django 2.1.7 on 2019-04-22 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=200)),
                ('repo', models.CharField(max_length=200)),
                ('description', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=None)),
            ],
        ),
    ]
