# Generated by Django 3.0.3 on 2020-03-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20200302_0239'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
