# Generated by Django 4.1.1 on 2022-09-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_alter_replies_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='replies',
            name='like',
            field=models.ManyToManyField(related_name='reply_liked_by', through='groups.Like', to='groups.member'),
        ),
    ]
