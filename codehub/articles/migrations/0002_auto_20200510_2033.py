# Generated by Django 2.2.8 on 2020-05-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(default='article content', max_length=32768),
        ),
    ]
