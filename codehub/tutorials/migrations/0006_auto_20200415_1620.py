# Generated by Django 2.2.8 on 2020-04-15 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tutorials', '0005_tutorialarticle_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='last_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tutorialarticle',
            name='last_modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
