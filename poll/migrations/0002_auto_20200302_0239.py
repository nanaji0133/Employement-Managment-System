# Generated by Django 3.0.3 on 2020-03-02 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={},
        ),
        migrations.RemoveField(
            model_name='question',
            name='tags',
        ),
    ]