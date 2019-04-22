# Generated by Django 2.2 on 2019-04-22 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=150)),
                ('repo', models.CharField(max_length=150)),
                ('have_license', models.BooleanField(default=False)),
                ('date_time', models.DateTimeField(default=None)),
            ],
        ),
    ]