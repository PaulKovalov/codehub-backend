# Generated by Django 2.2.8 on 2020-04-03 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0002_auto_20200124_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]