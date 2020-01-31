# Generated by Django 2.2.4 on 2020-01-30 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fixture',
            options={'ordering': ['date_time'], 'verbose_name': 'fixture', 'verbose_name_plural': 'fixtures'},
        ),
        migrations.RemoveField(
            model_name='fixture',
            name='fixed_by',
        ),
        migrations.AlterField(
            model_name='fixture',
            name='fixed_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]