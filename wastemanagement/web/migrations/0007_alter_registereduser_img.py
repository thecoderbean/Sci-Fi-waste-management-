# Generated by Django 5.0.1 on 2024-01-28 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_registereduser_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registereduser',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
