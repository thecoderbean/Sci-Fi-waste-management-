# Generated by Django 5.0.1 on 2024-01-27 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_registereduser_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='img',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]