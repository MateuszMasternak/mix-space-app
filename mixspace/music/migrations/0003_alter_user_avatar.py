# Generated by Django 4.1.1 on 2022-09-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_user_avatar_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]